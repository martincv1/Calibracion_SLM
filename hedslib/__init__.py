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


from ctypes import *
import os
import sys
import math

# Stores if the current Python version is 3 or higher
isPython3 = sys.version_info[0] == 3

# Stores if NumPy could be found.
supportNumPy = True

try:
    import numpy
except:
    supportNumPy = False


if isPython3:
    sys.path.append(os.path.dirname(__file__))
from heds_types import *
from data_conversion import *

if isPython3:
    del sys.path[-1]

# Usage of this library:
#  - Copy this file into your python project directory
#  - import library using
# import hedslib
#  - create an instance:
# "holoeye_slmdisplaysdk_library_instance = hedslib.holoeye_slmdisplaysdk_library(path_to_dll)"
#
#  - call functions by using the definitions in this class:
# "holoeye_slmdisplaysdk_librarylib.function_name(arguments)"
#    In this case, normal python data types can be used, but some library function may not be implemented in this class.
#
#  - call any functions HOLOEYE_APIed by the DLL (see header file):
# "holoeye_slmdisplaysdk_library_instance.lib.function_name(arguments)"
#    When using this general form, please note that all arguments need to have the c data types defined by ctypes.
#    E. g. "c_double", c_char_p("string".encode("utf-8")), ...
#    If using functions like this, you need to import ctypes also in your calling application to have access to these types.


## This class provides access to the dynamic link library (DLL) of the SDK, which defines the
## Library API in ANSI C language, and implements the full feature set of SLM Display SDK.
## If available, you may want to use the Convenience API instead. Library API functions
## can be found in the namespace HEDS.SDK.libapi, which is an object of this class to access all
## the member functions.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class holoeye_slmdisplaysdk_library:
    lib = None
    def __init__(self, path):
        cwd = os.getcwd()  # save current working directory
        full_lib_path_name = os.path.abspath(path)
        lib_folder = os.path.dirname(full_lib_path_name)
        os.chdir(lib_folder)  # we need to change to the directory of the lib (DLL) so that it can find its dependency dll files.

        try:
            self.lib = cdll.LoadLibrary(full_lib_path_name)
            # print("LoadLibrary(holoeye_slmconfigsdk) returned: ", self.lib)
        except BaseException as e:
            raise RuntimeError("Failed to initialize library from \"" + full_lib_path_name + "\".\nSystem error message: " + str(e))

        os.chdir(cwd)  # undo the change of the current working directory

        self.lib.heds_dataformat_size.restype = c_uint
        self.lib.heds_dataformat_string.restype = c_char_p
        self.lib.heds_datahandle_state_string.restype = c_char_p
        self.lib.heds_dataflags_string.restype = c_char_p
        self.lib.heds_zernike_param_name.restype = c_char_p
        self.lib.heds_zernike_param_funcstr.restype = c_char_p
        self.lib.heds_requires_version.restype = c_int
        self.lib.heds_config_api.restype = c_int
        self.lib.heds_error_string.restype = c_char_p
        self.lib.heds_datahandles_show.restype = c_int
        self.lib.heds_datahandles_release.restype = c_int
        self.lib.heds_datahandles_release_all.restype = c_int
        self.lib.heds_time_now.restype = c_ulonglong
        self.lib.heds_time_duration_ms.restype = c_double
        self.lib.heds_time_wait_ms.restype = c_double
        self.lib.heds_info_version_string.restype = c_char_p
        self.lib.heds_info_version_major.restype = c_int
        self.lib.heds_info_version_minor.restype = c_int
        self.lib.heds_info_version_hotfix.restype = c_int
        self.lib.heds_info_version_revision.restype = c_int
        self.lib.heds_info_monitor_count.restype = c_int
        self.lib.heds_info_monitor_get_id_primary.restype = c_int
        self.lib.heds_info_monitor_get_id_secondary.restype = c_int
        self.lib.heds_info_monitor_get_id_used_slm.restype = c_int
        self.lib.heds_info_monitor_get_geometry.restype = c_int
        self.lib.heds_info_monitor_get_framerate.restype = c_float
        self.lib.heds_info_monitor_get_name.restype = c_char_p
        self.lib.heds_datahandle_read_internal_data.restype = c_int
        self.lib.heds_datahandle_apply_changes.restype = c_int
        self.lib.heds_datahandle_set_showflags.restype = c_int
        self.lib.heds_datahandle_get_showflags.restype = c_int
        self.lib.heds_datahandle_set_duration.restype = c_int
        self.lib.heds_datahandle_get_duration.restype = c_int
        self.lib.heds_datahandle_set_beammanipulation.restype = c_int
        self.lib.heds_datahandle_get_beammanipulation.restype = c_int
        self.lib.heds_datahandle_set_transform_scale.restype = c_int
        self.lib.heds_datahandle_get_transform_scale.restype = c_int
        self.lib.heds_datahandle_set_transform_shift.restype = c_int
        self.lib.heds_datahandle_get_transform_shift.restype = c_int
        self.lib.heds_datahandle_set_gamma.restype = c_int
        self.lib.heds_datahandle_get_gamma.restype = c_int
        self.lib.heds_datahandle_set_value_offset.restype = c_int
        self.lib.heds_datahandle_get_value_offset.restype = c_int
        self.lib.heds_datahandle_get_data_properties.restype = c_int
        self.lib.heds_datahandle_get_errorcode.restype = c_int
        self.lib.heds_datahandle_get_state.restype = c_int
        self.lib.heds_datahandle_get_state_duration_ms.restype = c_int
        self.lib.heds_datahandle_waitfor_state.restype = c_int
        self.lib.heds_datahandle_beam_steer_to_angle_rad.restype = c_float
        self.lib.heds_datahandle_beam_steer_to_angle_deg.restype = c_float
        self.lib.heds_datahandle_beam_steer_from_angle_rad.restype = c_float
        self.lib.heds_datahandle_beam_steer_from_angle_deg.restype = c_float
        self.lib.heds_datahandle_beam_lens_to_focal_length_mm.restype = c_float
        self.lib.heds_datahandle_beam_lens_from_focal_length_mm.restype = c_float
        self.lib.heds_slmwindow_open.restype = c_int
        self.lib.heds_slmwindow_isopen.restype = c_int
        self.lib.heds_slmwindow_close.restype = c_int
        self.lib.heds_slmwindow_wait.restype = c_int
        self.lib.heds_slmwindow_slmsetup_clear.restype = c_int
        self.lib.heds_slmwindow_slmsetup_count.restype = c_uint
        self.lib.heds_slmwindow_slmsetup_add_screen.restype = c_int
        self.lib.heds_slmwindow_slmsetup_apply.restype = c_int
        self.lib.heds_slmwindow_slmsetup_apply_changes.restype = c_int
        self.lib.heds_slmwindow_device_layout.restype = c_int
        self.lib.heds_slmwindow_size_px.restype = c_int
        self.lib.heds_slmwindow_pixelsize_um.restype = c_float
        self.lib.heds_slmwindow_refreshrate_hz.restype = c_float
        self.lib.heds_slmwindow_wavefrontcompensation_load_from_file.restype = c_int
        self.lib.heds_slmwindow_wavefrontcompensation_clear.restype = c_int
        self.lib.heds_slmwindow_get_image_width.restype = c_uint
        self.lib.heds_slmwindow_get_image_height.restype = c_uint
        self.lib.heds_slmwindow_get_image_data.restype = c_int
        self.lib.heds_slmpreview_open.restype = c_int
        self.lib.heds_slmpreview_close.restype = c_int
        self.lib.heds_slmpreview_isopen.restype = c_int
        self.lib.heds_slmpreview_set_settings.restype = c_int
        self.lib.heds_slmpreview_get_settings.restype = c_int
        self.lib.heds_slmpreview_move.restype = c_int
        self.lib.heds_slmpreview_get_geometry.restype = c_int
        self.lib.heds_slm_set_geometry.restype = c_int
        self.lib.heds_slm_get_geometry.restype = c_int
        self.lib.heds_slm_set_wavelength.restype = c_int
        self.lib.heds_slm_get_wavelength.restype = c_int
        self.lib.heds_slm_set_modulation.restype = c_int
        self.lib.heds_slm_get_modulation.restype = c_int
        self.lib.heds_slm_set_chromatic_abberation_factor.restype = c_int
        self.lib.heds_slm_get_chromatic_abberation_factor.restype = c_int
        self.lib.heds_slm_set_calibration_factor.restype = c_int
        self.lib.heds_slm_get_calibration_factor.restype = c_int
        self.lib.heds_slm_zernike_load_paramfile.restype = c_int
        self.lib.heds_slm_zernike_set_parameters.restype = c_int
        self.lib.heds_slm_wavefront_compensation_enable.restype = c_int
        self.lib.heds_slm_load_blankscreen.restype = c_int
        self.lib.heds_slm_load_dividedscreen_vertical.restype = c_int
        self.lib.heds_slm_load_dividedscreen_horizontal.restype = c_int
        self.lib.heds_slm_load_grating_binary_vertical.restype = c_int
        self.lib.heds_slm_load_grating_binary_horizontal.restype = c_int
        self.lib.heds_slm_load_grating_blaze_vertical.restype = c_int
        self.lib.heds_slm_load_grating_blaze_horizontal.restype = c_int
        self.lib.heds_slm_load_phasefunction_axicon.restype = c_int
        self.lib.heds_slm_load_phasefunction_lens.restype = c_int
        self.lib.heds_slm_load_phasefunction_vortex.restype = c_int
        self.lib.heds_slm_load_imagedata.restype = c_int
        self.lib.heds_slm_load_phasedata.restype = c_int
        self.lib.heds_slm_load_imagedata_from_file.restype = c_int
        self.lib.heds_slm_load_phasedata_from_file.restype = c_int
        self.lib.heds_slm_show_blankscreen.restype = c_int
        self.lib.heds_slm_show_dividedscreen_vertical.restype = c_int
        self.lib.heds_slm_show_dividedscreen_horizontal.restype = c_int
        self.lib.heds_slm_show_grating_binary_vertical.restype = c_int
        self.lib.heds_slm_show_grating_binary_horizontal.restype = c_int
        self.lib.heds_slm_show_grating_blaze_vertical.restype = c_int
        self.lib.heds_slm_show_grating_blaze_horizontal.restype = c_int
        self.lib.heds_slm_show_phasefunction_axicon.restype = c_int
        self.lib.heds_slm_show_phasefunction_lens.restype = c_int
        self.lib.heds_slm_show_phasefunction_vortex.restype = c_int
        self.lib.heds_slm_show_imagedata.restype = c_int
        self.lib.heds_slm_show_phasedata.restype = c_int
        self.lib.heds_slm_show_imagedata_from_file.restype = c_int
        self.lib.heds_slm_show_phasedata_from_file.restype = c_int

        self.lib.heds_dataformat_size.argtypes = (c_uint,)
        self.lib.heds_dataformat_string.argtypes = (c_uint, c_uint,)
        self.lib.heds_datahandle_state_string.argtypes = (c_uint, c_uint,)
        self.lib.heds_dataflags_string.argtypes = (c_uint, c_uint,)
        self.lib.heds_zernike_param_name.argtypes = (c_uint, c_uint,)
        self.lib.heds_zernike_param_funcstr.argtypes = (c_uint, c_uint,)
        self.lib.heds_requires_version.argtypes = (c_int, c_int, c_int,)
        self.lib.heds_config_api.argtypes = (c_int, c_char_p, c_uint,)
        self.lib.heds_error_string.argtypes = (c_int, c_uint,)
        self.lib.heds_datahandles_show.argtypes = (c_void_p, c_uint,)
        self.lib.heds_datahandles_release.argtypes = (c_void_p, c_uint,)
        self.lib.heds_datahandles_release_all.argtypes = (c_uint,)
        self.lib.heds_free_internal_string_memory.argtypes = (c_void_p,)
        self.lib.heds_time_duration_ms.argtypes = (c_ulonglong, c_ulonglong,)
        self.lib.heds_time_wait_ms.argtypes = (c_double,)
        self.lib.heds_info_version_string.argtypes = (c_uint,)
        self.lib.heds_info_monitor_get_id_used_slm.argtypes = (c_uint,)
        self.lib.heds_info_monitor_get_geometry.argtypes = (c_int, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int),)
        self.lib.heds_info_monitor_get_framerate.argtypes = (c_int,)
        self.lib.heds_info_monitor_get_name.argtypes = (c_int, c_uint,)
        self.lib.heds_datahandle_read_internal_data.argtypes = (c_void_p,)
        self.lib.heds_datahandle_apply_changes.argtypes = (c_void_p,)
        self.lib.heds_datahandle_set_showflags.argtypes = (c_void_p, c_uint,)
        self.lib.heds_datahandle_get_showflags.argtypes = (c_void_p, POINTER(c_uint),)
        self.lib.heds_datahandle_set_duration.argtypes = (c_void_p, c_uint,)
        self.lib.heds_datahandle_get_duration.argtypes = (c_void_p, POINTER(c_uint),)
        self.lib.heds_datahandle_set_beammanipulation.argtypes = (c_void_p, c_float, c_float, c_float,)
        self.lib.heds_datahandle_get_beammanipulation.argtypes = (c_void_p, POINTER(c_float), POINTER(c_float), POINTER(c_float),)
        self.lib.heds_datahandle_set_transform_scale.argtypes = (c_void_p, c_float,)
        self.lib.heds_datahandle_get_transform_scale.argtypes = (c_void_p, POINTER(c_float),)
        self.lib.heds_datahandle_set_transform_shift.argtypes = (c_void_p, c_int, c_int,)
        self.lib.heds_datahandle_get_transform_shift.argtypes = (c_void_p, POINTER(c_int), POINTER(c_int),)
        self.lib.heds_datahandle_set_gamma.argtypes = (c_void_p, c_float,)
        self.lib.heds_datahandle_get_gamma.argtypes = (c_void_p, POINTER(c_float),)
        self.lib.heds_datahandle_set_value_offset.argtypes = (c_void_p, c_void_p, c_uint,)
        self.lib.heds_datahandle_get_value_offset.argtypes = (c_void_p, c_void_p, c_uint,)
        self.lib.heds_datahandle_get_data_properties.argtypes = (c_void_p, POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_float), POINTER(c_uint),)
        self.lib.heds_datahandle_get_errorcode.argtypes = (c_void_p, POINTER(c_int),)
        self.lib.heds_datahandle_get_state.argtypes = (c_void_p, POINTER(c_uint),)
        self.lib.heds_datahandle_get_state_duration_ms.argtypes = (c_void_p, c_uint, POINTER(c_int), POINTER(c_int),)
        self.lib.heds_datahandle_waitfor_state.argtypes = (c_void_p, c_uint,)
        self.lib.heds_datahandle_beam_steer_to_angle_rad.argtypes = (c_float, c_float, c_float,)
        self.lib.heds_datahandle_beam_steer_to_angle_deg.argtypes = (c_float, c_float, c_float,)
        self.lib.heds_datahandle_beam_steer_from_angle_rad.argtypes = (c_float, c_float, c_float,)
        self.lib.heds_datahandle_beam_steer_from_angle_deg.argtypes = (c_float, c_float, c_float,)
        self.lib.heds_datahandle_beam_lens_to_focal_length_mm.argtypes = (c_int, c_float, c_float, c_float,)
        self.lib.heds_datahandle_beam_lens_from_focal_length_mm.argtypes = (c_int, c_float, c_float, c_float,)
        self.lib.heds_slmwindow_open.argtypes = (POINTER(c_uint), c_char_p, c_uint,)
        self.lib.heds_slmwindow_isopen.argtypes = (c_uint, c_int,)
        self.lib.heds_slmwindow_close.argtypes = (c_uint,)
        self.lib.heds_slmwindow_wait.argtypes = (c_uint, c_int,)
        self.lib.heds_slmwindow_slmsetup_clear.argtypes = (c_uint,)
        self.lib.heds_slmwindow_slmsetup_count.argtypes = (c_uint,)
        self.lib.heds_slmwindow_slmsetup_add_screen.argtypes = (c_uint, c_uint, c_uint, c_uint, c_uint,)
        self.lib.heds_slmwindow_slmsetup_apply.argtypes = (c_uint, c_void_p,)
        self.lib.heds_slmwindow_slmsetup_apply_changes.argtypes = (c_uint,)
        self.lib.heds_slmwindow_device_layout.argtypes = (c_uint, POINTER(c_uint), POINTER(c_uint),)
        self.lib.heds_slmwindow_size_px.argtypes = (c_uint, POINTER(c_uint), POINTER(c_uint),)
        self.lib.heds_slmwindow_pixelsize_um.argtypes = (c_uint,)
        self.lib.heds_slmwindow_refreshrate_hz.argtypes = (c_uint,)
        self.lib.heds_slmwindow_wavefrontcompensation_load_from_file.argtypes = (c_uint, c_char_p, c_uint, c_int, c_int, c_int, c_int, c_int, c_int,)
        self.lib.heds_slmwindow_wavefrontcompensation_clear.argtypes = (c_uint, c_int, c_int,)
        self.lib.heds_slmwindow_get_image_width.argtypes = (c_uint,)
        self.lib.heds_slmwindow_get_image_height.argtypes = (c_uint,)
        self.lib.heds_slmwindow_get_image_data.argtypes = (c_uint, c_void_p, c_uint, c_uint, c_uint,)
        self.lib.heds_slmpreview_open.argtypes = (c_uint,)
        self.lib.heds_slmpreview_close.argtypes = (c_uint,)
        self.lib.heds_slmpreview_isopen.argtypes = (c_uint,)
        self.lib.heds_slmpreview_set_settings.argtypes = (c_uint, c_uint, c_float,)
        self.lib.heds_slmpreview_get_settings.argtypes = (c_uint, POINTER(c_uint), POINTER(c_float),)
        self.lib.heds_slmpreview_move.argtypes = (c_uint, c_int, c_int, c_int, c_int,)
        self.lib.heds_slmpreview_get_geometry.argtypes = (c_uint, POINTER(c_int), POINTER(c_int), POINTER(c_int), POINTER(c_int),)
        self.lib.heds_slm_set_geometry.argtypes = (c_void_p, c_uint, c_uint, c_uint, c_uint, c_int,)
        self.lib.heds_slm_get_geometry.argtypes = (c_void_p, POINTER(c_uint), POINTER(c_uint), POINTER(c_uint), POINTER(c_uint),)
        self.lib.heds_slm_set_wavelength.argtypes = (c_void_p, c_void_p, c_uint, c_int,)
        self.lib.heds_slm_get_wavelength.argtypes = (c_void_p, POINTER(c_float), c_ubyte,)
        self.lib.heds_slm_set_modulation.argtypes = (c_void_p, c_ubyte, c_int,)
        self.lib.heds_slm_get_modulation.argtypes = (c_void_p, POINTER(c_ubyte),)
        self.lib.heds_slm_set_chromatic_abberation_factor.argtypes = (c_void_p, c_float, c_ubyte, c_int,)
        self.lib.heds_slm_get_chromatic_abberation_factor.argtypes = (c_void_p, POINTER(c_float), c_ubyte,)
        self.lib.heds_slm_set_calibration_factor.argtypes = (c_void_p, c_float, c_int,)
        self.lib.heds_slm_get_calibration_factor.argtypes = (c_void_p, POINTER(c_float),)
        self.lib.heds_slm_zernike_load_paramfile.argtypes = (c_void_p, c_void_p, POINTER(c_int), c_char_p, c_uint,)
        self.lib.heds_slm_zernike_set_parameters.argtypes = (c_void_p, c_void_p, c_int, c_ubyte,)
        self.lib.heds_slm_wavefront_compensation_enable.argtypes = (c_void_p, c_int, c_int,)
        self.lib.heds_slm_load_blankscreen.argtypes = (c_void_p, c_void_p, c_void_p, c_uint,)
        self.lib.heds_slm_load_dividedscreen_vertical.argtypes = (c_void_p, c_void_p, c_void_p, c_void_p, c_uint, c_float, c_int,)
        self.lib.heds_slm_load_dividedscreen_horizontal.argtypes = (c_void_p, c_void_p, c_void_p, c_void_p, c_uint, c_float, c_int,)
        self.lib.heds_slm_load_grating_binary_vertical.argtypes = (c_void_p, c_void_p, c_int, c_int, c_void_p, c_void_p, c_uint, c_int,)
        self.lib.heds_slm_load_grating_binary_horizontal.argtypes = (c_void_p, c_void_p, c_int, c_int, c_void_p, c_void_p, c_uint, c_int,)
        self.lib.heds_slm_load_grating_blaze_vertical.argtypes = (c_void_p, c_void_p, c_int, c_int,)
        self.lib.heds_slm_load_grating_blaze_horizontal.argtypes = (c_void_p, c_void_p, c_int, c_int,)
        self.lib.heds_slm_load_phasefunction_axicon.argtypes = (c_void_p, c_void_p, c_int, c_int, c_int,)
        self.lib.heds_slm_load_phasefunction_lens.argtypes = (c_void_p, c_void_p, c_int, c_int, c_int,)
        self.lib.heds_slm_load_phasefunction_vortex.argtypes = (c_void_p, c_void_p, c_int, c_int, c_int, c_int,)
        self.lib.heds_slm_load_imagedata.argtypes = (c_void_p, c_void_p, c_int, c_int, c_void_p, c_uint, c_uint, c_int,)
        self.lib.heds_slm_load_phasedata.argtypes = (c_void_p, c_void_p, c_int, c_int, c_void_p, c_uint, c_uint, c_int, c_float,)
        self.lib.heds_slm_load_imagedata_from_file.argtypes = (c_void_p, c_void_p, c_char_p, c_uint, c_uint,)
        self.lib.heds_slm_load_phasedata_from_file.argtypes = (c_void_p, c_void_p, c_char_p, c_uint, c_uint,)
        self.lib.heds_slm_show_blankscreen.argtypes = (c_void_p, c_void_p, c_uint,)
        self.lib.heds_slm_show_dividedscreen_vertical.argtypes = (c_void_p, c_void_p, c_void_p, c_uint, c_float, c_int,)
        self.lib.heds_slm_show_dividedscreen_horizontal.argtypes = (c_void_p, c_void_p, c_void_p, c_uint, c_float, c_int,)
        self.lib.heds_slm_show_grating_binary_vertical.argtypes = (c_void_p, c_int, c_int, c_void_p, c_void_p, c_uint, c_int,)
        self.lib.heds_slm_show_grating_binary_horizontal.argtypes = (c_void_p, c_int, c_int, c_void_p, c_void_p, c_uint, c_int,)
        self.lib.heds_slm_show_grating_blaze_vertical.argtypes = (c_void_p, c_int, c_int,)
        self.lib.heds_slm_show_grating_blaze_horizontal.argtypes = (c_void_p, c_int, c_int,)
        self.lib.heds_slm_show_phasefunction_axicon.argtypes = (c_void_p, c_int, c_int, c_int,)
        self.lib.heds_slm_show_phasefunction_lens.argtypes = (c_void_p, c_int, c_int, c_int,)
        self.lib.heds_slm_show_phasefunction_vortex.argtypes = (c_void_p, c_int, c_int, c_int, c_int,)
        self.lib.heds_slm_show_imagedata.argtypes = (c_void_p, c_int, c_int, c_void_p, c_uint, c_uint, c_int,)
        self.lib.heds_slm_show_phasedata.argtypes = (c_void_p, c_int, c_int, c_void_p, c_uint, c_uint, c_int, c_float,)
        self.lib.heds_slm_show_imagedata_from_file.argtypes = (c_void_p, c_char_p, c_uint, c_uint,)
        self.lib.heds_slm_show_phasedata_from_file.argtypes = (c_void_p, c_char_p, c_uint, c_uint,)


    ## Returns the size in bytes the given \p dataformat will allocate in memory per pixel.
    ## \param dataformat The data format to retrieve the memory size for.
    ## \return dataformat_size: Returns the size of the given data format in bytes. Returns 0 in case of an invalid data format.
    def heds_dataformat_size(self, dataformat):
        dataformat_size = int(self.lib.heds_dataformat_size(dataformat))
        return dataformat_size

    ## Returns a string constant containing the data format name.
    ## \param datafmt The data format to retrieve the type name string for.
    ## \return dataformat_string: Returns a pointer to a string constant containing the data format name.
    def heds_dataformat_string(self, datafmt):
        dataformat_string = self.lib.heds_dataformat_string(datafmt, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return dataformat_string

    ## Returns a string constant containing the data handle state name for the enum.
    ## \param state The state to retrieve the type name string for.
    ## \return datahandle_state_string: Returns a pointer to a string constant containing the data format name.
    def heds_datahandle_state_string(self, state):
        datahandle_state_string = self.lib.heds_datahandle_state_string(state, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return datahandle_state_string

    ## Returns a string constant containing all the enabled flags.
    ## \param dataflags The flags to retrieve the string for.
    ## \return dataflags_string: Returns a pointer to a string constant containing the enabled flags in \p dataflags.
    def heds_dataflags_string(self, dataflags):
        dataflags_string = self.lib.heds_dataflags_string(dataflags, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return dataflags_string

    ## Returns a string constant naming the given Zernike parameter index.
    ## \param zernike_param The Zernike parameter index to retrieve the name for.
    ## \return zernike_param_name: Returns a pointer to a string constant containing the name of the Zernika parameter index \p zernike_param.
    def heds_zernike_param_name(self, zernike_param):
        zernike_param_name = self.lib.heds_zernike_param_name(zernike_param, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return zernike_param_name

    ## Returns a string constant containing the polynom of the given Zernike parameter index.
    ## \param zernike_param The Zernike parameter index to retrieve the function string for.
    ## \return zernike_param_funcstr: Returns a pointer to a string constant containing the enabled flags in \p dataflags.
    def heds_zernike_param_funcstr(self, zernike_param):
        zernike_param_funcstr = self.lib.heds_zernike_param_funcstr(zernike_param, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return zernike_param_funcstr

    ## Checks the API version compatibility and returns HOLOEYE_FALSE in case this SDK version is not API compatible with the requested version.
    ## Please add this function into your programs at the beginning and request the API version you write your program with.
    ## The version format is major.minor.hotfix.revision, and optionally some additions. API compatibility is maintained through major versions,
    ## like defined by semantic versioning, see https://semver.org/.
    ## \param major The major version number of the used SDK version.
    ## \param minor The minor version number of the used SDK version.
    ## \param show_message_box If set to HOLOEYE_TRUE, a message box will open when the used SDK version is incompatible with the requested version.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_requires_version(self, major, minor, show_message_box=True):
        errorcode = int(self.lib.heds_requires_version(major, minor, show_message_box))
        return errorcode

    ## This function provides information about the used environment to this SDK. The information is used in this SDK
    ## when check for updates dialog is used and provides useful information in the tray icon opened by created instances.
    ## Instead of calling this function directly, please use the function heds_sdk_init() or similar, provided by each convenience API implementation
    ## differently. This way, the API configuration information is created automatically for the used API.
    ## \param api_index An index specifying the programming language software package used to access HOLOEYE SLM Display SDK.
    ## \param api_name The name and version of the programming language software package. Must be a non-empty string.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_config_api(self, api_index, api_name):
        errorcode = int(self.lib.heds_config_api(api_index, c_char_p(str(api_name).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8)))
        return errorcode

    ## Returns the corresponding error string for a given error code in the requested format.
    ## \param error The error code to get the error string for.
    ## \return error_string: The string describing the error case.
    def heds_error_string(self, error):
        error_string = self.lib.heds_error_string(error, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return error_string

    ## Shows a list of data handles on their individual SLM screen simultaneously.
    ## The function blocks the current thread until all given data handles are in visible state.
    ## This may require already visible data handles on the same SLM screens to reach their duration_in_frames setting,
    ## before the given data handles can become visible.
    ## Each data handle provides its own show flags, which are either set during data load or later
    ## using \ref heds_datahandle_set_showflags (&datahandle_id, showflags) function.
    ## \param datahandle_ids A pointer to an array of heds_datahandle_id objects to be shown on their SLM screens.
    ##                       The input data must be a ctypes array.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandles_show(self, datahandle_ids):
        datahandle_ids_size = 0
        if isinstance(datahandle_ids, ctypes.Array):
            datahandle_ids_size = len(datahandle_ids)

        if datahandle_ids_size <= 0:
            return HEDSERR_InvalidArgument

        errorcode = int(self.lib.heds_datahandles_show(pointer(datahandle_ids), c_uint(datahandle_ids_size)))
        return errorcode

    ## Releases all internal data (including data on GPU memory) for the given data handles.
    ## Does not free up memory of the given heds_datahandle_id array content.
    ## To release all data handles, please refer to \ref heds_datahandles_release_all().
    ## \param datahandle_ids A pointer to an array of heds_datahandle_id objects.
    ##                       The input data must be a ctypes array.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandles_release(self, datahandle_ids):
        datahandle_ids_size = 0
        if isinstance(datahandle_ids, ctypes.Array):
            datahandle_ids_size = len(datahandle_ids)

        if datahandle_ids_size <= 0:
            return HEDSERR_InvalidArgument

        errorcode = int(self.lib.heds_datahandles_release(pointer(datahandle_ids), c_uint(datahandle_ids_size)))
        return errorcode

    ## Releases all internal data (including data on GPU memory) for all handles uploaded into the given SLM window.
    ## Does not free up memory of the given heds_datahandle_id array content.
    ## \param slmwindow_id The SLM window ID to release all handles for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandles_release_all(self, slmwindow_id):
        errorcode = int(self.lib.heds_datahandles_release_all(slmwindow_id))
        return errorcode

    ## This function frees up internally allocated string memory. Please call after calling a function returning a string constant to make
    ## sure there is no memory leak. This function is thread-safe. Is not needed on all returned strings, but does not hurt to be called on all
    ## returned string data pointers.
    ## \param string_data_ptr The pointer returned by the called function. It does not matter which format the string was returned in.
    def heds_free_internal_string_memory(self, string_data_ptr):
        self.lib.heds_free_internal_string_memory(string_data_ptr)


    ## Closes everything, i.e. closes all open SLM windows including tray icons etc., and cleans up
    ## everything except for the development environment configuration, see \ref heds_sdk_init() and \ref heds_config_api().
    def heds_close(self):
        self.lib.heds_close()


    ## Get a precise time point in platform dependent unit. Please use \ref heds_time_duration_ms()
    ## to measure a duration between two time points.
    ## Is meant to be used in languages with less accurate time measurement implementations.
    ## \return time_now: An arbitrary unsigned 64-bit integer value representing the current time.
    def heds_time_now(self):
        time_now = int(self.lib.heds_time_now())
        return time_now

    ## Get the duration between two calls to \ref heds_time_now() in floating point milliseconds to not loose microsendond precision, if available.
    ## \param t2 The end time point of the duration to be measured. Must be in unit returned by \ref heds_time_now().
    ## \param t1 The start time point of the duration to be measured. Must be in unit returned by \ref heds_time_now().
    ## \return time_duration_ms: The duration between both time points in floating point milliseconds.
    def heds_time_duration_ms(self, t2, t1):
        time_duration_ms = float(self.lib.heds_time_duration_ms(t2, t1))
        return time_duration_ms

    ## A precise waiting function compared to heds_slmwindow_wait() function. Compared to the SLM window wait functions,
    ## this function will block the current thread with full load on one CPU core while waiting.
    ## Uses \ref heds_time_now() and \ref heds_time_duration_ms() functions to measure the time internally.
    ## It is recommended to use this function for short but precise durations, like below 100 ms.
    ## In case of waiting for longer periods, there is the function \ref heds_slmwindow_wait(), which will stop
    ## waiting in case the process is closed in between.
    ## \param min_wait_dur_ms The duration to block the current thread for in floating point milliseconds.
    ##                        This duration is the minimum executation duration of this function. There is no guaranty
    ##                        the operating system will allow this function to return at the end of the period, but typically
    ##                        it returns within a few microseconds after the period has passed. Please check the return value
    ##                        for the actual execution time.
    ## \return time_wait_ms: The actual measured executation duration of this function call in floating point milliseconds.
    def heds_time_wait_ms(self, min_wait_dur_ms):
        time_wait_ms = float(self.lib.heds_time_wait_ms(min_wait_dur_ms))
        return time_wait_ms

    ## Provides the version of the SDK as a string.
    ## \return info_version_string: The version string.
    def heds_info_version_string(self):
        info_version_string = self.lib.heds_info_version_string(c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return info_version_string

    ## Provides the major version of the SDK.
    ## The version format is major.minor.hotfix.revision.
    ## \return info_version_major: The major number of the version.
    def heds_info_version_major(self):
        info_version_major = int(self.lib.heds_info_version_major())
        return info_version_major

    ## Provides the minor version of the SDK.
    ## The version format is major.minor.hotfix.revision.
    ## \return info_version_minor: The minor number of the version.
    def heds_info_version_minor(self):
        info_version_minor = int(self.lib.heds_info_version_minor())
        return info_version_minor

    ## Provides the hotfix version of the SDK.
    ## The version format is major.minor.hotfix.revision.
    ## \return info_version_hotfix: The hotfix number of the version.
    def heds_info_version_hotfix(self):
        info_version_hotfix = int(self.lib.heds_info_version_hotfix())
        return info_version_hotfix

    ## Provides the revision of the SDK.
    ## The version format is major.minor.hotfix.revision.
    ## \return info_version_revision: The revision number of the version.
    def heds_info_version_revision(self):
        info_version_revision = int(self.lib.heds_info_version_revision())
        return info_version_revision

    ## Returns the number of monitor devices found within the operating systems multi-monitor virtual desktop area.
    ## Please note: The function can only return valid values when there is at least one SLMWindow open.
    ## \return info_monitor_count: Returns the number of monitors found in the system, or 0 on any error, e.g. when there is no SLMWindow open.
    def heds_info_monitor_count(self):
        info_monitor_count = int(self.lib.heds_info_monitor_count())
        return info_monitor_count

    ## Returns the monitor ID within the operating systems multi-monitor virtual desktop area for the operating systems primary monitor.
    ## This is useful to be able to place the SLM Preview window or other application windows on the main monitor.
    ## Please note: The function can only return a valid ID when there is at least one SLMWindow open.
    ## \return info_monitor_id_primary: Returns the ID of the primary monitor, or -1 on any error, e.g. when there is no SLMWindow open.
    def heds_info_monitor_get_id_primary(self):
        info_monitor_id_primary = int(self.lib.heds_info_monitor_get_id_primary())
        return info_monitor_id_primary

    ## Returns a monitor ID within the operating systems multi-monitor virtual desktop area for a monitor, which is not the primary and not and an SLM monitor.
    ## This is useful to be able to place the SLM Preview window or other application windows on a secondary monitor except any HOLOEYE SLM monitor.
    ## Please note: The function can only return a valid ID when there is at least one SLMWindow open.
    ## \return info_monitor_id_secondary: Returns the ID of a secondary monitor except for SLMs, or the ID of the primary monitor in case of an error, which may return -1 in case of an error.
    def heds_info_monitor_get_id_secondary(self):
        info_monitor_id_secondary = int(self.lib.heds_info_monitor_get_id_secondary())
        return info_monitor_id_secondary

    ## Returns the monitor ID within the operating systems multi-monitor virtual desktop area for the given SLMWindow \p slmwindow_id.
    ## This function provides the monitor ID needed to call the functions \ref heds_info_monitor_get_geometry(),
    ## \ref heds_info_monitor_get_framerate(), and \ref heds_info_monitor_get_name().
    ## Please note: The function can only return a valid ID when there is at least one SLMWindow open.
    ## \param slmwindow_id The ID of the SLMWindow, which is the user of the returned monitor ID.
    ## \return info_monitor_id_used_slm: Returns the ID of the primary monitor, or -1 on any error, e.g. when the given \p slmwindow_id is not open.
    def heds_info_monitor_get_id_used_slm(self, slmwindow_id):
        info_monitor_id_used_slm = int(self.lib.heds_info_monitor_get_id_used_slm(slmwindow_id))
        return info_monitor_id_used_slm

    ## Retrieves the geometry (position \p x, and \p y, width \p w, and height \p h) of the given \p monitor_id.
    ## If \p monitor_id is less than zero, e.g. -1, the function tries to return the geometry of the primary monitor, which may not be implemented on all platforms.
    ## In the case of missing implementation for negative monitor IDs default geometry, the error code HEDS_NotImplemented is returned.
    ## \param monitor_id The ID of the monitor within the operating system. Must be from 0 to \ref heds_info_monitor_count()-1.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return x: The retrieved position in x direction, i.e. the number of pixel from the multi-monitor virtual desktop area origin to the left edge of the monitor area.
    ## \return y: The retrieved position in y direction, i.e. the number of pixel from the multi-monitor virtual desktop area origin to the top edge of the monitor area.
    ## \return w: The retrieved width of the monitor area in number of pixel.
    ## \return h: The retrieved height of the monitor area in number of pixel.
    def heds_info_monitor_get_geometry(self, monitor_id):
        x = c_int(0)
        y = c_int(0)
        w = c_int(0)
        h = c_int(0)
        errorcode = int(self.lib.heds_info_monitor_get_geometry(monitor_id, pointer(x), pointer(y), pointer(w), pointer(h)))
        return errorcode, x.value, y.value, w.value, h.value

    ## Retrieves the frame rate in Hertz (frames per second) of the given \p monitor_id.
    ## If \p monitor_id is invalid, e.g. -1, the function returns 0.0f.
    ## \param monitor_id The ID of the monitor within the operating system. Must be from 0 to \ref heds_info_monitor_count()-1.
    ## \return info_monitor_framerate: The frame rate of the given monitor_id, or 0.0f in case of any error.
    def heds_info_monitor_get_framerate(self, monitor_id):
        info_monitor_framerate = float(self.lib.heds_info_monitor_get_framerate(monitor_id))
        return info_monitor_framerate

    ## Retrieves the frame rate in Hertz (frames per second) of the given \p monitor_id.
    ## If \p monitor_id is invalid, e.g. -1, the function returns an empty string.
    ## \param monitor_id The ID of the monitor within the operating system. Must be from 0 to \ref heds_info_monitor_count()-1.
    ## \return info_monitor_name: The name string of the given monitor_id. Will be an empty string in case of any error.
    def heds_info_monitor_get_name(self, monitor_id):
        info_monitor_name = self.lib.heds_info_monitor_get_name(monitor_id, c_uint(HEDSSTRFMT_UTF8)).decode('utf-8')
        return info_monitor_name

    ## This function transfers internal data handle structure efficiently from renderer. Please call this function before retrieving data
    ## from a data handle, i.e. before using any heds_datahandle_get_...() function.
    ## Please avoid calling this function too often, because it may take some time depending on how SDK is connected to the API.
    ## No need to call this function before applying new values to a data handle.
    ## \param datahandle_id The data handle to update internal data structure for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_read_internal_data(self, datahandle_id):
        errorcode = int(self.lib.heds_datahandle_read_internal_data(pointer(datahandle_id)))
        return errorcode

    ## This function allows to apply multiple changes made to the data handle simultaneously.
    ## After making changes to the data handle, like calling \ref heds_datahandle_set_beammanipulation() on the same \p datahandle_id,
    ## the changes must be applied before being visible on the SLM screen.
    ## If the data it not visible so far, the changes will be applied automatically on the next call to \ref heds_datahandles_show()
    ## for the same \p datahandle_id.
    ## Instead, if the data is already visible and waits for its visible duration to pass, this apply function can still apply the changes
    ## and make them visible as soon as possible, i.e. within the next video output frame.
    ## \param datahandle_id The data handle to apply changes for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_apply_changes(self, datahandle_id):
        errorcode = int(self.lib.heds_datahandle_apply_changes(pointer(datahandle_id)))
        return errorcode

    ## Set new show flags for the data handle.
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The data handle to set show flags for.
    ## \param showflags A bitfield representing presentation and flipping options, see \ref heds_showflags_enum.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_showflags(self, datahandle_id, showflags=HEDSSHF_PresentAutomatic):
        errorcode = int(self.lib.heds_datahandle_set_showflags(pointer(datahandle_id), showflags))
        return errorcode

    ## Get show flags of the data handle.
    ## \param datahandle_id The data handle to get show flags from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return showflags: Returns a bitfield containing presentation and flipping options, see \ref heds_showflags_enum.
    def heds_datahandle_get_showflags(self, datahandle_id):
        showflags = c_uint(0)
        errorcode = int(self.lib.heds_datahandle_get_showflags(pointer(datahandle_id), pointer(showflags)))
        return errorcode, showflags.value

    ## Request a visible during given in number of video output frames of the SLM display device. For example, if the SLM is addressed at
    ## 60 Hz frame rate (60 frames per second) through HDMI or any other video signal, a duration of one would request a visible duration
    ## of about 16.67 ms for this data, until the next data can be made visible. If no other data is shown after this \p datahandle_id,
    ## this data handle will stay visible for an unlimited period, until either the SDK is closed or other data is shown on the same SLM screen.
    ## The maximum duration in frames supported here is defined by HEDS_DATAHANDLE_MAX_DURATION (255).
    ## Please note: If the data handle is currently visible on SLM screen, the change can be applied immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The data handle to set a duration request for.
    ## \param duration_in_frames The number of video signal frames this data should be visible when shown within a sequence of show data handle calls. Default is 1, maximum is defined by HEDS_DATAHANDLE_MAX_DURATION (255).
    ## \return errorcode: HEDSERR_NoError when there is no error.
    def heds_datahandle_set_duration(self, datahandle_id, duration_in_frames=1):
        errorcode = int(self.lib.heds_datahandle_set_duration(pointer(datahandle_id), duration_in_frames))
        return errorcode

    ## Get the currently set duration in video signal frames property of the data handle.
    ## \param datahandle_id The data handle to get the currently set visible duration request from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return duration_in_frames: Returns the number of video signal frames this data should be visible when shown within a sequence of show data handle calls.
    def heds_datahandle_get_duration(self, datahandle_id):
        duration_in_frames = c_uint(0)
        errorcode = int(self.lib.heds_datahandle_get_duration(pointer(datahandle_id), pointer(duration_in_frames)))
        return errorcode, duration_in_frames.value

    ## Apply beam manipulation parameters for beam steering and beam focusing to the data.
    ## The beam manipulation parameters are normalized so that a value range from -1.0 to 1.0 addresses meaningful phase pattern in respect to the pixel size.
    ## To calculate these beam manipulation parameters from SI units (focal length in milli meter and angle in degree or radian), please refer to the functions
    ## \see heds_datahandle_beam_steer_from_angle_rad(),
    ## \see heds_datahandle_beam_steer_from_angle_deg(), and
    ## \see heds_datahandle_beam_lens_from_focal_length_mm().
    ## The SLMs pixel size in micro meter can be retrieved using the function \ref heds_slmwindow_pixelsize_um(\p datahandle_id.slmwindow_id).
    ## In case the SLM is set into color operation, please provide the factors for the smallest wavelength used in your color setup, i.e. the blue wavelength.
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The ID of the data handle to apply beam manipulation for.
    ## \param beamSteerX A factor to shift the hologram in x-direction (left and right).
    ## \param beamSteerY A factor to shift the hologram in y-direction (up and down).
    ## \param beamLens A factor to focus the hologram into another z-plane.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_beammanipulation(self, datahandle_id, beamSteerX=0.0, beamSteerY=0.0, beamLens=0.0):
        errorcode = int(self.lib.heds_datahandle_set_beammanipulation(pointer(datahandle_id), beamSteerX, beamSteerY, beamLens))
        return errorcode

    ## Retrieve current beam manipulation parameters for beam steering and beam focusing from the data.
    ## The factors are normalized so that a value range from -1.0 to 1.0 addresses meaningful phase pattern in respect to the pixel size.
    ## To calculate SI units (focal length in milli meter and angle in degree or radian) from the returned factors, please refer to the functions
    ## \see heds_datahandle_beam_steer_to_angle_rad(),
    ## \see heds_datahandle_beam_steer_to_angle_deg(), and
    ## \see heds_datahandle_beam_lens_to_focal_length_mm().
    ## The SLMs pixel size in micro meter can be retrieved using the function \ref heds_slmwindow_pixelsize_um(slm_id.slmwindow_id).
    ## In case the SLM is set into color operation, please provide the factors for the smallest wavelength used in your color setup, i.e. the blue wavelength.
    ## \param datahandle_id The ID of the data handle to retrieve beam manipulation for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return beamSteerX: Returns the currently set factor to shift the hologram in x-direction (left and right).
    ## \return beamSteerY: Returns the currently set factor to shift the hologram in y-direction (up and down).
    ## \return beamLens: Returns the currently set factor to focus the hologram into another z-plane.
    def heds_datahandle_get_beammanipulation(self, datahandle_id):
        beamSteerX = c_float(0)
        beamSteerY = c_float(0)
        beamLens = c_float(0)
        errorcode = int(self.lib.heds_datahandle_get_beammanipulation(pointer(datahandle_id), pointer(beamSteerX), pointer(beamSteerY), pointer(beamLens)))
        return errorcode, beamSteerX.value, beamSteerY.value, beamLens.value

    ## Set a transform scale to rescale the shown data handle on screen by the \p scale factor.
    ## Due to the resampling, it is not recommended to use other values except for the default 1.0f when showing phase data fields. This is most useful
    ## when showing image data instead of phase data fields.
    ## This value will be ignored as soon as there is a present show flag set for rescaling, like the fit show flags.
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The ID of the data handle to set transform scale for.
    ## \param scale The new scale factor to apply to the data handle. Default value is 1.0f, which shows data in 1:1 pixel scale, i.e. there is no spatial resampling done by default.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_transform_scale(self, datahandle_id, scale=1.0):
        errorcode = int(self.lib.heds_datahandle_set_transform_scale(pointer(datahandle_id), scale))
        return errorcode

    ## Retrieve the currently set transform scale factor from a data handle.
    ## \param datahandle_id The ID of the data handle to get transform scale from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return scale: Returns the currently set scale factor.
    def heds_datahandle_get_transform_scale(self, datahandle_id):
        scale = c_float(0)
        errorcode = int(self.lib.heds_datahandle_get_transform_scale(pointer(datahandle_id), pointer(scale)))
        return errorcode, scale.value

    ## Set a transform shift to move the shown data handle in x- and y-direction on the SLM screen.
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The ID of the data handle to set transform shifts for.
    ## \param shift_x_px The shift applied in x-direction (horizontal shift) in number of SLM pixel. Positive shift move to the right, and negative shifts to the left side when looking onto the preview screen.
    ## \param shift_y_px The shift applied in y-direction (vertical shift) in number of SLM pixel. Positive shift move to the top, and negative shifts to the bottom when looking onto the preview screen.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_transform_shift(self, datahandle_id, shift_x_px=0, shift_y_px=0):
        errorcode = int(self.lib.heds_datahandle_set_transform_shift(pointer(datahandle_id), shift_x_px, shift_y_px))
        return errorcode

    ## Retrieve the currently applied transform shift values, which move the shown data handle in x- and y-direction on the SLM screen.
    ## \param datahandle_id The ID of the data handle to get transform shifts from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return shift_x_px: Returns the shift applied in x-direction (horizontal shift) in number of SLM pixel. Positive shift move to the right, and negative shifts to the left side when looking onto the preview screen.
    ## \return shift_y_px: Returns the shift applied in y-direction (vertical shift) in number of SLM pixel. Positive shift move to the top, and negative shifts to the bottom when looking onto the preview screen.
    def heds_datahandle_get_transform_shift(self, datahandle_id):
        shift_x_px = c_int(0)
        shift_y_px = c_int(0)
        errorcode = int(self.lib.heds_datahandle_get_transform_shift(pointer(datahandle_id), pointer(shift_x_px), pointer(shift_y_px)))
        return errorcode, shift_x_px.value, shift_y_px.value

    ## Set a gamma factor value for the shown data. The gamma factor manipulates the output gray levels like possible within some image editing software.
    ## The new gray value is calculated from the original gray value like this: gv_out = gv_in ^ (1/gamma).
    ## The effect is that gamma > 1 increases the brightness, and gamma < 1 lowers the brightness of the image.
    ## The default value is 1.0 and does not transform the output gray levels. This is recommended for phase modulation mode.
    ## The SLM can be calibrated using Configuration Manager, instead.
    ## The gamma factor is applied to the output gray levels, not only to the data handles data, but to the whole SLM screen area the data is shown on,
    ## including wavefront compensation etc. .
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The ID of the data handle to set a gamma factor for.
    ## \param gamma The gamma factor to set to the SLM screen area the \p datahandle_id is shown on. Default value is 1.0f for no manipluation.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_gamma(self, datahandle_id, gamma=1.0):
        errorcode = int(self.lib.heds_datahandle_set_gamma(pointer(datahandle_id), gamma))
        return errorcode

    ## Retrieve the currently applied gamma factor. \see heds_datahandle_set_gamma() for more info about the gamma factor.
    ## \param datahandle_id The ID of the data handle to get a gamma factor from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return gamma: Returns the currently applied gamma factor of the \p datahandle_id.
    def heds_datahandle_get_gamma(self, datahandle_id):
        gamma = c_float(0)
        errorcode = int(self.lib.heds_datahandle_get_gamma(pointer(datahandle_id), pointer(gamma)))
        return errorcode, gamma.value

    ## Set a gray value offset for the shown data. The applied gray value offset will be added onto the whole SLM screen area, the \p datahandle_id is shown on,
    ## and the gray values are wrapped around on overflow or underflow. This feature is meant to be used in phase modulation mode, when an 8-bit gray value of 256 shall have
    ## exactly the same phase value like a gray value of 0 due to the periodicity of the phase.
    ## Please note: If the data handle is currently visible on SLM screen, the change can be made visible immediately by calling
    ## \ref heds_datahandle_apply_changes(\p datahandle_id). Otherwise, the change will take effect on the next show event of the
    ## same data handle (\ref heds_datahandles_show(\p datahandle_id)).
    ## \param datahandle_id The ID of the data handle to set the gray value offset for.
    ## \param offset The gray value offset. The value can be given in all supported formats, like float 32/64-bit, integer, and color formats, see \ref heds_dataformat_enum.
    ##               The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##               Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_set_value_offset(self, datahandle_id, offset):
        offset_obj = HoloeyeInputDataDescriptor(offset)

        if offset_obj.error_code != HEDSERR_NoError:
            return offset_obj.error_code
        # data must be 1 x 1:
        if offset_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if offset_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_datahandle_set_value_offset(pointer(datahandle_id), offset_obj.c_data_ptr, c_uint(offset_obj.data_format)))
        return errorcode

    ## Retrieve the currently applied gray value offset. Please provide the format you want to receive the offset value in, and please pass a pointer to the corresponding data object matching the requested format.
    ## \param datahandle_id The ID of the data handle to get the gray value offset from.
    ## \param fmt The data format the offset value is passed in for returning the value. The void pointer \p offset allows passing and returning any data format, please see
    ##            \ref heds_dataformat_enum for supported formats. Please provide the correct format for the passed data pointer to avoid memory access issues.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return offset: The gray value offset. The value can be given in all supported formats, like float 32/64-bit, integer, and color formats, see \ref heds_dataformat_enum.
    ##                 The output data is a numpy array containing data in the given format if numpy is installed,
    ##                 otherwise a ctypes array containing data in the equivilent ctypes data format is returned.
    ##                 Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeOutputDataDescriptor for more info about returned data formats.
    def heds_datahandle_get_value_offset(self, datahandle_id, fmt=HEDSDTFMT_INT_U8):

        offset_obj = HoloeyeOutputDataDescriptor(1, 1, fmt)

        errorcode = int(self.lib.heds_datahandle_get_value_offset(pointer(datahandle_id), offset_obj.c_data_ptr, c_uint(offset_obj.data_format)))
        return errorcode, offset_obj.data  # offset_obj.data is either a numpy array or a ctypes array in case no numpy installation is available.

    ## Retrieve some read-only properties from the data handle abou the uploaded data.
    ## \param datahandle_id The ID of the data handle to get the data properties from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return fmt: Returns the format of the uploaded data, see \ref heds_dataformat_enum.
    ## \return width: Returns the number of columns of the uploaded data field.
    ## \return height: Returns the number of rows of the uploaded data field.
    ## \return pitch: Returns the number of bytes in memory between multiple rows of the uploaded data field.
    ## \return phasewrap: Returns the phasewrap setting of rows of the uploaded data field. This is zero if the data was uploaded as image data instead of phase data.
    ## \return flags: Returns the currently applied load- and show-flags of the data handle.
    def heds_datahandle_get_data_properties(self, datahandle_id):
        fmt = c_uint(0)
        width = c_uint(0)
        height = c_uint(0)
        pitch = c_uint(0)
        phasewrap = c_float(0)
        flags = c_uint(0)
        errorcode = int(self.lib.heds_datahandle_get_data_properties(pointer(datahandle_id), pointer(fmt), pointer(width), pointer(height), pointer(pitch), pointer(phasewrap), pointer(flags)))
        return errorcode, fmt.value, width.value, height.value, pitch.value, phasewrap.value, flags.value

    ## Retrieve the internal error code of the data handle. Some errors are specific for the data object, and these may be returned here.
    ## \param datahandle_id The ID of the data handle to get the internal error code from.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return ec: Returns the internal error code.
    def heds_datahandle_get_errorcode(self, datahandle_id):
        ec = c_int(0)
        errorcode = int(self.lib.heds_datahandle_get_errorcode(pointer(datahandle_id), pointer(ec)))
        return errorcode, ec.value

    ## Retrieve the current processing state of the uploaded data.
    ## \param datahandle_id The ID of the data handle to get the data processing state for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return state: Returns the current state the data is in, \see heds_datahandle_state_enum.
    def heds_datahandle_get_state(self, datahandle_id):
        state = c_uint(0)
        errorcode = int(self.lib.heds_datahandle_get_state(pointer(datahandle_id), pointer(state)))
        return errorcode, state.value

    ## Retrieve the duration in milliseconds for how long a specified \p state was active within the processing pipeline.
    ## \param datahandle_id The ID of the data handle to get the duration for.
    ## \param state The state for which to receive the duration for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return duration_ms: Returns the duration of the specified \p state in milliseconds.
    ## \return was_done: Optionally returns if the state was ever reached so far. Some states may not be executed during the processing pipeline, depending on the uploaded data.
    ##                   If this returns HOLOEYE_FALSE (0), \p duration_ms is 0, so that no special value would return invalid duration values when calculating with or visualizing the returned durations.
    def heds_datahandle_get_state_duration_ms(self, datahandle_id, state):
        duration_ms = c_int(0)
        was_done = c_int(0)
        errorcode = int(self.lib.heds_datahandle_get_state_duration_ms(pointer(datahandle_id), state, pointer(duration_ms), pointer(was_done)))
        return errorcode, duration_ms.value, was_done.value

    ## When calling this function on an existing data handle, the function will block the current thread until the data handle has reached the requested internal processing \p state.
    ## For example, when waiting for the state HEDSDHST_ReadyToRender, the function will return as soon as all internal preparations are done, and the data can be shown using
    ## \ref heds_datahandles_show() immediately, without any delay introduced by internal preparations. However, when uploading data and retrieving the data handle, the load function
    ## will already block the thread and returns when the data is ready to render, i.e. ready to be shown. Therefore, typically there is no need to call this after loading data.
    ## But you can wait for any state defined in \ref heds_datahandle_state_enum.
    ## \param datahandle_id The ID of the data handle to wait for.
    ## \param state The state to wait for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_datahandle_waitfor_state(self, datahandle_id, state=HEDSDHST_ReadyToRender):
        errorcode = int(self.lib.heds_datahandle_waitfor_state(pointer(datahandle_id), state))
        return errorcode

    ## Utilities function for calculating proper values for the beam manipulation parameters in heds_handle.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the beam steer value from the data handle property as an input and calculates the corresponding
    ## steering angle of the incident light in radian.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param beam_steer The parameter passed to the data handle property "beamSteerX" or "beamSteerY". Best optical blaze results are gained for values between -1.0f and 1.0f.
    ## \return angle_rad: Returns the corresponding deviation angle in radian (full circle is 2*pi rad).
    def heds_datahandle_beam_steer_to_angle_rad(self, pixelsize_um, wavelength_nm, beam_steer):
        angle_rad = float(self.lib.heds_datahandle_beam_steer_to_angle_rad(pixelsize_um, wavelength_nm, beam_steer))
        return angle_rad

    ## Utilities function for calculating proper values for the beam manipulation parameters in heds_handle.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the beam steer value from the data handle property as an input and calculates the corresponding
    ## steering angle of the incident light in degree.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param beam_steer The parameter passed to the data handle property "beamSteerX" or "beamSteerY". Best optical blaze results are gained for values between -1.0f and 1.0f.
    ## \return angle_deg: Returns the corresponding deviation angle in degree (full circle is 360 degree).
    def heds_datahandle_beam_steer_to_angle_deg(self, pixelsize_um, wavelength_nm, beam_steer):
        angle_deg = float(self.lib.heds_datahandle_beam_steer_to_angle_deg(pixelsize_um, wavelength_nm, beam_steer))
        return angle_deg

    ## Utilities function for calculating proper values for the beam manipulation parameters in heds_handle.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the desired steering angle of the incident light in radian as an input and calculates the
    ## corresponding beam steer parameter to be passed into data handle. The beam steer parameter is normalized to
    ## meaningful values in the range from -1.0f to +1.0f. The value corresponds to steering from one side of the
    ## unit cell to the other side in the far field of a holographic projection.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param steering_angle_rad Desired steering angle of the incident light in radian (full circle is 2*pi rad).
    ## \return beam_steer: Returns the corresponding beam steer parameter to be passed into data handle. Values in range [-1.0f, 1.0f] are recommended.
    def heds_datahandle_beam_steer_from_angle_rad(self, pixelsize_um, wavelength_nm, steering_angle_rad):
        beam_steer = float(self.lib.heds_datahandle_beam_steer_from_angle_rad(pixelsize_um, wavelength_nm, steering_angle_rad))
        return beam_steer

    ## Utilities function for calculating proper values for the beam manipulation parameters in heds_handle.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the desired steering angle of the incident light in degree as an input and calculates the
    ## corresponding beam steer parameter to be passed into data handle. The beam steer parameter is normalized to
    ## meaningful values in the range from -1.0f to +1.0f. The value corresponds to steering from one side of the
    ## unit cell to the other side in the far field of a holographic projection.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param steering_angle_deg Desired steering angle of the incident light in degree (full circle is 360 degree).
    ## \return beam_steer: Returns the corresponding beam steer parameter to be passed into data handle. Values in range [-1.0f, 1.0f] are recommended.
    def heds_datahandle_beam_steer_from_angle_deg(self, pixelsize_um, wavelength_nm, steering_angle_deg):
        beam_steer = float(self.lib.heds_datahandle_beam_steer_from_angle_deg(pixelsize_um, wavelength_nm, steering_angle_deg))
        return beam_steer

    ## Utilities function for calculating proper values for the beam manipulation parameters in heds_handle.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the beam lens parameter value from the data handle property as an input and calculates
    ## the corresponding focal length of the Fresnel zone lens addressed with the given beam lens parameter.
    ## The beam lens parameter is proportional to the lens power (1/f) and is scaled so that for values in the range
    ## between -1.0f and +1.0f the addressed phase function has no artifacts due to the pixel size of the SLM.
    ## Higher absolute values might still produce valid optical lens results, but the quality of the addressed lens
    ## phase function will degrade with an increasing absolute value above 1.0f.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param slm_width_px The maximum of width and height of the SLM screen the lens should be applied to.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param beam_lens The parameter passed to the data handle property "beamLens". Values in range [-1.0f, 1.0f] are recommended.
    ## \return focal_length_mm: Returns the corresponding focal length of the Fresnel zone lens in SI-unit mm.
    def heds_datahandle_beam_lens_to_focal_length_mm(self, slm_width_px, pixelsize_um, wavelength_nm, beam_lens):
        focal_length_mm = float(self.lib.heds_datahandle_beam_lens_to_focal_length_mm(slm_width_px, pixelsize_um, wavelength_nm, beam_lens))
        return focal_length_mm

    ## Utilities function for calculating proper values for the beam manipulation parameters in data handles.
    ## Please consider applying beam manipulation parameters directly to the handle using physical units, see \ref heds_datahandle_set_beammanipulation().
    ## The function takes the desired folcal length as an input and calculates the corresponding beam lens parameter.
    ## The beam lens parameter is proportional to the lens power (1/f) and is scaled so that for values in the range
    ## between -1.0f and +1.0f the addressed phase function has no artifacts due to the pixel size of the SLM.
    ## Higher absolute values might still produce valid optical lens results, but the quality of the addressed lens
    ## phase function will degrade with an increasing absolute value above 1.0f.
    ## The SLM must be initialized properly in order to return the correct value.
    ## In case of an error due to uninitialized SLM the function returns 0.0f.
    ## Please note: In case of a color-field sequential (CFS) setup with red, green, and blue wavelengths, please use the blue wavelength to calculate the beam steer parameter.
    ## \param slm_width_px The maximum of width and height of the SLM screen the lens should be applied to.
    ## \param pixelsize_um The SLMs pixel size in micrometer. Can be retrieved through SLM screen, see \ref heds_slmwindow_pixelsize_um().
    ## \param wavelength_nm The wavelength of the incident light in SI-unit nanometer. In case of CFS, please provide the blue wavelength.
    ## \param focal_length_mm Desired focal length in SI-unit millimeter.
    ## \return beam_lens: Returns the corresponding "beamLens" parameter to be passed into data handle. Values in range [-1.0f, 1.0f] are recommended.
    def heds_datahandle_beam_lens_from_focal_length_mm(self, slm_width_px, pixelsize_um, wavelength_nm, focal_length_mm):
        beam_lens = float(self.lib.heds_datahandle_beam_lens_from_focal_length_mm(slm_width_px, pixelsize_um, wavelength_nm, focal_length_mm))
        return beam_lens

    ## Opens a new SLM window. If you pass a non-empty pre-selection string, the device will be
    ## selected without any GUI dialogs.
    ## The pre-selection string can contain device property filter(s) to automatically find and select the
    ## device to open the SLM window on.
    ## If the maximum number of concurrent SLM windows is already reached, this call will return the error
    ## code HEDSERR_MaxSLMWindowCountReached.
    ## If a remote host is opened using a preselection string like "connect://127.0.0.1:6230", a connection will be established and
    ## the remotely running process will be told to open its SLM window. The connection will persist until heds_slmwindow_close(slmwindow)
    ## is called. The remote SLM window may stay open depending on the remote server configuration.
    ## \param preselect_device_name An optional string to automatically select a device to open the SLM window on.
    ##                              The string consists of a format "property:value", with properties separated by ";" Valid properties are "index", "name",
    ##                              and "serial". An example would be "name:pluto;serial:0001". In addition, if the string starts with "connect://", a manually
    ##                              started process can be addressed using the format "connect://ipv4:port", e.g. "connect://127.0.0.1:6230".
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return slmwindow_id: Returns the index of the newly opened SLM window.
    def heds_slmwindow_open(self, preselect_device_name=""):
        slmwindow_id = c_uint(0)
        errorcode = int(self.lib.heds_slmwindow_open(pointer(slmwindow_id), c_char_p(str(preselect_device_name).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8)))
        return errorcode, slmwindow_id.value

    ## Checks if the given SLM window is already open. Can check for a response of the connected SLM window.
    ## \param slmwindow_id The SLM window to check.
    ## \param check_response If this is HOLOEYE_FALSE, the function just checks if the SLM window was created initially.
    ##                       Otherwise it will actually transfer data and will wait for a valid response, which will
    ##                       take at least a few milliseconds.
    ## \return slmwindow_isopen: HOLOEYE_TRUE if the window is open and responds, and HOLOEYE_FALSE if it is not open.
    def heds_slmwindow_isopen(self, slmwindow_id, check_response=True):
        slmwindow_isopen = int(self.lib.heds_slmwindow_isopen(slmwindow_id, check_response))
        return slmwindow_isopen

    ## Close the given SLM window. If available, this call will close the SLM preview window and the related tray icon of that SLM window, too.
    ## \param slmwindow_id The index of the SLM window to close.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_close(self, slmwindow_id):
        errorcode = int(self.lib.heds_slmwindow_close(slmwindow_id))
        return errorcode

    ## Blocks the current thread and waits until the given duration has passed. If given duration is zero (default), it will wait forever.
    ## The function checks if the SLM window is closed (e.g. through tray icon) during the wait.
    ## Therefore, by default, a duration of zero will wait until the given SLM window is closed, either manually or due to an error.
    ## \param slmwindow_id The ID of the SLM Window to check during the wait duration.
    ## \param duration_ms The number of milliseconds to wait before returning for sure. By default (0),
    ##                    the function waits forever until the given SLM window was closed.
    ## \return errorcode: HEDSERR_NoError when either the SLM was closed or the desired wait duration was reached.
    def heds_slmwindow_wait(self, slmwindow_id, duration_ms=0):
        errorcode = int(self.lib.heds_slmwindow_wait(slmwindow_id, duration_ms))
        return errorcode

    ## Remove all existing SLM geometry definitions from the SLM window, so that a new SLM setup can be defined from scratch.
    ## \param slmwindow_id The SLM window ID to clear the SLM setup for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_slmsetup_clear(self, slmwindow_id):
        errorcode = int(self.lib.heds_slmwindow_slmsetup_clear(slmwindow_id))
        return errorcode

    ## Returns the number of all geometry definitions already added. This can be used to reserve memory for the
    ## SLM structs in \ref heds_slmwindow_slmsetup_apply().
    ## \param slmwindow_id The ID of the SLM window to retrieve the count of all added SLMs in its SLM setup.
    ## \return slmwindow_slmsetup_count: The number of SLMs waiting for set up.
    def heds_slmwindow_slmsetup_count(self, slmwindow_id):
        slmwindow_slmsetup_count = int(self.lib.heds_slmwindow_slmsetup_count(slmwindow_id))
        return slmwindow_slmsetup_count

    ## SLM setup function to create SLM screens on the SLM window area during initialization of the SLM window.
    ## Adds a geometry description for an SLM screen area to be applied with \ref heds_slmwindow_slmsetup_apply().
    ## The position is measured within SLM window in SLM pixel, and (0, 0) means at the top left edge of SLM window.
    ## When passing a size of 0 (default), the SLM screen geometry is automatically extended to fill the window.
    ## If the new area overlaps with another SLM screen area already defined, an error is returned.
    ## \param slmwindow_id The index of the SLM window to add an SLM into.
    ## \param pos_left_px The x coordinate of the left top edge of the new SLM screen area in pixel.
    ## \param pos_top_px The y coordinate of the left top edge of the new SLM screen area in pixel.
    ## \param width_px The width of the new SLM screen area in pixel.
    ## \param height_px The height of the new SLM screen area in pixel.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_slmsetup_add_screen(self, slmwindow_id, pos_left_px=0, pos_top_px=0, width_px=0, height_px=0):
        errorcode = int(self.lib.heds_slmwindow_slmsetup_add_screen(slmwindow_id, pos_left_px, pos_top_px, width_px, height_px))
        return errorcode

    ## Applies the SLM setup created by calls of \ref heds_slmwindow_slmsetup_add_screen().
    ## This function must be called before SLMs can be used. Therefore this function returns the actually created SLMs (\p slm)
    ## in the same order of the calls to \ref heds_slmwindow_slmsetup_add_screen().
    ## If \ref heds_slmwindow_slmsetup_add_screen() was never called, an error is returned.
    ## \param slmwindow_id The index of the SLM window to add an SLM into.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return slm_id_list: A pointer to a list of heds_slm_id structs. The memory must be allocated to fit all returned SLM screen IDs into, i.e. all added screens since last clear of SLM setup.
    ##                      The output data is a ctypes array.
    def heds_slmwindow_slmsetup_apply(self, slmwindow_id):
        slm_id_list_count = self.heds_slmwindow_slmsetup_count(slmwindow_id)
        slm_id_list = (heds_slm_id * slm_id_list_count)()  # reserve memory for returning ctypes array.
        errorcode = int(self.lib.heds_slmwindow_slmsetup_apply(slmwindow_id, pointer(slm_id_list)))
        return errorcode, slm_id_list

    ## The purpose of this function is to apply multiple SLM screen area changes (like geometry, wavelength, calibration, etc.) in one call to speed
    ## up apply of changes to multiple canvases. The SLM setup done by adding screens is not affected by calling this function, and the SLM IDs will not change.
    ## \param slmwindow_id The index of the SLM window, which shall apply all property changes to already existing SLM screen areas.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_slmsetup_apply_changes(self, slmwindow_id):
        errorcode = int(self.lib.heds_slmwindow_slmsetup_apply_changes(slmwindow_id))
        return errorcode

    ## Returns the number of hardware SLM devices the SLM window was opened on.
    ## The devices may be set up in a layout with a number of columns and/or rows.
    ## Normally the returned layout is 1x1, except if an NVIDIA Mosaic screen was configured and selected for the SLM window in \ref heds_slmwindow_open().
    ## \param slmwindow_id The SLM window to retrieve the SLM device list for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return columns: Number of columns the device layout has. This is the number of devices merged together in x-direction,
    ##                  i.e. beneeth each other in respect to the operating systems monitor layout.
    ## \return rows: Number of rows the device layout has. This is the number of devices merged together in y-direction,
    ##               i.e. on top of each other in respect to the operating systems monitor layout.
    def heds_slmwindow_device_layout(self, slmwindow_id):
        columns = c_uint(0)
        rows = c_uint(0)
        errorcode = int(self.lib.heds_slmwindow_device_layout(slmwindow_id, pointer(columns), pointer(rows)))
        return errorcode, columns.value, rows.value

    ## Provides the width and height of the connected SLM device in number of pixels.
    ## \param slmwindow_id The ID of the SLM Window to retrieve the size for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return width_px: Returns the width of the SLM Window in pixel.
    ## \return height_px: Returns the height of the SLM Window in pixel.
    def heds_slmwindow_size_px(self, slmwindow_id):
        width_px = c_uint(0)
        height_px = c_uint(0)
        errorcode = int(self.lib.heds_slmwindow_size_px(slmwindow_id, pointer(width_px), pointer(height_px)))
        return errorcode, width_px.value, height_px.value

    ## Provides the pixel size/pitch of the connected SLM hardware device(s). The unit of the returned pixel size is micro-meter.
    ## If the SLM window is spread over multiple hardware SLMs, all hardware SLMs will have the same pixel size for sure.
    ## \param slmwindow_id The ID of the SLM Window to retrieve the pixel size for.
    ## \return slmwindow_pixelsize_um: The SLM's pixelsize in micro meter. Returns zero when the SLM window was not opened yet.
    def heds_slmwindow_pixelsize_um(self, slmwindow_id):
        slmwindow_pixelsize_um = float(self.lib.heds_slmwindow_pixelsize_um(slmwindow_id))
        return slmwindow_pixelsize_um

    ## Provides the refresh rate of the connected device. The unit of the returned refresh rate is the derived SI unit Hz.
    ## \param slmwindow_id The ID of the SLM Window to retrieve the refresh rate for.
    ## \return slmwindow_refreshrate_hz: The SLM's current refreshrate. Returns zero when the SLM window was not opened yet.
    def heds_slmwindow_refreshrate_hz(self, slmwindow_id):
        slmwindow_refreshrate_hz = float(self.lib.heds_slmwindow_refreshrate_hz(slmwindow_id))
        return slmwindow_refreshrate_hz

    ## Loads a wavefront compensation from a *.h5 file provided by HOLOEYE and applies it to the given device area within the SLM window.
    ## The wavelength for converting optical path differences into phase shifts is taken from the given SLM screen properties,
    ## \see heds_slm_set_wavelength_nm(), and \see heds_slm_set_modulation(), so the wavefront compensation can only be applied to regions
    ## where an SLM is defined in, \see heds_slmwindow_slmsetup_apply(), and the wavelength is set so that the SLM is in phase shift mode.
    ## \param slmwindow_id The SLM window to load the wavefront into.
    ## \param filename The wavefront compensation H5 file to load.
    ## \param dev_col_idx The column index of the hardware device behind the SLM window if there are multiple hardware devices merged into one operating system screen. Not working yet. WFC is always applied to full SLM window atm.
    ## \param dev_row_idx The row index of the hardware device behind the SLM window if there are multiple hardware devices merged into one operating system screen. Not working yet. WFC is always applied to full SLM window atm.
    ## \param flip_x Flip the wavefront compensation field in x direction, i.e. flip left/right.
    ## \param flip_y Flip the wavefront compensation field in y direction, i.e. flip top/bottom.
    ## \param shift_x Shift the wavefront compensation field in x direction.
    ## \param shift_y Shift the wavefront compensation field in y direction.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_wavefrontcompensation_load_from_file(self, slmwindow_id, filename, dev_col_idx=0, dev_row_idx=0, flip_x=False, flip_y=False, shift_x=0, shift_y=0):
        errorcode = int(self.lib.heds_slmwindow_wavefrontcompensation_load_from_file(slmwindow_id, c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8), dev_col_idx, dev_row_idx, flip_x, flip_y, shift_x, shift_y))
        return errorcode

    ## Clears a previously loaded wavefront compensation for a given device area.
    ## \param slmwindow_id The SLM window to load the wavefront into.
    ## \param dev_col_idx The column index of the hardware device behind the SLM window if there are multiple hardware devices merged into one operating system screen. Not working yet. It always clears the WFC from the full SLM window atm.
    ## \param dev_row_idx The row index of the hardware device behind the SLM window if there are multiple hardware devices merged into one operating system screen. Not working yet. It always clears the WFC from the full SLM window atm.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmwindow_wavefrontcompensation_clear(self, slmwindow_id, dev_col_idx=0, dev_row_idx=0):
        errorcode = int(self.lib.heds_slmwindow_wavefrontcompensation_clear(slmwindow_id, dev_col_idx, dev_row_idx))
        return errorcode

    ## Returns the required data width in pixel of the preview image returned by \ref heds_slmwindow_get_image_data().
    ## \param slmwindow_id The SLM window to retrieve the image from.
    ## \return slmwindow_image_width: Required data size in pixel.
    def heds_slmwindow_get_image_width(self, slmwindow_id):
        slmwindow_image_width = int(self.lib.heds_slmwindow_get_image_width(slmwindow_id))
        return slmwindow_image_width

    ## Returns the required data width in pixel of the preview image returned by \ref heds_slmwindow_get_image_data().
    ## \param slmwindow_id The SLM window to retrieve the image from.
    ## \return slmwindow_image_height: Required data size in pixel.
    def heds_slmwindow_get_image_height(self, slmwindow_id):
        slmwindow_image_height = int(self.lib.heds_slmwindow_get_image_height(slmwindow_id))
        return slmwindow_image_height

    ## Writes the currently retrieved preview image data in RGB format captured from the screen into given \p image_data pointers memory.
    ## Please allocate enough memory and use \ref heds_slmwindow_get_image_height() * \p pitch to allocate the needed amount.
    ## \p pitch needs to be calculated as \ref heds_slmwindow_get_image_width() * \ref heds_dataformat_size(\p image_data_fmt) using the data type size.
    ## Native image format without needing to convert data is RGB 24-bit. Requesting floating point formats would result in an error message.
    ## \param slmwindow_id The SLM window to retrieve the image from.
    ## \param image_data_fmt The requested format of the captured image.
    ##                       If a monochrome format is requested, R, G, and B channels are merged together.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return image_data: A pointer to pre-allocated memory into which SLM Display SDK can copy the retrieved image data.
    ##                     The format is defined by \p image_data_fmt.
    ##                     The output data is a numpy array containing data in the given format if numpy is installed,
    ##                     otherwise a ctypes array containing data in the equivilent ctypes data format is returned.
    ##                     Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeOutputDataDescriptor for more info about returned data formats.
    def heds_slmwindow_get_image_data(self, slmwindow_id, image_data_fmt=HEDSDTFMT_INT_RGB24):
        image_data_w = int(self.lib.heds_slmwindow_get_image_width(slmwindow_id))
        image_data_h = int(self.lib.heds_slmwindow_get_image_height(slmwindow_id))

        image_data_obj = HoloeyeOutputDataDescriptor(image_data_w, image_data_h, image_data_fmt)

        errorcode = int(self.lib.heds_slmwindow_get_image_data(slmwindow_id, image_data_obj.c_data_ptr, c_uint(image_data_obj.data_format), c_uint(image_data_obj.pitch), HEDSMEMLO_C))
        return errorcode, image_data_obj.data  # image_data_obj.data is either a numpy array or a ctypes array in case no numpy installation is available.

    ## Open the SLM preview window. SLM window must be initialized before opening the corresponding SLM preview window.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmpreview_open(self, slmwindow_id):
        errorcode = int(self.lib.heds_slmpreview_open(slmwindow_id))
        return errorcode

    ## Open the SLM preview window. SLM window must be initialized.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmpreview_close(self, slmwindow_id):
        errorcode = int(self.lib.heds_slmpreview_close(slmwindow_id))
        return errorcode

    ## Check if the SLM preview window is open. SLM window must be initialized.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \return slmpreview_isopen: HOLOEYE_TRUE if SLM preview is open for the given SLM window, and HOLOEYE_FALSE if the preview is closed or if there is an error with \p slmwindow.
    def heds_slmpreview_isopen(self, slmwindow_id):
        slmpreview_isopen = int(self.lib.heds_slmpreview_isopen(slmwindow_id))
        return slmpreview_isopen

    ## Sets settings flags and the zoom factor of the preview window.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \param flags The preview flags to set. Refer to \ref heds_slmpreviewflags_enum for details.
    ## \param zoom The zoom factor of the preview window. Use zero to make the data fit the screen.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmpreview_set_settings(self, slmwindow_id, flags=HEDSSLMPF_None, zoom=1.0):
        errorcode = int(self.lib.heds_slmpreview_set_settings(slmwindow_id, flags, zoom))
        return errorcode

    ## Gets settings flags and the zoom factor of the preview window.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return flags: The preview flags to set. Refer to \ref heds_slmpreviewflags_enum for details.
    ## \return zoom: The zoom factor of the preview window. Use zero to make the data fit the screen.
    def heds_slmpreview_get_settings(self, slmwindow_id):
        flags = c_uint(0)
        zoom = c_float(0)
        errorcode = int(self.lib.heds_slmpreview_get_settings(slmwindow_id, pointer(flags), pointer(zoom)))
        return errorcode, flags.value, zoom.value

    ## Changes the position and size of the preview window.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \param pos_x The horizontal position of the window on the desktop.
    ## \param pos_y The vertical position of the window on the desktop.
    ## \param width The width of the window. If \p width or \p height is zero, the size will not be changed.
    ## \param height The height of the window. If \p width or \p height is zero, the size will not be changed.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slmpreview_move(self, slmwindow_id, pos_x, pos_y, width=0, height=0):
        errorcode = int(self.lib.heds_slmpreview_move(slmwindow_id, pos_x, pos_y, width, height))
        return errorcode

    ## Changes the position and size of the preview window.
    ## \param slmwindow_id The SLM window to access the SLM preview window of.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return pos_x: The horizontal position of the window on the desktop.
    ## \return pos_y: The vertical position of the window on the desktop.
    ## \return width: The width of the window. If \p width or \p height is zero, the size will not be changed.
    ## \return height: The height of the window. If \p width or \p height is zero, the size will not be changed.
    def heds_slmpreview_get_geometry(self, slmwindow_id):
        pos_x = c_int(0)
        pos_y = c_int(0)
        width = c_int(0)
        height = c_int(0)
        errorcode = int(self.lib.heds_slmpreview_get_geometry(slmwindow_id, pointer(pos_x), pointer(pos_y), pointer(width), pointer(height)))
        return errorcode, pos_x.value, pos_y.value, width.value, height.value

    ## Allows moving and/or resizing the SLM screen area geometry within the SLM window after it was created already. The geometry must be within the
    ## SLM window and must not overlap with another SLM screen area already defined. In case \p direct_apply is false, the error check for the geometry overlaps
    ## is done later when applying all together using \ref heds_slmwindow_slmsetup_apply_changes().
    ## \param slm_id The SLM screen area object to retrieve the geometry for.
    ## \param pos_x_px Returns the number of pixel from the left edge of the SLM window to the SLM screen area start pixel in x direction.
    ## \param pos_y_px Returns the number of pixel from the top edge of the SLM window to the SLM screen area start pixel in y direction.
    ## \param width_px Returns the number of pixel for the width of the SLM screen area.
    ## \param height_px Returns the number of pixel for the height of the SLM screen area.
    ## \param direct_apply If true, new geometry is applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_set_geometry(self, slm_id, pos_x_px, pos_y_px, width_px, height_px, direct_apply=True):
        errorcode = int(self.lib.heds_slm_set_geometry(pointer(slm_id), pos_x_px, pos_y_px, width_px, height_px, direct_apply))
        return errorcode

    ## Returns position and size of SLM screen area within its SLM window in pixel.
    ## Given parameters can be null to omit them.
    ## \param slm_id The SLM screen area object to retrieve the geometry for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return pos_x_px: Returns the number of pixel from the left edge of the SLM window to the SLM screen area start pixel in x direction.
    ## \return pos_y_px: Returns the number of pixel from the top edge of the SLM window to the SLM screen area start pixel in y direction.
    ## \return width_px: Returns the number of pixel for the width of the SLM screen area.
    ## \return height_px: Returns the number of pixel for the height of the SLM screen area.
    def heds_slm_get_geometry(self, slm_id):
        pos_x_px = c_uint(0)
        pos_y_px = c_uint(0)
        width_px = c_uint(0)
        height_px = c_uint(0)
        errorcode = int(self.lib.heds_slm_get_geometry(pointer(slm_id), pointer(pos_x_px), pointer(pos_y_px), pointer(width_px), pointer(height_px)))
        return errorcode, pos_x_px.value, pos_y_px.value, width_px.value, height_px.value

    ## Sets incident laser beam wavelength(s) for an SLM screen area. Please provide a list of wavelengths with either one (monochrome)
    ## or three (RGB color) elements. In case of three wavelengths, the color channel indices in the list are according to \ref heds_color_channel_enum values.
    ## The wavelength only makes sense in phase modulation mode, therefore when calling this function, the given SLM is set
    ## to phase modulation. This allows using multiple features like Zernike, beam manipulation overlays, and wavefrontcompensation,
    ## which are only possible when the wavelength settings are available.
    ## If zero wavelengths are provided, the SLM is set into intensity modulation mode.
    ## If wavelength_count is not 0, 1, or 3, an error code is returned.
    ## \param slm_id The SLM screen area object to set the wavelength(s) for.
    ## \param wavelengths_nm A pointer to either one or three floating point values storing the wavelengths in SI unit nano-meter.
    ##                       The input data must be a ctypes array.
    ## \param direct_apply If true, new wavelength values are applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_set_wavelength(self, slm_id, wavelengths_nm=None, direct_apply=True):
        wavelengths_nm_size = 0
        if isinstance(wavelengths_nm, ctypes.Array):
            wavelengths_nm_size = len(wavelengths_nm)

        if wavelengths_nm is None:
            # this is an ugly workaround to be able to pass a pointer instead of a null pointer (size is set to 0 anyway):
            wavelengths_nm = (ctypes.c_float * 1)()

        errorcode = int(self.lib.heds_slm_set_wavelength(pointer(slm_id), pointer(wavelengths_nm), c_uint(wavelengths_nm_size), direct_apply))
        return errorcode

    ## Returns the wavelength settings for an SLM screen area set earlier through \ref heds_slm_set_wavelength().
    ## Returns 0.0f in case any error occurs, i.e. when either the SLM (\p slm_id) does not exist or the \p color_channel is out of range.
    ## The \p color_channel needs to be 0 for the monochrome/red, 1 for the green, or 2 for the blue wavelength setting.
    ## \param slm_id The SLM screen area object to retrieve the wavelength for.
    ## \param color_channel The color channel to retrieve the wavelength for. By default HEDSCC_Mono will return either the monochrome or red wavelength. \see heds_color_channel_enum for applicable values.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return wavelength_nm: Returns the wavelength in namo meter for the selected color channel.
    def heds_slm_get_wavelength(self, slm_id, color_channel=HEDSCC_Mono):
        wavelength_nm = c_float(0)
        errorcode = int(self.lib.heds_slm_get_wavelength(pointer(slm_id), pointer(wavelength_nm), color_channel))
        return errorcode, wavelength_nm.value

    ## Sets the modulation type for the SLM screen area. Please have in mind that in phase modulation mode, wavelength setting is needed, too.
    ## Therefore, if that SLM screen area has not got any wavelength setting yet, please use \ref heds_slm_set_wavelength() instead to switch
    ## into \ref HEDSSLMMOD_Phase modulation mode. If the wavelength setting would be missing, an error code HEDSERR_InvalidAPIUsage is returned
    ## and the modulation is set into phase modulation without a wavelength setting, which limits the feature set but allows the phase modulation
    ## features, which does not require a wavelength setting.
    ## \param slm_id The SLM screen area object to get the modulation type for.
    ## \param modulation The modulation type. Please use the enum integer values to differentiate between the types.
    ## \param direct_apply If true, new modulation values are applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_set_modulation(self, slm_id, modulation, direct_apply=True):
        errorcode = int(self.lib.heds_slm_set_modulation(pointer(slm_id), modulation, direct_apply))
        return errorcode

    ## Returns the modulation type the SLM currently is in.
    ## \param slm_id The SLM screen area object to get the modulation type for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return modulation: Return the currently set modulation mode, \see heds_slm_modulation_enum.
    def heds_slm_get_modulation(self, slm_id):
        modulation = c_ubyte(0)
        errorcode = int(self.lib.heds_slm_get_modulation(pointer(slm_id), pointer(modulation)))
        return errorcode, modulation.value

    ## This factor allows to compensate for transverse (lateral) chromatic abberations within the optical setup when using color field sequential mode on the
    ## SLM screen area. By default, beam manipulation (\see heds_datahandle_set_beam_manipulation()) and hologram calculation use the wavelengths set for the
    ## SLM screen area to compute different phase fields for each color channel. In case the optical setup introduces chromatic abberations, the wavelengths
    ## alone would not result in best overlap of the three colored holograms. Therefore, this factor allows to multiply the wavelengths with this factor for
    ## each color channel separately, but only for diffraction angle dependent features like beam manipulation and hologram calculation.
    ## In monochrome operation, this factor is not needed typically.
    ## \param slm_id The SLM screen area ID to apply a chromatic abberation factor to.
    ## \param abberation_factor The chromatic abberation factor to apply.
    ## \param cc The color channel to apply the factor to.
    ## \param direct_apply If true, new calibration factor value is applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_set_chromatic_abberation_factor(self, slm_id, abberation_factor=1.0, cc=HEDSCC_Mono, direct_apply=True):
        errorcode = int(self.lib.heds_slm_set_chromatic_abberation_factor(pointer(slm_id), abberation_factor, cc, direct_apply))
        return errorcode

    ## Returns the currently set chromatic abberation factor for the given color channel.
    ## \see heds_slm_set_chromatic_abberation_factor().
    ## \param slm_id The SLM screen area ID to retrieve the chromatic abberation factor for.
    ## \param color_channel The color channel to retrieve the factor for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return abberation_factor: Returns the chromatic abberation factor.
    def heds_slm_get_chromatic_abberation_factor(self, slm_id, color_channel):
        abberation_factor = c_float(0)
        errorcode = int(self.lib.heds_slm_get_chromatic_abberation_factor(pointer(slm_id), pointer(abberation_factor), color_channel))
        return errorcode, abberation_factor.value

    ## Sets a phase shift calibration factor for an SLM screen area. Please provide the factor in the range 0.0 to 1.0. Values outside this range are cropped
    ## into the range and result in an error code returned by this function.
    ## A factor of 1.0 leads to default rendering behavoir of the output image data using all available gray levels (typically 0 to 255 for 8-bit addressed SLMs).
    ## A factor of 1.0 assumes that the SLM is calibrated for the used laser wavelength to a phase shift of 2.0 pi radian.
    ## By lowering the factor, the renderer adapts to an SLM screen area with an acutually higher phase shift value at maximum gray level,
    ## and reduces the shown phase values (0-2pi rad) by that factor.
    ## Please calibrate your SLM so that you can use the maximum calibration factor on each hardware SLM display device.
    ## This factor is intended to be used when multiple SLM screen areas are used with different wavelengths on a single hardware SLM display,
    ## and the hardware SLM calibration is done for the longest wavelength. The other SLM screen areas using a shorter wavelength can then be
    ## re-calibrated by reducing the gray level range using this factor.
    ## SLM screen areas set to the modulation type HEDSMOD_Intensity ignore this factor.
    ## After calling this function on an SLM screen, HEDSMOD_Phase is enabled automatically.
    ## \param slm_id The SLM screen area object to set the \p calibration_factor for.
    ## \param calibration_factor A factor to reduce output graylevel values for that SLM screen area. Default is 1.0. Cannot be larger than 1.0 since the output gray level range is limited (typically to 0-255).
    ## \param direct_apply If true, new calibration factor value is applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_set_calibration_factor(self, slm_id, calibration_factor=1.0, direct_apply=True):
        errorcode = int(self.lib.heds_slm_set_calibration_factor(pointer(slm_id), calibration_factor, direct_apply))
        return errorcode

    ## Returns the calibration factor for an SLM screen area set earlier through \ref heds_slm_set_calibration_factor().
    ## \param slm_id The SLM screen area object to set the wavelength(s) for.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return calibration_factor: Returns the calibration factor.
    def heds_slm_get_calibration_factor(self, slm_id):
        calibration_factor = c_float(0)
        errorcode = int(self.lib.heds_slm_get_calibration_factor(pointer(slm_id), pointer(calibration_factor)))
        return errorcode, calibration_factor.value

    ## Loads Zernike parameters from a HOLOEYE Zernike parameter file, for example saved by HOLOEYE SLM Pattern Generator.
    ## The loaded Zernike parameters are returned in \p zernike_params, as long as they fit into given memory indicated with input value into \p n_params.
    ## \param slm_id The SLM screen area object to load Zernike parameters for. This parameter is needed for technical reasons.
    ## \param filename The Zernike parameter filename to load.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return zernike_params: Returns a list of Zernike parameters found in the file. Please pre-allocate enough memory to fit all possible parameters (n_max = \ref HEDSZER_COUNT).
    ##                         The output data is a ctypes array.
    def heds_slm_zernike_load_paramfile(self, slm_id, filename):
        zernike_params_count = HEDSZER_COUNT
        zernike_params = (ctypes.c_float * zernike_params_count)()  # reserve memory for returning ctypes array.
        zernike_params_size = 0
        if isinstance(zernike_params, ctypes.Array):
            zernike_params_size = len(zernike_params)

        if zernike_params_size <= 0:
            return HEDSERR_InvalidArgument

        zernike_params_size = c_int(zernike_params_size)

        errorcode = int(self.lib.heds_slm_zernike_load_paramfile(pointer(slm_id), pointer(zernike_params), pointer(zernike_params_size), c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8)))
        return errorcode, zernike_params

    ## Sets Zernike overlay parameters for the SLM. The first value (\p zernike_params[0]) determines the Zernike radius in milli-meter.
    ## The SLM screen area must be in phase modulation mode. Otherwise, set Zernike parameters are ignored until SLM is set into phase modulation mode.
    ## \param slm_id The SLM screen area object to apply Zernike parameters to.
    ## \param zernike_params An array of Zernike values. Refer to \ref heds_zernikevalues_enum for more details. Set to zero or nullptr to disable Zernike overlay.
    ##                       The input data must be a ctypes array.
    ## \param color_channel The color channel(s) to load the parameter set for. By default, HEDSCC_Mono applies the parameter set to all color channels. \see heds_color_channel_enum.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_zernike_set_parameters(self, slm_id, zernike_params, color_channel=HEDSCC_Mono):
        zernike_params_size = 0
        if isinstance(zernike_params, ctypes.Array):
            zernike_params_size = len(zernike_params)

        if zernike_params_size <= 0:
            return HEDSERR_InvalidArgument

        errorcode = int(self.lib.heds_slm_zernike_set_parameters(pointer(slm_id), pointer(zernike_params), c_int(zernike_params_size), color_channel))
        return errorcode

    ## This function allows to disable wavefront compensation overlay for the given SLM screen area ID only. That means, if you load a
    ## wavefront compensation file for the SLM window, while you have defined multiple SLMs on that window, you can switch the wavefront
    ## compensation overlay on and off for each SLM screen area independently.
    ## To load the wavefront compensation field, please refer to \ref heds_slmwindow_wavefrontcompensation_load_from_file().
    ## \param slm_id The SLM screen area object to enable or disable wavefront compensation overlay on.
    ## \param enable If true, the wavefront compensation overlay is applied on the SLM, and if false, it is not applied.
    ## \param direct_apply If true, new geometry is applied immediately to the SLM screen area.
    ##                     If false, new value needs to be applied manually by calling
    ##                     \ref heds_slmwindow_slmsetup_apply_changes(slm_id.slmwindow_id).
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_wavefront_compensation_enable(self, slm_id, enable=True, direct_apply=True):
        errorcode = int(self.lib.heds_slm_wavefront_compensation_enable(pointer(slm_id), enable, direct_apply))
        return errorcode

    ## Loads a blank screen with a constant value into a data handle. The value can either be a phase value, a gray or color
    ## value, and can be provided in all supported formats, depending on the data format provided through \p value_fmt. Whether
    ## the provided data is interpreted as phase value or as image data depends on the settings of the provided SLM screen \p slm.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param value The color value which is addressed to the full SLM.
    ##              The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##              Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_blankscreen(self, slm_id, value):
        datahandle_id = heds_datahandle_id()
        value_obj = HoloeyeInputDataDescriptor(value)

        if value_obj.error_code != HEDSERR_NoError:
            return value_obj.error_code
        # data must be 1 x 1:
        if value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_blankscreen(pointer(slm_id), pointer(datahandle_id), value_obj.c_data_ptr, c_uint(value_obj.data_format)))
        return errorcode, datahandle_id

    ## Loads data to show two areas on the SLM with two different color values. The function is intended to be used for phase
    ## measurements of the SLM in which one half of the SLM can be used as a reference to the other half. The screen will be
    ## split along the vertical (y) axis. This means that the values a and b are painted to the left and right side of the SLM, resp.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param a_value The color value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default: 0]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The color value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default: 255]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param screen_divider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default: 0.5]
    ## \param flipped If set to true, the first side will addressed with \p b_value and the second side will be set to a_value. [default: false]
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_dividedscreen_vertical(self, slm_id, a_value, b_value, screen_divider=0.5, flipped=False):
        datahandle_id = heds_datahandle_id()
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_dividedscreen_vertical(pointer(slm_id), pointer(datahandle_id), a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), screen_divider, flipped))
        return errorcode, datahandle_id

    ## Loads data to show two areas on the SLM with two different color values. The function is intended to be used for phase measurements of the SLM in which one half of the SLM can be used as a reference to the other half.
    ## The screen will be split along the horizontal (x) axis. This means that the color values a and b are painted to the upper and lower side of the SLM, resp.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param a_value The color value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default: 0]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The color value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default: 255]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param screen_divider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default: 0.5]
    ## \param flipped If set to true, the first side will addressed with \p b_value and the second side will be set to a_value. [default: false]
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_dividedscreen_horizontal(self, slm_id, a_value, b_value, screen_divider=0.5, flipped=False):
        datahandle_id = heds_datahandle_id()
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_dividedscreen_horizontal(pointer(slm_id), pointer(datahandle_id), a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), screen_divider, flipped))
        return errorcode, datahandle_id

    ## Loads data to show a vertical binary grating. The grating consists of two values \p a_value and \p b_value, which will be
    ## addressed to the SLM pixel. The width of each area with the value \p a_value and \p b_value is defined by \p a_width and
    ## \p b_width, respectively. Each pair of values is repeated so that the SLM screen is completely filled.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param a_width The width of the first pixel block with the value of \p a_value. This parameter is mandatory.
    ## \param b_width The width of the second pixel block with the value of \p b_value. This parameter is mandatory.
    ## \param a_value The addressed value of the first pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The addressed value of the second pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param shift_x The horizontal offset applied to both pixel blocks. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_grating_binary_vertical(self, slm_id, a_width, b_width, a_value, b_value, shift_x=0):
        datahandle_id = heds_datahandle_id()
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_grating_binary_vertical(pointer(slm_id), pointer(datahandle_id), a_width, b_width, a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), shift_x))
        return errorcode, datahandle_id

    ## Loads data to show a horizontal binary grating. The grating consists of two values \p a_value and \p b_value, which will be
    ## addressed to the SLM pixel. The width of each area with the value \p a_value and \p b_value is defined by \p a_width and
    ## \p b_width, respectively. Each pair of values is repeated so that the SLM screen is completely filled.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param a_width The width of the first pixel block with the value of \p a_value. This parameter is mandatory.
    ## \param b_width The width of the second pixel block with the value of \p b_value. This parameter is mandatory.
    ## \param a_value The addressed value of the first pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The addressed value of the second pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param shift_y The vertical offset applied to both pixel blocks. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_grating_binary_horizontal(self, slm_id, a_width, b_width, a_value, b_value, shift_y=0):
        datahandle_id = heds_datahandle_id()
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_grating_binary_horizontal(pointer(slm_id), pointer(datahandle_id), a_width, b_width, a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), shift_y))
        return errorcode, datahandle_id

    ## Loads data to show a vertical blazed grating on the SLM.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param grating_period The grating period in SLM pixel. The value is mandatory. Can be either positive or negative for an inverted grating profile. Please note that the phase can also be inverted by the \p phase_scale. If both values are negative, the invertions will superimpose to non invertion.
    ## \param shift_x The horizontal offset applied to the grating in pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_grating_blaze_vertical(self, slm_id, grating_period, shift_x=0):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_grating_blaze_vertical(pointer(slm_id), pointer(datahandle_id), grating_period, shift_x))
        return errorcode, datahandle_id

    ## Loads data to show a horizontal blazed grating on the SLM.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param grating_period The grating period in SLM pixel. The value is mandatory. Can be either positive or negative for an inverted grating profile.
    ## \param shift_y The vertical offset applied to the grating. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_grating_blaze_horizontal(self, slm_id, grating_period, shift_y=0):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_grating_blaze_horizontal(pointer(slm_id), pointer(datahandle_id), grating_period, shift_y))
        return errorcode, datahandle_id

    ## Loads data to show an axicon phase function. The phase has a conical shape.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param inner_radius_px The radius in number of SLM pixel where the axicon phase function reached 2pi for the first time in respect to the center of the axicon.
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_phasefunction_axicon(self, slm_id, inner_radius_px, center_x=0, center_y=0):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_phasefunction_axicon(pointer(slm_id), pointer(datahandle_id), inner_radius_px, center_x, center_y))
        return errorcode, datahandle_id

    ## Loads data to show a lens phase function. The phase has a parabolic shape.
    ## The resulting focal length can be calculated as f [m] = (\p inner_radius_px * \ref heds_slmwindow_pixelsize_um()*1.0E-6) ^2 / (2.0*lambda),
    ## with the incident optical wavelength lambda.
    ## \param slm_id The SLM screen to load the created data into.
    ## \param inner_radius_px The radius in number of SLM pixel where the lens phase function reached 2pi for the first time in respect to the center of the lens. This value is related to the focal length f of the lens phase function by f = (inner_radius_px * heds_slm_pixelsize())^2 / (2*lambda).
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_phasefunction_lens(self, slm_id, inner_radius_px, center_x=0, center_y=0):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_phasefunction_lens(pointer(slm_id), pointer(datahandle_id), inner_radius_px, center_x, center_y))
        return errorcode, datahandle_id

    ## Loads data to show an optical vortex phase function into. The phase has a helical shape.
    ## \param slm_id The SLM screen (i.e. canvas) to load the created data into.
    ## \param vortex_order The order of the optical vortex. If the order is one, the phase goes from 0 to 2pi over the full angle of 360 degree. For higher orders, 2pi phase shift is reached at angles of 360 degree divided by the given \p vortex_order. [default: 1].
    ## \param inner_radius_px The radius at the sigularity which will be set to gray value 0 on the SLM. [default: 0].
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: A handle is returned to identify the uploaded data. If datahandle_id is a null pointer, data is shown directly.
    def heds_slm_load_phasefunction_vortex(self, slm_id, vortex_order=1, inner_radius_px=0, center_x=0, center_y=0):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_phasefunction_vortex(pointer(slm_id), pointer(datahandle_id), vortex_order, inner_radius_px, center_x, center_y))
        return errorcode, datahandle_id

    ## Load image data from memory into HOLOEYE SLM Display SDK. The SDK can pre-load the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Loading data as image data marks the data to behave differently compared to phase values.
    ## Image data is shown as is and does not allow phase overlays.
    ## The expected memory layout is C and not Fortran layout. If Fortran layout is passed, please set the load flag HEDSLDF_TransposeData to compensate for that.
    ## \param slm_id The SLM screen to load the data for.
    ## \param data The data pointer to the beginning of the image data memory block. Each element can have different formats, please see \p datafmt.
    ##             The minimum reserved memory behind this pointer must be \p width * \p heigth * sizeof(element_type) bytes,
    ##             and if pitch is not 0 (default), it must be at least \p pitch * \p height * sizeof(element_type).
    ##             The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##             Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param flags Load flags to change behavior when loading data. You can already pass show flags here to be stored in the returned \p datahandle_id.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: The returned data datahandle_id. Please pass a valid pointer to a single heds_datahandle_id structure.
    def heds_slm_load_imagedata(self, slm_id, data, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        datahandle_id = heds_datahandle_id()
        data_obj = HoloeyeInputDataDescriptor(data)

        if data_obj.error_code != HEDSERR_NoError:
            return data_obj.error_code
        # data must be two-dimensional array:
        if data_obj.width <= 0:
            return HEDSERR_InvalidDataWidth
        if data_obj.height <= 0:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_imagedata(pointer(slm_id), pointer(datahandle_id), c_int(data_obj.width), c_int(data_obj.height), data_obj.c_data_ptr, c_uint(data_obj.data_format), flags, c_int(data_obj.pitch)))
        return errorcode, datahandle_id

    ## Load phase values data from memory into HOLOEYE SLM Display SDK. The SDK can pre-load the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Loading data as phase values marks the data to behave differently compared to image data. In addition,
    ## you can specify a phase value unit (e.g. 2 pi rad), at which the SDK can automatically wrap the values at.
    ## The expected memory layout is C and not Fortran layout. If Fortran layout is passed, please set the load flag
    ## HEDSLDF_TransposeData to compensate for that.
    ## \param slm_id The SLM screen to load the data for.
    ## \param data The data pointer to the beginning of the phase values memory block. Each element can have different formats, please see \p datafmt.
    ##             The minimum reserved memory behind this pointer must be \p width * \p heigth * sizeof(element_type) bytes,
    ##             and if pitch is not 0 (default), it must be at least \p pitch * \p height * sizeof(element_type).
    ##             The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##             Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param flags Load flags to change behavior when loading data. You can already pass show flags here to be stored in the returned \p datahandle_id.
    ## \param phase_unit The unit of the given phase values. The default value is 2 pi radian. If necessary, the given phase values are automatically
    ##                   and efficiently wrapped into the given phase unit by the SDK.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: The returned data datahandle_id. Please pass a valid pointer to a single heds_datahandle_id structure.
    def heds_slm_load_phasedata(self, slm_id, data, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic, phase_unit=2.0*math.pi):
        datahandle_id = heds_datahandle_id()
        data_obj = HoloeyeInputDataDescriptor(data)

        if data_obj.error_code != HEDSERR_NoError:
            return data_obj.error_code
        # data must be two-dimensional array:
        if data_obj.width <= 0:
            return HEDSERR_InvalidDataWidth
        if data_obj.height <= 0:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_load_phasedata(pointer(slm_id), pointer(datahandle_id), c_int(data_obj.width), c_int(data_obj.height), data_obj.c_data_ptr, c_uint(data_obj.data_format), flags, c_int(data_obj.pitch), phase_unit))
        return errorcode, datahandle_id

    ## Load image data from an image file on disk into HOLOEYE SLM Display SDK. The SDK can pre-load the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Loading data as image data marks the data to behave differently compared to phase values.
    ## Image data is shown as is and does not allow phase overlays.
    ## \param slm_id The SLM screen to load the data for.
    ## \param filename The file name and/or path to load the data from.
    ## \param flags Load flags to change behavior when loading data. You can already pass show flags here to be stored in the returned \p datahandle_id.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: The returned data datahandle_id. Please pass a valid pointer to a single heds_datahandle_id structure.
    def heds_slm_load_imagedata_from_file(self, slm_id, filename, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_imagedata_from_file(pointer(slm_id), pointer(datahandle_id), c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8), flags))
        return errorcode, datahandle_id

    ## Load phase values data from a file on disk into HOLOEYE SLM Display SDK. The SDK can pre-load the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Loading data as phase values marks the data to behave differently compared to image data.
    ## When loading phase values from image files containing integer gray values in range 0 to n_gray_levels-1, the phase values will be converted
    ## assuming a phase unit of 2*pi*rad for the whole file, i.e. each value will be read by doing
    ## > phase_val = (float)gray_level * (2*pi*rad) / (float)n_gray_levels,
    ## with n_gray_levels is typically 256 and gray_level is ranging from 0 to 255.
    ## If the image file stores multiple color channels, they are all converted into phase values separately.
    ## \param slm_id The SLM screen to load the data for.
    ## \param filename The file name and/or path to load the data from.
    ## \param flags Load flags to change behavior when loading data. You can already pass show flags here to be stored in the returned \p datahandle_id.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    ## \return datahandle_id: The returned data datahandle_id. Please pass a valid pointer to a single heds_datahandle_id structure.
    def heds_slm_load_phasedata_from_file(self, slm_id, filename, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        datahandle_id = heds_datahandle_id()
        errorcode = int(self.lib.heds_slm_load_phasedata_from_file(pointer(slm_id), pointer(datahandle_id), c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8), flags))
        return errorcode, datahandle_id

    ## Shows a blank screen with a constant value into a data handle. The value can either be a phase value, a gray or color
    ## value, and can be provided in all supported formats, depending on the data format provided through \p value_fmt. Whether
    ## the provided data is interpreted as phase value or as image data depends on the settings of the provided SLM screen \p slm.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param value The color value which is addressed to the full SLM.
    ##              The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##              Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_blankscreen(self, slm_id, value):
        value_obj = HoloeyeInputDataDescriptor(value)

        if value_obj.error_code != HEDSERR_NoError:
            return value_obj.error_code
        # data must be 1 x 1:
        if value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_blankscreen(pointer(slm_id), value_obj.c_data_ptr, c_uint(value_obj.data_format)))
        return errorcode

    ## Shows data to show two areas on the SLM with two different color values. The function is intended to be used for phase
    ## measurements of the SLM in which one half of the SLM can be used as a reference to the other half. The screen will be
    ## split along the vertical (y) axis. This means that the values a and b are painted to the left and right side of the SLM, resp.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param a_value The color value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default: 0]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The color value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default: 255]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param screen_divider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default: 0.5]
    ## \param flipped If set to true, the first side will addressed with \p b_value and the second side will be set to a_value. [default: false]
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_dividedscreen_vertical(self, slm_id, a_value, b_value, screen_divider=0.5, flipped=False):
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_dividedscreen_vertical(pointer(slm_id), a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), screen_divider, flipped))
        return errorcode

    ## Shows data to show two areas on the SLM with two different color values. The function is intended to be used for phase measurements of the SLM in which one half of the SLM can be used as a reference to the other half.
    ## The screen will be split along the horizontal (x) axis. This means that the color values a and b are painted to the upper and lower side of the SLM, resp.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param a_value The color value which will be adressed on the first side of the SLM. Values are wrapped to 0-255 range. [default: 0]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The color value which will be adressed on the second side of the SLM. Values are wrapped to 0-255 range. [default: 255]
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param screen_divider The ratio by which the SLM screen should be divided. Meaningful values are between 0.0 and 1.0. [default: 0.5]
    ## \param flipped If set to true, the first side will addressed with \p b_value and the second side will be set to a_value. [default: false]
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_dividedscreen_horizontal(self, slm_id, a_value, b_value, screen_divider=0.5, flipped=False):
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_dividedscreen_horizontal(pointer(slm_id), a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), screen_divider, flipped))
        return errorcode

    ## Shows data to show a vertical binary grating. The grating consists of two values \p a_value and \p b_value, which will be
    ## addressed to the SLM pixel. The width of each area with the value \p a_value and \p b_value is defined by \p a_width and
    ## \p b_width, respectively. Each pair of values is repeated so that the SLM screen is completely filled.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param a_width The width of the first pixel block with the value of \p a_value. This parameter is mandatory.
    ## \param b_width The width of the second pixel block with the value of \p b_value. This parameter is mandatory.
    ## \param a_value The addressed value of the first pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The addressed value of the second pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param shift_x The horizontal offset applied to both pixel blocks. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_grating_binary_vertical(self, slm_id, a_width, b_width, a_value, b_value, shift_x=0):
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_grating_binary_vertical(pointer(slm_id), a_width, b_width, a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), shift_x))
        return errorcode

    ## Shows data to show a horizontal binary grating. The grating consists of two values \p a_value and \p b_value, which will be
    ## addressed to the SLM pixel. The width of each area with the value \p a_value and \p b_value is defined by \p a_width and
    ## \p b_width, respectively. Each pair of values is repeated so that the SLM screen is completely filled.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param a_width The width of the first pixel block with the value of \p a_value. This parameter is mandatory.
    ## \param b_width The width of the second pixel block with the value of \p b_value. This parameter is mandatory.
    ## \param a_value The addressed value of the first pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param b_value The addressed value of the second pixel block.
    ##                The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##                Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param shift_y The vertical offset applied to both pixel blocks. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_grating_binary_horizontal(self, slm_id, a_width, b_width, a_value, b_value, shift_y=0):
        a_value_obj = HoloeyeInputDataDescriptor(a_value)

        if a_value_obj.error_code != HEDSERR_NoError:
            return a_value_obj.error_code
        # data must be 1 x 1:
        if a_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if a_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        b_value_obj = HoloeyeInputDataDescriptor(b_value)

        if b_value_obj.error_code != HEDSERR_NoError:
            return b_value_obj.error_code
        # data must be 1 x 1:
        if b_value_obj.width != 1:
            return HEDSERR_InvalidDataWidth
        if b_value_obj.height != 1:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_grating_binary_horizontal(pointer(slm_id), a_width, b_width, a_value_obj.c_data_ptr, b_value_obj.c_data_ptr, c_uint(b_value_obj.data_format), shift_y))
        return errorcode

    ## Shows data to show a vertical blazed grating on the SLM.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param grating_period The grating period in SLM pixel. The value is mandatory. Can be either positive or negative for an inverted grating profile. Please note that the phase can also be inverted by the \p phase_scale. If both values are negative, the invertions will superimpose to non invertion.
    ## \param shift_x The horizontal offset applied to the grating in pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_grating_blaze_vertical(self, slm_id, grating_period, shift_x=0):
        errorcode = int(self.lib.heds_slm_show_grating_blaze_vertical(pointer(slm_id), grating_period, shift_x))
        return errorcode

    ## Shows data to show a horizontal blazed grating on the SLM.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param grating_period The grating period in SLM pixel. The value is mandatory. Can be either positive or negative for an inverted grating profile.
    ## \param shift_y The vertical offset applied to the grating. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_grating_blaze_horizontal(self, slm_id, grating_period, shift_y=0):
        errorcode = int(self.lib.heds_slm_show_grating_blaze_horizontal(pointer(slm_id), grating_period, shift_y))
        return errorcode

    ## Shows data to show an axicon phase function. The phase has a conical shape.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param inner_radius_px The radius in number of SLM pixel where the axicon phase function reached 2pi for the first time in respect to the center of the axicon.
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_phasefunction_axicon(self, slm_id, inner_radius_px, center_x=0, center_y=0):
        errorcode = int(self.lib.heds_slm_show_phasefunction_axicon(pointer(slm_id), inner_radius_px, center_x, center_y))
        return errorcode

    ## Shows data to show a lens phase function. The phase has a parabolic shape.
    ## The resulting focal length can be calculated as f [m] = (\p inner_radius_px * \ref heds_slmwindow_pixelsize_um()*1.0E-6) ^2 / (2.0*lambda),
    ## with the incident optical wavelength lambda.
    ## \param slm_id The SLM screen to show the created data into.
    ## \param inner_radius_px The radius in number of SLM pixel where the lens phase function reached 2pi for the first time in respect to the center of the lens. This value is related to the focal length f of the lens phase function by f = (inner_radius_px * heds_slm_pixelsize())^2 / (2*lambda).
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_phasefunction_lens(self, slm_id, inner_radius_px, center_x=0, center_y=0):
        errorcode = int(self.lib.heds_slm_show_phasefunction_lens(pointer(slm_id), inner_radius_px, center_x, center_y))
        return errorcode

    ## Shows data to show an optical vortex phase function into. The phase has a helical shape.
    ## \param slm_id The SLM screen (i.e. canvas) to show the created data into.
    ## \param vortex_order The order of the optical vortex. If the order is one, the phase goes from 0 to 2pi over the full angle of 360 degree. For higher orders, 2pi phase shift is reached at angles of 360 degree divided by the given \p vortex_order. [default: 1].
    ## \param inner_radius_px The radius at the sigularity which will be set to gray value 0 on the SLM. [default: 0].
    ## \param center_x Horizontal shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \param center_y Vertical shift of the center of the optical function on the SLM in number of pixel. [default: 0].
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_phasefunction_vortex(self, slm_id, vortex_order=1, inner_radius_px=0, center_x=0, center_y=0):
        errorcode = int(self.lib.heds_slm_show_phasefunction_vortex(pointer(slm_id), vortex_order, inner_radius_px, center_x, center_y))
        return errorcode

    ## Show image data from memory into HOLOEYE SLM Display SDK. The SDK can pre-show the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Showing data as image data marks the data to behave differently compared to phase values.
    ## Image data is shown as is and does not allow phase overlays.
    ## The expected memory layout is C and not Fortran layout. If Fortran layout is passed, please set the show flag HEDSLDF_TransposeData to compensate for that.
    ## \param slm_id The SLM screen to show the data for.
    ## \param data The data pointer to the beginning of the image data memory block. Each element can have different formats, please see \p datafmt.
    ##             The minimum reserved memory behind this pointer must be \p width * \p heigth * sizeof(element_type) bytes,
    ##             and if pitch is not 0 (default), it must be at least \p pitch * \p height * sizeof(element_type).
    ##             The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##             Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param flags Show flags to change behavior when showing data. \see heds_showflags_enum.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_imagedata(self, slm_id, data, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        data_obj = HoloeyeInputDataDescriptor(data)

        if data_obj.error_code != HEDSERR_NoError:
            return data_obj.error_code
        # data must be two-dimensional array:
        if data_obj.width <= 0:
            return HEDSERR_InvalidDataWidth
        if data_obj.height <= 0:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_imagedata(pointer(slm_id), c_int(data_obj.width), c_int(data_obj.height), data_obj.c_data_ptr, c_uint(data_obj.data_format), flags, c_int(data_obj.pitch)))
        return errorcode

    ## Show phase values data from memory into HOLOEYE SLM Display SDK. The SDK can pre-show the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Showing data as phase values marks the data to behave differently compared to image data. In addition,
    ## you can specify a phase value unit (e.g. 2 pi rad), at which the SDK can automatically wrap the values at.
    ## The expected memory layout is C and not Fortran layout. If Fortran layout is passed, please set the show flag
    ## HEDSLDF_TransposeData to compensate for that.
    ## \param slm_id The SLM screen to show the data for.
    ## \param data The data pointer to the beginning of the phase values memory block. Each element can have different formats, please see \p datafmt.
    ##             The minimum reserved memory behind this pointer must be \p width * \p heigth * sizeof(element_type) bytes,
    ##             and if pitch is not 0 (default), it must be at least \p pitch * \p height * sizeof(element_type).
    ##             The input data can either be a numpy array or a ctypes array. For scalar data (1x1), native python formats like float, int etc. are supported as well.
    ##             Please refer to \b HEDS.SDK.libapi.data_conversion.HoloeyeInputDataDescriptor for more info about the supported input data formats.
    ## \param flags Show flags to change behavior when showing data. \see heds_showflags_enum.
    ## \param phase_unit The unit of the given phase values. The default value is 2 pi radian. If necessary, the given phase values are automatically
    ##                   and efficiently wrapped into the given phase unit by the SDK.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_phasedata(self, slm_id, data, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic, phase_unit=2.0*math.pi):
        data_obj = HoloeyeInputDataDescriptor(data)

        if data_obj.error_code != HEDSERR_NoError:
            return data_obj.error_code
        # data must be two-dimensional array:
        if data_obj.width <= 0:
            return HEDSERR_InvalidDataWidth
        if data_obj.height <= 0:
            return HEDSERR_InvalidDataHeight

        errorcode = int(self.lib.heds_slm_show_phasedata(pointer(slm_id), c_int(data_obj.width), c_int(data_obj.height), data_obj.c_data_ptr, c_uint(data_obj.data_format), flags, c_int(data_obj.pitch), phase_unit))
        return errorcode

    ## Show image data from an image file on disk into HOLOEYE SLM Display SDK. The SDK can pre-show the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Showing data as image data marks the data to behave differently compared to phase values.
    ## Image data is shown as is and does not allow phase overlays.
    ## \param slm_id The SLM screen to show the data for.
    ## \param filename The file name and/or path to show the data from.
    ## \param flags Show flags to change behavior when showing data. \see heds_showflags_enum.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_imagedata_from_file(self, slm_id, filename, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        errorcode = int(self.lib.heds_slm_show_imagedata_from_file(pointer(slm_id), c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8), flags))
        return errorcode

    ## Show phase values data from a file on disk into HOLOEYE SLM Display SDK. The SDK can pre-show the data into the GPU memory
    ## or any other device memory, so that the command \ref heds_datahandles_show() can be as fast as possible.
    ## Showing data as phase values marks the data to behave differently compared to image data.
    ## When showing phase values from image files containing integer gray values in range 0 to n_gray_levels-1, the phase values will be converted
    ## assuming a phase unit of 2*pi*rad for the whole file, i.e. each value will be read by doing
    ## > phase_val = (float)gray_level * (2*pi*rad) / (float)n_gray_levels,
    ## with n_gray_levels is typically 256 and gray_level is ranging from 0 to 255.
    ## If the image file stores multiple color channels, they are all converted into phase values separately.
    ## \param slm_id The SLM screen to show the data for.
    ## \param filename The file name and/or path to show the data from.
    ## \param flags Show flags to change behavior when showing data. \see heds_showflags_enum.
    ## \return errorcode: HEDSERR_NoError when there is no error. Please use \ref heds_error_string() to retrieve further error information.
    def heds_slm_show_phasedata_from_file(self, slm_id, filename, flags=HEDSLDF_Default | HEDSSHF_PresentAutomatic):
        errorcode = int(self.lib.heds_slm_show_phasedata_from_file(pointer(slm_id), c_char_p(str(filename).encode("utf-8")), c_uint(HEDSSTRFMT_UTF8), flags))
        return errorcode

