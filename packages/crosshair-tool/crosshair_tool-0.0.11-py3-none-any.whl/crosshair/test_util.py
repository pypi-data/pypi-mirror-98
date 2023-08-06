from copy import deepcopy
from dataclasses import replace
from dataclasses import dataclass
from traceback import extract_tb
import types

from crosshair.core import analyze_function
from crosshair.core import realize
from crosshair.core import deep_realize
from crosshair.core import run_checkables
from crosshair.core import AnalysisMessage
from crosshair.core import Checkable
from crosshair.core import MessageType
from crosshair.options import AnalysisOptions
from crosshair.options import AnalysisOptionSet
from crosshair.options import DEFAULT_OPTIONS
from crosshair.util import debug
from crosshair.util import in_debug
from crosshair.util import name_of_type
from crosshair.util import test_stack
from crosshair.util import UnexploredPath
from crosshair.util import IgnoreAttempt
from typing import *

ComparableLists = Tuple[List, List]


def check_fail(
    fn: Callable, optionset: AnalysisOptionSet = AnalysisOptionSet()
) -> ComparableLists:
    local_opts = AnalysisOptionSet(max_iterations=40, per_condition_timeout=5)
    options = local_opts.overlay(optionset)
    states = [m.state for m in run_checkables(analyze_function(fn, options))]
    return (states, [MessageType.POST_FAIL])


def check_exec_err(
    fn: Callable, message_prefix="", optionset: AnalysisOptionSet = AnalysisOptionSet()
) -> ComparableLists:
    local_opts = AnalysisOptionSet(max_iterations=20, per_condition_timeout=5)
    options = local_opts.overlay(optionset)
    messages = run_checkables(analyze_function(fn, options))
    if all(m.message.startswith(message_prefix) for m in messages):
        return ([m.state for m in messages], [MessageType.EXEC_ERR])
    else:
        return (
            [(m.state, m.message) for m in messages],
            [(MessageType.EXEC_ERR, message_prefix)],
        )


def check_post_err(
    fn: Callable, optionset: AnalysisOptionSet = AnalysisOptionSet()
) -> ComparableLists:
    local_opts = AnalysisOptionSet(max_iterations=20)
    options = local_opts.overlay(optionset)
    states = [m.state for m in run_checkables(analyze_function(fn, options))]
    return (states, [MessageType.POST_ERR])


def check_unknown(
    fn: Callable, optionset: AnalysisOptionSet = AnalysisOptionSet()
) -> ComparableLists:
    local_opts = AnalysisOptionSet(max_iterations=40, per_condition_timeout=3)
    options = local_opts.overlay(optionset)
    messages = [
        (m.state, m.message, m.traceback)
        for m in run_checkables(analyze_function(fn, options))
    ]
    return (messages, [(MessageType.CANNOT_CONFIRM, "Not confirmed.", "")])


def check_ok(
    fn: Callable, optionset: AnalysisOptionSet = AnalysisOptionSet()
) -> ComparableLists:
    local_opts = AnalysisOptionSet(per_condition_timeout=5)
    options = local_opts.overlay(optionset)
    messages = [
        message
        for message in run_checkables(analyze_function(fn, options))
        if message.state != MessageType.CONFIRMED
    ]
    return (messages, [])


def check_messages(checkables: Iterable[Checkable], **kw) -> ComparableLists:
    msgs = run_checkables(checkables)
    if kw.get("state") != MessageType.CONFIRMED:
        # Normally, ignore confirmation messages:
        msgs = [m for m in msgs if m.state != MessageType.CONFIRMED]
    else:
        # When we are checking confirmation, just check one:
        msgs = [msgs[0]]
    default_msg = AnalysisMessage(MessageType.CANNOT_CONFIRM, "", "", 0, 0, "")
    msg = msgs[0] if msgs else replace(default_msg)
    fields = (
        "state",
        "message",
        "filename",
        "line",
        "column",
        "traceback",
        "test_fn",
        "condition_src",
    )
    for k in fields:
        if k not in kw:
            default_val = getattr(default_msg, k)
            msg = replace(msg, **{k: default_val})
            kw[k] = default_val
    if msgs:
        msgs[0] = msg
    return (msgs, [AnalysisMessage(**kw)])


@dataclass(eq=False)
class ExecutionResult:
    ret: object  # return value
    exc: Optional[BaseException]  # exception raised, if any
    # args after the function terminates:
    post_args: Sequence
    post_kwargs: Mapping[str, object]

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExecutionResult):
            return False
        return (
            self.ret == other.ret
            and type(self.exc) == type(other.exc)
            and self.post_args == other.post_args
            and self.post_kwargs == other.post_kwargs
        )

    def describe(self, include_postexec=False) -> str:
        ret = ""
        if self.exc:
            exc = self.exc
            exc_type = name_of_type(type(exc))
            tb = test_stack(exc.__traceback__)
            ret = f"exc={exc_type}: {str(exc)} {tb}"
        else:
            ret = f"ret={self.ret!r}"
        if include_postexec:
            a = [repr(a) for a in self.post_args]
            a += [f"{k}={v!r}" for k, v in self.post_kwargs.items()]
            ret += f'  post=({", ".join(a)})'
        return ret


def summarize_execution(
    fn: Callable, args: Sequence[object] = (), kwargs: Mapping[str, object] = None
) -> ExecutionResult:
    if not kwargs:
        kwargs = {}
    ret = None
    exc = None
    try:
        _ret = realize(fn(*args, **kwargs))
        # summarize iterators as the values they produce:
        if hasattr(_ret, "__next__"):
            ret = list(_ret)
        else:
            ret = _ret
    except BaseException as e:
        if isinstance(e, (UnexploredPath, IgnoreAttempt)):
            raise
        if in_debug():
            debug(type(e), e, test_stack(e.__traceback__))
        exc = e
    args = tuple(realize(a) for a in args)
    kwargs = {k: realize(v) for (k, v) in kwargs.items()}
    return ExecutionResult(ret, exc, args, kwargs)


@dataclass
class ResultComparison:
    left: ExecutionResult
    right: ExecutionResult

    def __bool__(self):
        return self.left == self.right

    def __repr__(self):
        left, right = self.left, self.right
        include_postexec = left.ret == right.ret and type(left.exc) == type(right.exc)
        return (
            left.describe(include_postexec)
            + "  <-symbolic-vs-concrete->  "
            + right.describe(include_postexec)
        )


def compare_results(fn: Callable, *a: object, **kw: object) -> ResultComparison:
    original_a = deepcopy(a)
    original_kw = deepcopy(kw)
    symbolic_result = summarize_execution(fn, a, kw)

    concrete_a = deep_realize(original_a)
    concrete_kw = deep_realize(original_kw)
    concrete_result = summarize_execution(fn, concrete_a, concrete_kw)

    ret = ResultComparison(symbolic_result, concrete_result)
    bool(ret)
    return ret
