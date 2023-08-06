# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
This module contains workarounds for the fact that some builtin methods appear
to be unpatchable using funchook for one reason or another.
"""
import sys

from contrast.extern.six import PY2, PY3, binary_type, text_type

import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager
from contrast.agent.assess.policy.analysis import skip_analysis
from contrast.agent.policy.loader import Policy
from contrast.agent.assess.policy.propagation_policy import (
    PROPAGATOR_ACTIONS,
    propagate,
)
from contrast.agent.assess.policy.preshift import Preshift
from contrast.assess_extensions import smart_setattr
from contrast.utils.patch_utils import patch_cls_or_instance


from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


PY38 = PY3 and sys.version_info[1] == 8


def bytearray_join_patch(orig_method, patch_policy, self, *args, **kwargs):
    # Since we need to make reference to the input multiple times, convert the
    # first argument to a list and use that instead. This prevents any iterators
    # from being exhausted before we can make use of them in propagation.
    # For bytearray.join, args == (list_or_iterator_of_things_to_join,...)
    # Note that this is different from the C hooks for other join methods. In
    # those cases, the PyObject *args argument corresponds to just the list or
    # iterator itself, in contrast to a tuple that contains that list or
    # iterator. (Got that straight?)
    args_list = [list(args[0])] + list(args[1:])
    result = orig_method(self, *args_list, **kwargs)

    context = contrast.CS__CONTEXT_TRACKER.current()
    if skip_analysis(context) or scope.in_scope():
        return result

    try:
        frame = sys._getframe()
        with scope.propagation_scope():
            propagate("join", result, self, result, frame, args_list, kwargs)
    except Exception:
        logger.exception("failed to propagate bytearray.join")
    finally:
        return result


def str_format_patch(orig_method, patch_policy, self, *args, **kwargs):
    """
    Propagation hook for str.format

    This hook is a special case because we need to enable some propagation to occur
    while we evaluate whether to propagate this particular event. With the current
    general hook infrastructure, this is not possible, so we need to account for it
    here. Eventually it may be possible to fit this back into the more general
    infrastructure if we overhaul the way that scope works.
    """
    result = orig_method(self, *args, **kwargs)

    context = contrast.CS__CONTEXT_TRACKER.current()
    if skip_analysis(context) or scope.in_scope():
        return result

    try:
        with scope.contrast_scope():
            frame = sys._getframe()

            policy = Policy()
            preshift = Preshift(self, args, kwargs)

        for node in policy.propagators_by_name["BUILTIN.str.format"]:
            propagator_class = PROPAGATOR_ACTIONS.get(node.action)
            if propagator_class is None:
                continue

            propagator = propagator_class(node, preshift, result)

            # This evaluation must not occur in scope. This is what enables us
            # to perform any conversions from object to __str__ or __repr__,
            # while allowing propagation to occur through those methods if
            # necessary.
            if not propagator.needs_propagation:
                continue

            with scope.contrast_scope():
                propagator.track_and_propagate(result, frame)
    except Exception:
        logger.exception("failed to propagate str.format")
    finally:
        return result


def generic_str_patch(orig_method, patch_policy, self, *args, **kwargs):
    """
    General-purpose patch implementation to be used for replacing string methods
    """
    result = orig_method(self, *args, **kwargs)

    context = contrast.CS__CONTEXT_TRACKER.current()
    if skip_analysis(context) or scope.in_scope():
        return result

    try:
        frame = sys._getframe()
        with scope.propagation_scope():
            propagate(orig_method.__name__, result, self, result, frame, args, kwargs)
    except Exception:
        name = orig_method.__class__.__name__
        logger.exception("failed to propagate %s.%s", name, orig_method.__name__)
    finally:
        return result


def patch_py38_methods():
    """
    Apply patches for methods that can't be hooked with funchook in Py38

    Specifically, the `strip`, `lstrip`, and `rstrip` methods of both `str` and
    `bytes` can't be hooked with funchook.
    """
    for strtype in [str, bytes]:
        for method_name in ["strip", "lstrip", "rstrip"]:
            patch_cls_or_instance(strtype, method_name, generic_str_patch)


def patch_format_methods():
    patch_cls_or_instance(str, "format", str_format_patch)

    if PY2:
        patch_cls_or_instance(text_type, "format", str_format_patch)


def property_getter(self):
    return contrast.STRING_TRACKER.get(self, None)


def property_setter(self, value):
    contrast.STRING_TRACKER.update_properties(self, value)


def enable_str_properties():
    strprop = property(fget=property_getter, fset=property_setter)

    smart_setattr(text_type, "cs__properties", strprop)
    smart_setattr(binary_type, "cs__properties", strprop)
    smart_setattr(bytearray, "cs__properties", strprop)


def patch_strtype_methods():
    """
    Apply patches for all methods that can't be hooked with funchook

    For reasons that are not well understood, funchook fails to apply patches
    to certain methods on certain platforms. Now that we can hook builtins
    directly from Python, we apply the workarounds here. There is probably a
    performance penalty for having these patches implemented purely in Python,
    but it's better than not hooking these methods at all.

    Currently the only versions affected are Py3 and higher, but if we ever
    have problems with Py2 hooks, those workarounds should be added here too.
    """
    enable_str_properties()

    patch_cls_or_instance(text_type, "partition", generic_str_patch)
    patch_cls_or_instance(text_type, "rpartition", generic_str_patch)

    patch_format_methods()

    # Patching bytearray.join with funchook does not work for any Py3 versions
    if PY3:
        patch_cls_or_instance(bytearray, "join", bytearray_join_patch)

    if PY38:
        patch_py38_methods()


def unpatch_strtype_methods():
    """
    Replace all patched strtype methods with the original implementation
    """
    patch_manager.reverse_patches_by_owner(text_type)
    patch_manager.reverse_patches_by_owner(binary_type)
    patch_manager.reverse_patches_by_owner(bytearray)
