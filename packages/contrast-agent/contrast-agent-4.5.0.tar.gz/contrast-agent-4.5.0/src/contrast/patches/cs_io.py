# -*- coding: utf-8 -*-
# Copyright © 2020 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import functools
import sys
from contrast.extern.wrapt import register_post_import_hook

from contrast.agent.policy import patch_manager
from contrast.utils.patch_utils import patch_cls_or_instance
from contrast.utils.assess.stream_utils import stream_patch_body

from contrast.extern import structlog as logging

logger = logging.getLogger("contrast")


def patched_func(orig_func, patch_policy, self, *args, **kwargs):
    bound_method = functools.partial(orig_func, self)
    return stream_patch_body(orig_func.__name__, bound_method, self, *args, **kwargs)


def patch_method(io_type, method_name):
    patch_cls_or_instance(io_type, method_name, patched_func)


def patch_getvalue(io_module):
    patch_method(io_module.StringIO, "getvalue")
    patch_method(io_module.BytesIO, "getvalue")


def patch_io(io_module):
    """
    Apply patches to methods of builtin stream types
    """
    for io_type in [io_module.StringIO, io_module.BytesIO]:
        patch_method(io_type, "write")

    # No need to hook StringIO.writelines because it is implemented as str.join under
    # the hood, so we already propagate for free. Unfortunately this might make the
    # reporting look a little odd, so we maybe should consider another solution later.
    patch_method(io_module.BytesIO, "writelines")

    # This patch exists solely for the purposes of working around our inability
    # to patch getvalue in StringIO and BytesIO using funchook.
    patch_getvalue(io_module)


def register_patches():
    register_post_import_hook(patch_io, "io")


def reverse_patches():
    io_module = sys.modules.get("io")
    if not io_module:
        return

    patch_manager.reverse_patches_by_owner(io_module)
    patch_manager.reverse_patches_by_owner(io_module.BytesIO)
    patch_manager.reverse_patches_by_owner(io_module.StringIO)
