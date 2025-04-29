# -*- coding: utf-8 -*-

#------------------------- \cond COPYRIGHT --------------------------#
#                                                                    #
# Copyright (C) 2024 HOLOEYE Photonics AG. All rights reserved.      #
# Contact: https://holoeye.com/contact/                              #
#                                                                    #
# This file is part of HOLOEYE SLM Display SDK.                      #
#                                                                    #
# You may use this file under the terms and conditions of the        #
# "HOLOEYE SLM Display SDK Standard License v1.0" license agreement. #
#                                                                    #
#----------------------------- \endcond -----------------------------#


import sys

from ctypes import *
from hedslib.heds_types import *

## \cond INTERNALDOC
## Stores if the current Python version is 3 or higher
isPython3 = sys.version_info[0] == 3
## \endcond

## Stores if NumPy could be found.
# \ingroup SLMDisplayPython
supportNumPy = True

try:
    import numpy
except:
    supportNumPy = False

# A class holding information about the provided data before passing into the HOLOEYE library.
# Please provide your Python data in constructor.
# This class supports up to 2d data, and if three dimensional data is passed into the constructor,
# it is taken as RGB format, so that image data loaded using PIL can be passed here.
class HoloeyeInputDataDescriptor:
    # Shows arbitrary data on the slm.
    # \param data A ctypes or numpy data pointer.
    def __init__(self, data):
        # Is HEDSERR_NoError after initialization if the provided data is valid.
        self.error_code = HEDSERR_InvalidDataFormat
        self.c_data_ptr = None  # c_char_p()
        self.data_format = HEDSDTFMT_INT_U8
        self.width = 0
        self.height = 0
        self.pitch = 0

        # Create an array of the single pixel value, to be evaluated below:
        if isinstance(data, int):
            dat_tmp = data
            data = ((ctypes.c_ubyte * 1) * 1)()
            data[0][0] = ctypes.c_ubyte(dat_tmp)
        elif isinstance(data, float):
            dat_tmp = data
            data = ((ctypes.c_float * 1) * 1)()
            data[0][0] = ctypes.c_float(dat_tmp)
        elif isinstance(data, heds_rgb24):
            dat_tmp = data
            data = ((heds_rgb24 * 1) * 1)()
            data[0][0] = dat_tmp
        elif isinstance(data, heds_rgba32):
            dat_tmp = data
            data = ((heds_rgba32 * 1) * 1)()
            data[0][0] = dat_tmp

        # At this point we need to have an array type, else it would be an error.

        # Check width and height is both greater than 0 (works for numpy and ctypes the same way:
        self.height = len(data)
        if self.height < 1:
            self.error_code = HEDSERR_InvalidDataHeight
            return

        self.width = len(data[0])
        if self.width < 1:
            self.error_code = HEDSERR_InvalidDataWidth
            return

        # Detect format type of the data and set data pointer in case everything went smooth:
        if supportNumPy and isinstance(data, numpy.ndarray):
            type = data.dtype.type

            if type is numpy.uint8:
                if len(data.shape) < 3:
                    self.data_format = HEDSDTFMT_INT_U8
                    self.error_code = HEDSERR_NoError
                if len(data.shape) == 3:
                    if (data.shape[2] == 1):
                        self.data_format = HEDSDTFMT_INT_U8
                        self.error_code = HEDSERR_NoError
                    elif (data.shape[2] == 3):
                        self.data_format = HEDSDTFMT_INT_RGB24
                        self.error_code = HEDSERR_NoError
                    elif (data.shape[2] == 4):
                        self.data_format = HEDSDTFMT_INT_RGBA32
                        self.error_code = HEDSERR_NoError

            if type is numpy.single:
                self.data_format = HEDSDTFMT_FLOAT_32
                self.error_code = HEDSERR_NoError

            if type is numpy.double:
                self.data_format = HEDSDTFMT_FLOAT_64
                self.error_code = HEDSERR_NoError

            # convert numpy data to ctypes data pointer:
            if self.error_code == HEDSERR_NoError:
                self.c_data_ptr = data.ctypes

            return

        elif isinstance(data, ctypes.Array):
            type = data._type_._type_

            if type is ctypes.c_ubyte:
                self.data_format = HEDSDTFMT_INT_U8
                self.error_code = HEDSERR_NoError

            if type is heds_rgb24:
                self.data_format = HEDSDTFMT_INT_RGB24
                self.error_code = HEDSERR_NoError

            if type is heds_rgba32:
                self.data_format = HEDSDTFMT_INT_RGBA32
                self.error_code = HEDSERR_NoError

            if type is ctypes.c_float:
                self.data_format = HEDSDTFMT_FLOAT_32
                self.error_code = HEDSERR_NoError

            if type is ctypes.c_double:
                self.data_format = HEDSDTFMT_FLOAT_64
                self.error_code = HEDSERR_NoError

            if self.error_code == HEDSERR_NoError:
                self.c_data_ptr = data


# A class to allocate storage to be passed into SLM Display SDKs Library API functions when retrieving data from the
# SLM. SLM Display SDK writes into the data pointer of our self-allocated storage block, so that the data is valid
# after the API call, and the SDK does no allocation for us.
class HoloeyeOutputDataDescriptor:
    def __init__(self, width, height, dataformat=HEDSDTFMT_FLOAT_32, useNumpy=True):
        # Is HEDSERR_NoError after initialization if the provided data is valid.
        self.error_code = HEDSERR_NoError
        self.data = None
        self.c_data_ptr = None  # c_char_p()
        self.data_format = dataformat
        self.width = width
        self.height = height
        self.pitch = 0  # default pitch 0 is supported by the SDK. This is automatically width * element_size.

        if supportNumPy and useNumpy:
            nparray_dtype = numpy.float32
            third_dim = 1
            if self.data_format == HEDSDTFMT_FLOAT_64:
                nparray_dtype = numpy.float64
            elif self.data_format == HEDSDTFMT_INT_U8:
                nparray_dtype = numpy.uint8
            elif self.data_format == HEDSDTFMT_INT_RGB24:
                nparray_dtype = numpy.uint8
                third_dim = 3
            elif self.data_format == HEDSDTFMT_INT_RGB24:
                nparray_dtype = numpy.uint8
                third_dim = 4

            shape = [self.height, self.width]
            if third_dim > 1:
                shape = [self.height, self.width, third_dim]
            self.data = numpy.zeros(shape, dtype=nparray_dtype)
            self.c_data_ptr = self.data.ctypes

        else:  # ctypes data
            if self.data_format == HEDSDTFMT_FLOAT_32:
                self.data = ((ctypes.c_float * self.width) * self.height)()
            elif self.data_format == HEDSDTFMT_FLOAT_64:
                self.data = ((ctypes.c_double * self.width) * self.height)()
            elif self.data_format == HEDSDTFMT_INT_U8:
                self.data = ((ctypes.c_uint8 * self.width) * self.height)()
            elif self.data_format == HEDSDTFMT_INT_RGB24:
                self.data = ((heds_rgb24 * self.width) * self.height)()
            elif self.data_format == HEDSDTFMT_INT_RGB24:
                self.data = ((heds_rgba32 * self.width) * self.height)()

            self.c_data_ptr = self.data


