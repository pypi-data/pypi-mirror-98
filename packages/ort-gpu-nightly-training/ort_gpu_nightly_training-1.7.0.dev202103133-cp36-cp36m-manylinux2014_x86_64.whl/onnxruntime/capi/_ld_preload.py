# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
# --------------------------------------------------------------------------

# This file can be modified by setup.py when building a manylinux2010 wheel
# When modified, it will preload some libraries needed for the python C extension
# Do not remove or move the following comment

# LD_PRELOAD_BEGIN_MARK
from ctypes import CDLL, RTLD_GLOBAL
_libcublas = CDLL("libcublas.so.10", mode=RTLD_GLOBAL)
_libcudnn = CDLL("libcudnn.so.8", mode=RTLD_GLOBAL)
_libcurand = CDLL("libcurand.so.10", mode=RTLD_GLOBAL)
_libcufft = CDLL("libcufft.so.10", mode=RTLD_GLOBAL)
_libcudart = CDLL("libcudart.so.10.2", mode=RTLD_GLOBAL)
