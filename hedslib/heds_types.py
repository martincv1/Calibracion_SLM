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


import ctypes


HEDS_SLMWINDOW_MAX_COUNT = 8
HEDS_SLMWINDOW_ID_MAX = (HEDS_SLMWINDOW_MAX_COUNT - 1)
HEDS_SLMWINDOW_ID_INVALID = HEDS_SLMWINDOW_MAX_COUNT
HEDS_SLMWINDOW_ID_DEFAULT = 0
HEDS_SLMSCREEN_MAX_COUNT = 254
HEDS_SLMSCREEN_ID_MAX = (HEDS_SLMSCREEN_MAX_COUNT - 1)
HEDS_SLMSCREEN_ID_INVALID = 0xFF
HEDS_DATAHANDLE_MAX_DURATION = 255


## Each SLM screen area can have different modulation types, describing how the hardware is used in an optical setup.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_slm_modulation_enum:
    ## In intensity mode, data manipulations only valid for phase modulation are not applied by the renderer.
    HEDSSLMMOD_Intensity = 0

    ## In phase modulation mode, all data manipulations are applied.
    HEDSSLMMOD_Phase = 1

# Make enum values for heds_slm_modulation_enum available without namespace:
HEDSSLMMOD_Intensity = heds_slm_modulation_enum.HEDSSLMMOD_Intensity
HEDSSLMMOD_Phase = heds_slm_modulation_enum.HEDSSLMMOD_Phase




## Pixel data format of image or phase shift data passed through a void pointer in ANSI C API.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_dataformat_enum:
    ## Each byte represents one pixel. This is gray scale image data with 8-bit depth, i.e. gray values ranging from 0 to 255. If used for phase data, the values are interpreted as grayvalue/256*2*pi.
    HEDSDTFMT_INT_U8 = 0

    ## Three bytes per pixel, with 8-bit gray scale image data for red (index 0), green (index 1), and blue (index 2) color channels.
    HEDSDTFMT_INT_RGB24 = 1

    ## Four bytes per pixel, with 8-bit gray scale image data for red, green, and blue color channels, and an additional alpha channel, which is ignored by this SDK.
    HEDSDTFMT_INT_RGBA32 = 2

    ## 32-bit floating point data, i.e. float. This is the recommended floating point format.
    HEDSDTFMT_FLOAT_32 = 3

    ## 64-bit floating point data, i.e. double. When passing such data, the data will be converted internally into 32-bit floating point format, which results in lower performance.
    HEDSDTFMT_FLOAT_64 = 4

# Make enum values for heds_dataformat_enum available without namespace:
HEDSDTFMT_INT_U8 = heds_dataformat_enum.HEDSDTFMT_INT_U8
HEDSDTFMT_INT_RGB24 = heds_dataformat_enum.HEDSDTFMT_INT_RGB24
HEDSDTFMT_INT_RGBA32 = heds_dataformat_enum.HEDSDTFMT_INT_RGBA32
HEDSDTFMT_FLOAT_32 = heds_dataformat_enum.HEDSDTFMT_FLOAT_32
HEDSDTFMT_FLOAT_64 = heds_dataformat_enum.HEDSDTFMT_FLOAT_64




## In addition to the data format, this can be used to provide a memory layout the image or phase shift data is stored in.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_memorylayout_enum:
    ## Use the HEDSAPI_... value to determine the memory layout automatically.
    HEDSMEMLO_Autodetect = 0

    ## C memory layout means row-by-row storage, and pixels are stored one after each other.
    HEDSMEMLO_C = 1

    ## MATLAB storage format means Fortran (column-by-column) storage, and pixel color channels are
    ## stored as field red, field green, field blue after each other using a three dimensional array.
    HEDSMEMLO_MATLAB = 2

# Make enum values for heds_memorylayout_enum available without namespace:
HEDSMEMLO_Autodetect = heds_memorylayout_enum.HEDSMEMLO_Autodetect
HEDSMEMLO_C = heds_memorylayout_enum.HEDSMEMLO_C
HEDSMEMLO_MATLAB = heds_memorylayout_enum.HEDSMEMLO_MATLAB




## Format of string data passed through a C-string void pointer.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_stringformat_enum:
    ## Encoding: ASCII; Codepage: Unicode.
    HEDSSTRFMT_UTF8 = 0

    ## Encoding: UTF16; Codepage: Unicode.
    HEDSSTRFMT_UTF16 = 1

    ## Encoding: UTF32; Codepage: Unicode.
    HEDSSTRFMT_UTF32 = 2

    ## Encoding: Either UTF16 or UTF32, depending on platform; Codepage: Unicode.
    HEDSSTRFMT_WCHAR = 3

    ## Encoding: ASCII; Codepage: Latin1, CP1252, etc. The codepage of the system settings.
    HEDSSTRFMT_Latin1 = 4

# Make enum values for heds_stringformat_enum available without namespace:
HEDSSTRFMT_UTF8 = heds_stringformat_enum.HEDSSTRFMT_UTF8
HEDSSTRFMT_UTF16 = heds_stringformat_enum.HEDSSTRFMT_UTF16
HEDSSTRFMT_UTF32 = heds_stringformat_enum.HEDSSTRFMT_UTF32
HEDSSTRFMT_WCHAR = heds_stringformat_enum.HEDSSTRFMT_WCHAR
HEDSSTRFMT_Latin1 = heds_stringformat_enum.HEDSSTRFMT_Latin1




## A list of available load flags. Please use heds_flags_t as storage format.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_loadflags_enum:
    ## The default load behavior, optimized for performance.
    HEDSLDF_Default = 0

    ## Generate a colortable for the provided data. Only applies to integer data types (HEDS_DF_INT_...).
    HEDSLDF_CreateColorTable = 65536

    ## Shows the data after loading it and transfers the data right before showing it.    This is only a convenience feature and cannot provide optimal performance.
    HEDSLDF_ShowImmediately = 131072

    ## This load flag inverts the transpose option in showflags, which conjugate-transposes the data by exchanging rows and colums to convert from Fortran to C memory layout.
    ## Please use this when the API data is stored in Fortran memory layout instead of C memory layout, e.g. in Python Numpy, MATLAB/Octave, etc.
    HEDSLDF_TransposeData = 262144

# Make enum values for heds_loadflags_enum available without namespace:
HEDSLDF_Default = heds_loadflags_enum.HEDSLDF_Default
HEDSLDF_CreateColorTable = heds_loadflags_enum.HEDSLDF_CreateColorTable
HEDSLDF_ShowImmediately = heds_loadflags_enum.HEDSLDF_ShowImmediately
HEDSLDF_TransposeData = heds_loadflags_enum.HEDSLDF_TransposeData




## A list of available show flags. Please use heds_flags_t as storage format.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_showflags_enum:
    ## Shows two-dimensional data unscaled at the center of the slm. One-dimensional data is shown as a grating.
    HEDSSHF_PresentAutomatic = 0

    ## The data is shown unscaled at the center of the slm.
    ## Free areas are filled with zeroes. The data is cropped to the slm size.
    HEDSSHF_PresentCentered = 1

    ## If set, the data will fit the slm so all data is visible and the aspect ratio is kept.
    ## Free areas on the top/bottom or left/right will be filled with zeroes.
    ## Only one of the present flags may be set.
    ## This option changes the scale of the displayed data. Therefore this show flag overwrites the transformScale option in a data handle.
    HEDSSHF_PresentFitWithBars = 2

    ## If set, the data will fit the slm so the slm is completely filled with data but the aspect ratio is kept.
    ## Some data might not be visible. Only one of the present flags may be set.
    ## This option changes the scale of the displayed data. Therefore this show flag overwrites the transformScale option in a data handle.
    HEDSSHF_PresentFitNoBars = 4

    ## If set, the data will completely fill the slm. The aspect ratio will not be kept.
    ## In short the data is shown fullscreen. Only one of the present flags may be set.
    ## This option changes the scale of the displayed data. Therefore this show flag overwrites the transformScale option in a data handle.
    HEDSSHF_PresentFitScreen = 8

    ## Shows the given data in a tiling pattern. The pattern is tiled around the center of the slm.
    HEDSSHF_PresentTiledCentered = 16

    ## If set, the rows and columns will be switched, i.e. the data is conjugate-transposed to convert from Fortran to C memory layout.
    HEDSSHF_TransposeData = 32

    ## If set, the data will be flipped horizontally.
    HEDSSHF_FlipHorizontal = 64

    ## If set, the data will be flipped vertically.
    HEDSSHF_FlipVertical = 128

    ## If set, the data will be inverted.
    HEDSSHF_InvertValues = 256

# Make enum values for heds_showflags_enum available without namespace:
HEDSSHF_PresentAutomatic = heds_showflags_enum.HEDSSHF_PresentAutomatic
HEDSSHF_PresentCentered = heds_showflags_enum.HEDSSHF_PresentCentered
HEDSSHF_PresentFitWithBars = heds_showflags_enum.HEDSSHF_PresentFitWithBars
HEDSSHF_PresentFitNoBars = heds_showflags_enum.HEDSSHF_PresentFitNoBars
HEDSSHF_PresentFitScreen = heds_showflags_enum.HEDSSHF_PresentFitScreen
HEDSSHF_PresentTiledCentered = heds_showflags_enum.HEDSSHF_PresentTiledCentered
HEDSSHF_TransposeData = heds_showflags_enum.HEDSSHF_TransposeData
HEDSSHF_FlipHorizontal = heds_showflags_enum.HEDSSHF_FlipHorizontal
HEDSSHF_FlipVertical = heds_showflags_enum.HEDSSHF_FlipVertical
HEDSSHF_InvertValues = heds_showflags_enum.HEDSSHF_InvertValues




## The current state of the rendering process of a specific data handle ID.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_datahandle_state_enum:
    ## The data was just created.
    HEDSDHST_Issued = 0

    ## The given filename or data is waiting for processing.
    HEDSDHST_WaitingForProcessing = 1

    ## The given filename is being loaded.
    HEDSDHST_LoadingFile = 2

    ## The given or loaded data needs to be converted. Performance Warning!
    HEDSDHST_ConvertingData = 3

    ## The data is being processed for display. This is not about conversion but about processing the data.
    HEDSDHST_ProcessingData = 4

    ## The data is waiting to be transferred to the gpu.
    HEDSDHST_WaitingForTransfer = 5

    ## The data is uploaded to the gpu.
    HEDSDHST_TransferringData = 6

    ## The data is ready to be rendered. This is the end state of the loading process.
    HEDSDHST_ReadyToRender = 7

    ## The data is waiting to be rendered. This is the first state when showing data.
    HEDSDHST_WaitingForRendering = 8

    ## The data is being rendered. This is about the actual effort needed to render the data.
    HEDSDHST_Rendering = 9

    ## The data is waiting to become visible on the SLM. Only applies to deferred rendering.
    HEDSDHST_WaitingToBecomeVisible = 10

    ## The data is currently visible on the slm.
    HEDSDHST_Visible = 11

    ## The data is currently visible on the slm and the property durationInFrames has passed.
    HEDSDHST_VisibleDurationFinished = 12

    ## The data has been shown and is now no longer visible.
    HEDSDHST_Finished = 13

    ## An error occured. Check error code.
    HEDSDHST_Error = 14

# Make enum values for heds_datahandle_state_enum available without namespace:
HEDSDHST_Issued = heds_datahandle_state_enum.HEDSDHST_Issued
HEDSDHST_WaitingForProcessing = heds_datahandle_state_enum.HEDSDHST_WaitingForProcessing
HEDSDHST_LoadingFile = heds_datahandle_state_enum.HEDSDHST_LoadingFile
HEDSDHST_ConvertingData = heds_datahandle_state_enum.HEDSDHST_ConvertingData
HEDSDHST_ProcessingData = heds_datahandle_state_enum.HEDSDHST_ProcessingData
HEDSDHST_WaitingForTransfer = heds_datahandle_state_enum.HEDSDHST_WaitingForTransfer
HEDSDHST_TransferringData = heds_datahandle_state_enum.HEDSDHST_TransferringData
HEDSDHST_ReadyToRender = heds_datahandle_state_enum.HEDSDHST_ReadyToRender
HEDSDHST_WaitingForRendering = heds_datahandle_state_enum.HEDSDHST_WaitingForRendering
HEDSDHST_Rendering = heds_datahandle_state_enum.HEDSDHST_Rendering
HEDSDHST_WaitingToBecomeVisible = heds_datahandle_state_enum.HEDSDHST_WaitingToBecomeVisible
HEDSDHST_Visible = heds_datahandle_state_enum.HEDSDHST_Visible
HEDSDHST_VisibleDurationFinished = heds_datahandle_state_enum.HEDSDHST_VisibleDurationFinished
HEDSDHST_Finished = heds_datahandle_state_enum.HEDSDHST_Finished
HEDSDHST_Error = heds_datahandle_state_enum.HEDSDHST_Error




## A list of the supported Zernike functions and their position in the list of values.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_zernikevalues_enum:
    ## The radius is always the first argument and is required. It is provided in pixels.
    HEDSZER_RadiusPx = 0

    ## The Tilt X function. f = x
    HEDSZER_TiltX = 1

    ## The Tilt Y function. f = y
    HEDSZER_TiltY = 2

    ## The Astig 45deg function. f = 2xy
    HEDSZER_Astig45 = 3

    ## The Defocus function. f = 1-2x^2-2y^2
    HEDSZER_Defocus = 4

    ## The Astig 0deg function. f = y^2-x^2
    HEDSZER_Astig0 = 5

    ## The Trifoil X function. f = 3xy^2-x^3
    HEDSZER_TrifoilX = 6

    ## The Coma X function. f = -2x+3xy^2+3x^3
    HEDSZER_ComaX = 7

    ## The Coma Y function. f = -2y+3y^3+3x^2y
    HEDSZER_ComaY = 8

    ## The Trifoil Y function. f = y^3-3x^2y
    HEDSZER_TrifoilY = 9

    ## The Quadrafoil X function. f = 4y^3x-4x^3y
    HEDSZER_QuadrafoilX = 10

    ## The Astig 2nd 45deg function. f = -6xy+8y^3x+8x^3y
    HEDSZER_Astig2nd45 = 11

    ## The Spherical ABB function. f = 1-6y^2-6x^2+6y^4+12x^2y^2+6x^4
    HEDSZER_SphericalABB = 12

    ## The Astig 2nd 0deg function. f = -3y^2+3x^2+4y^4-4x^2y^2-4x^4
    HEDSZER_Astig2nd0 = 13

    ## The Quadrafoil Y function. f = y^4-6x^2y^2+x^4
    HEDSZER_QuadrafoilY = 14

    ## The number of supported Zernike values.
    HEDSZER_COUNT = 15

# Make enum values for heds_zernikevalues_enum available without namespace:
HEDSZER_RadiusPx = heds_zernikevalues_enum.HEDSZER_RadiusPx
HEDSZER_TiltX = heds_zernikevalues_enum.HEDSZER_TiltX
HEDSZER_TiltY = heds_zernikevalues_enum.HEDSZER_TiltY
HEDSZER_Astig45 = heds_zernikevalues_enum.HEDSZER_Astig45
HEDSZER_Defocus = heds_zernikevalues_enum.HEDSZER_Defocus
HEDSZER_Astig0 = heds_zernikevalues_enum.HEDSZER_Astig0
HEDSZER_TrifoilX = heds_zernikevalues_enum.HEDSZER_TrifoilX
HEDSZER_ComaX = heds_zernikevalues_enum.HEDSZER_ComaX
HEDSZER_ComaY = heds_zernikevalues_enum.HEDSZER_ComaY
HEDSZER_TrifoilY = heds_zernikevalues_enum.HEDSZER_TrifoilY
HEDSZER_QuadrafoilX = heds_zernikevalues_enum.HEDSZER_QuadrafoilX
HEDSZER_Astig2nd45 = heds_zernikevalues_enum.HEDSZER_Astig2nd45
HEDSZER_SphericalABB = heds_zernikevalues_enum.HEDSZER_SphericalABB
HEDSZER_Astig2nd0 = heds_zernikevalues_enum.HEDSZER_Astig2nd0
HEDSZER_QuadrafoilY = heds_zernikevalues_enum.HEDSZER_QuadrafoilY
HEDSZER_COUNT = heds_zernikevalues_enum.HEDSZER_COUNT




## Represents the different settings for the preview window.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_slmpreviewflags_enum:
    ## No settings will be applied.
    HEDSSLMPF_None = 0

    ## Disables the border of the preview window.
    HEDSSLMPF_NoBorder = 1

    ## Makes sure the window is on top of other windows.
    HEDSSLMPF_OnTop = 2

    ## Shows the Zernike radius.
    HEDSSLMPF_ShowZernikeRadius = 4

    ## Show the wavefront compensation in the preview.
    HEDSSLMPF_ShowWavefrontCompensation = 8

# Make enum values for heds_slmpreviewflags_enum available without namespace:
HEDSSLMPF_None = heds_slmpreviewflags_enum.HEDSSLMPF_None
HEDSSLMPF_NoBorder = heds_slmpreviewflags_enum.HEDSSLMPF_NoBorder
HEDSSLMPF_OnTop = heds_slmpreviewflags_enum.HEDSSLMPF_OnTop
HEDSSLMPF_ShowZernikeRadius = heds_slmpreviewflags_enum.HEDSSLMPF_ShowZernikeRadius
HEDSSLMPF_ShowWavefrontCompensation = heds_slmpreviewflags_enum.HEDSSLMPF_ShowWavefrontCompensation




## Defines indices for different color channels. This needs to be used when working with data formats like \see heds_rgb24 and \see heds_rgba32.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_color_channel_index_enum:
    ## The red color channel index.
    HEDSCCI_Red = 0

    ## The green color channel index.
    HEDSCCI_Green = 1

    ## The blue color channel index.
    HEDSCCI_Blue = 2

    ## The monochrome color channel index.
    HEDSCCI_Mono = 0

# Make enum values for heds_color_channel_index_enum available without namespace:
HEDSCCI_Red = heds_color_channel_index_enum.HEDSCCI_Red
HEDSCCI_Green = heds_color_channel_index_enum.HEDSCCI_Green
HEDSCCI_Blue = heds_color_channel_index_enum.HEDSCCI_Blue
HEDSCCI_Mono = heds_color_channel_index_enum.HEDSCCI_Mono




## Defines types for different color channels, which can be combined in one unsigned char (8-bit) value. This needs to be used when passing color channel dependent information through the API for multiple color channels in one API call.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_color_channel_enum:
    ## The red color channel.
    HEDSCC_Red = 1

    ## The green color channel.
    HEDSCC_Green = 2

    ## The blue color channel.
    HEDSCC_Blue = 4

    ## The monochrome color channel. (HEDSCC_Red | HEDSCC_Green | HEDSCC_Blue)
    HEDSCC_Mono = 7

# Make enum values for heds_color_channel_enum available without namespace:
HEDSCC_Red = heds_color_channel_enum.HEDSCC_Red
HEDSCC_Green = heds_color_channel_enum.HEDSCC_Green
HEDSCC_Blue = heds_color_channel_enum.HEDSCC_Blue
HEDSCC_Mono = heds_color_channel_enum.HEDSCC_Mono




## The code for any error that occured. Please use the function \ref holoeye_slmdisplaysdk_library.heds_error_string() to retrieve the documentation of each
## error code in a string format to be used for showing the error strings in your user interface.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_errorcodes:
    ## No error.
    HEDSERR_NoError = 0

    ## The given SLM window does not exist.
    HEDSERR_NoSLMConnected = 1

    ## The given filename is zero or too long.
    HEDSERR_InvalidFilename = 2

    ## A filename was given, but the file does not exist.
    HEDSERR_FileNotFound = 3

    ## A filename was given and the file exists, but the file format is not supported.
    HEDSERR_UnsupportedFileFormat = 4

    ## The given data is zero or too long.
    HEDSERR_InvalidDataPointer = 5

    ## The given data has a width less than one.
    HEDSERR_InvalidDataWidth = 6

    ## The given data has a height less than one.
    HEDSERR_InvalidDataHeight = 7

    ## A valid and supported filename or data was given, but the contained format is not supported.
    HEDSERR_UnsupportedDataFormat = 8

    ## The renderer had an internal error, for example when updating the window or sprite.
    HEDSERR_InternalRendererError = 9

    ## There is not enough system memory left to process the given filename or data.
    HEDSERR_OutOfSystemMemory = 10

    ## Data transfer into video memory failed. There is either not enough video memory left on the GPU,
    ## or the maximum number of data handles with data on the GPU has been reached.
    ## Please release unused data handles and try again.
    HEDSERR_OutOfVideoMemory = 11

    ## The current handle is invalid.
    HEDSERR_InvalidHandle = 12

    ## The provided duration in frames is less than one or higher than 255.
    HEDSERR_InvalidDurationInFrames = 13

    ## The given phase wrap must be greater than zero.
    HEDSERR_InvalidPhaseWrap = 14

    ## Waiting for a datahandle to reach a certain state timed out and failed.
    HEDSERR_WaitForHandleTimedOut = 15

    ## The number of Zernike values must be between zero and \ref HEDSZER_COUNT.
    HEDSERR_InvalidZernikeValueSize = 19

    ## The scale needs to be greater than zero.
    HEDSERR_InvalidTransformScale = 20

    ## The value of a given enum is invalid.
    HEDSERR_InvalidEnumValue = 21

    ## One of the arguments is invalid.
    HEDSERR_InvalidArgument = 22

    ## The specified SLM screen does not exist.
    HEDSERR_InvalidSLMScreen = 23

    ## The data is locked to another SLM screen.
    HEDSERR_LockedToOtherSLM = 24

    ## The specified custom shader could not be found.
    HEDSERR_CustomShaderNotFound = 25

    ## The specified custom shader ha no data function.
    HEDSERR_CustomShaderHasNoDataFunction = 26

    ## The custom shader could not be compiled.
    HEDSERR_CustomerShaderFailedToCompile = 27

    ## Failed to connect to host.
    HEDSERR_ConnectionFailed = 28

    ## Internal network timeout occurred.
    HEDSERR_ConnectionTimedOut = 29

    ## There was an internal error during the connection.
    HEDSERR_ConnectionInternalError = 30

    ## The handle does not belong to the given SLM window.
    HEDSERR_HandleSLMWindowMismatch = 31

    ## The SLM screen does not belong to the given SLM window.
    HEDSERR_SLMScreenMismatch = 32

    ## The limit of the number of concurrently open SLM windows is reached.
    HEDSERR_MaxSLMWindowCountReached = 33

    ## The SLM screen count within an SLMWindow is limited to HEDS_SLMSCREEN_MAX_COUNT. This error occurs if you try to set up too many SLM screens within an SLMWindow.
    HEDSERR_MaxSLMScreenCountReached = 34

    ## The API function called needed other API calls for preparation. Please make sure to call functions in the correct order.
    HEDSERR_InvalidAPIUsage = 35

    ## SLM screens must be fully within the SLM window.
    HEDSERR_SLMScreenOutOfWindowArea = 36

    ## The SLM window ID is invalid.
    HEDSERR_InvalidSLMWindow = 37

    ## There was an internal error and the requested action was aborted.
    HEDSERR_InternalError = 38

    ## There was an error, which ocurred in the internal API implementation. The requested action was aborted.
    HEDSERR_APIInternalError = 39

    ## Each SLM screen has set a mode. This error occurs when loading data into an SLM screen and the data type does not match the mode the SLM screen is set to.
    HEDSERR_DataIncompatibleWithModulationType = 40

    ## Unknown data format was specified. Please provide the data only in supported formats.
    HEDSERR_InvalidDataFormat = 41

    ## SLM screen geometry must not overlap with another SLM screen geometry.
    HEDSERR_SLMScreenOverlap = 42

    ## There was an error when creating SLM screens within SLM window.
    HEDSERR_SLMSetupError = 43

    ## The library (.dll or .so file) has an API incompatible version. Please install the correct SDK version required to run your program or migrate your program to this SDK version.
    HEDSERR_LibraryVersionMismatch = 44

    ## The SDK must be initialized before opening any SLM window. It must be done after the library (.dll or .so file) was loaded.
    ## Please either call the appropriate Convenience API function HEDS::SDK::Init() / heds_sdk_init() or call \ref holoeye_slmdisplaysdk_library.heds_config_api() manually.
    HEDSERR_SDKNotInitialized = 45

    ## The requested feature is not implemented under the currently used platform.
    HEDSERR_NotImplemented = 46

# Make enum values for heds_errorcodes available without namespace:
HEDSERR_NoError = heds_errorcodes.HEDSERR_NoError
HEDSERR_NoSLMConnected = heds_errorcodes.HEDSERR_NoSLMConnected
HEDSERR_InvalidFilename = heds_errorcodes.HEDSERR_InvalidFilename
HEDSERR_FileNotFound = heds_errorcodes.HEDSERR_FileNotFound
HEDSERR_UnsupportedFileFormat = heds_errorcodes.HEDSERR_UnsupportedFileFormat
HEDSERR_InvalidDataPointer = heds_errorcodes.HEDSERR_InvalidDataPointer
HEDSERR_InvalidDataWidth = heds_errorcodes.HEDSERR_InvalidDataWidth
HEDSERR_InvalidDataHeight = heds_errorcodes.HEDSERR_InvalidDataHeight
HEDSERR_UnsupportedDataFormat = heds_errorcodes.HEDSERR_UnsupportedDataFormat
HEDSERR_InternalRendererError = heds_errorcodes.HEDSERR_InternalRendererError
HEDSERR_OutOfSystemMemory = heds_errorcodes.HEDSERR_OutOfSystemMemory
HEDSERR_OutOfVideoMemory = heds_errorcodes.HEDSERR_OutOfVideoMemory
HEDSERR_InvalidHandle = heds_errorcodes.HEDSERR_InvalidHandle
HEDSERR_InvalidDurationInFrames = heds_errorcodes.HEDSERR_InvalidDurationInFrames
HEDSERR_InvalidPhaseWrap = heds_errorcodes.HEDSERR_InvalidPhaseWrap
HEDSERR_WaitForHandleTimedOut = heds_errorcodes.HEDSERR_WaitForHandleTimedOut
HEDSERR_InvalidZernikeValueSize = heds_errorcodes.HEDSERR_InvalidZernikeValueSize
HEDSERR_InvalidTransformScale = heds_errorcodes.HEDSERR_InvalidTransformScale
HEDSERR_InvalidEnumValue = heds_errorcodes.HEDSERR_InvalidEnumValue
HEDSERR_InvalidArgument = heds_errorcodes.HEDSERR_InvalidArgument
HEDSERR_InvalidSLMScreen = heds_errorcodes.HEDSERR_InvalidSLMScreen
HEDSERR_LockedToOtherSLM = heds_errorcodes.HEDSERR_LockedToOtherSLM
HEDSERR_CustomShaderNotFound = heds_errorcodes.HEDSERR_CustomShaderNotFound
HEDSERR_CustomShaderHasNoDataFunction = heds_errorcodes.HEDSERR_CustomShaderHasNoDataFunction
HEDSERR_CustomerShaderFailedToCompile = heds_errorcodes.HEDSERR_CustomerShaderFailedToCompile
HEDSERR_ConnectionFailed = heds_errorcodes.HEDSERR_ConnectionFailed
HEDSERR_ConnectionTimedOut = heds_errorcodes.HEDSERR_ConnectionTimedOut
HEDSERR_ConnectionInternalError = heds_errorcodes.HEDSERR_ConnectionInternalError
HEDSERR_HandleSLMWindowMismatch = heds_errorcodes.HEDSERR_HandleSLMWindowMismatch
HEDSERR_SLMScreenMismatch = heds_errorcodes.HEDSERR_SLMScreenMismatch
HEDSERR_MaxSLMWindowCountReached = heds_errorcodes.HEDSERR_MaxSLMWindowCountReached
HEDSERR_MaxSLMScreenCountReached = heds_errorcodes.HEDSERR_MaxSLMScreenCountReached
HEDSERR_InvalidAPIUsage = heds_errorcodes.HEDSERR_InvalidAPIUsage
HEDSERR_SLMScreenOutOfWindowArea = heds_errorcodes.HEDSERR_SLMScreenOutOfWindowArea
HEDSERR_InvalidSLMWindow = heds_errorcodes.HEDSERR_InvalidSLMWindow
HEDSERR_InternalError = heds_errorcodes.HEDSERR_InternalError
HEDSERR_APIInternalError = heds_errorcodes.HEDSERR_APIInternalError
HEDSERR_DataIncompatibleWithModulationType = heds_errorcodes.HEDSERR_DataIncompatibleWithModulationType
HEDSERR_InvalidDataFormat = heds_errorcodes.HEDSERR_InvalidDataFormat
HEDSERR_SLMScreenOverlap = heds_errorcodes.HEDSERR_SLMScreenOverlap
HEDSERR_SLMSetupError = heds_errorcodes.HEDSERR_SLMSetupError
HEDSERR_LibraryVersionMismatch = heds_errorcodes.HEDSERR_LibraryVersionMismatch
HEDSERR_SDKNotInitialized = heds_errorcodes.HEDSERR_SDKNotInitialized
HEDSERR_NotImplemented = heds_errorcodes.HEDSERR_NotImplemented




## Defines which software package uses the SDK.
## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_sdkapi_index_enum:
    ## This is the default and will result in an error.
    HEDSAPI_Unknown = 0

    ## The SDK is used from ANSI C.
    HEDSAPI_ANSIC = 1

    ## The SDK is used from C++.
    HEDSAPI_CPP = 2

    ## The SDK is used from Python.
    HEDSAPI_Python = 3

    ## The SDK is used from MATLAB.
    HEDSAPI_MATLAB = 4

    ## The SDK is used from Octave.
    HEDSAPI_Octave = 5

    ## The SDK is used from LabVIEW.
    HEDSAPI_LabVIEW = 6

# Make enum values for heds_sdkapi_index_enum available without namespace:
HEDSAPI_Unknown = heds_sdkapi_index_enum.HEDSAPI_Unknown
HEDSAPI_ANSIC = heds_sdkapi_index_enum.HEDSAPI_ANSIC
HEDSAPI_CPP = heds_sdkapi_index_enum.HEDSAPI_CPP
HEDSAPI_Python = heds_sdkapi_index_enum.HEDSAPI_Python
HEDSAPI_MATLAB = heds_sdkapi_index_enum.HEDSAPI_MATLAB
HEDSAPI_Octave = heds_sdkapi_index_enum.HEDSAPI_Octave
HEDSAPI_LabVIEW = heds_sdkapi_index_enum.HEDSAPI_LabVIEW




## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_slm_id(ctypes.Structure):
    ## ctypes internal struct field map:
    _fields_ = [
        ("slmwindow_id", ctypes.c_uint),
        ("slmscreen_id", ctypes.c_uint),
    ]

    ## Constructs a new ctypes struct object of type heds_slm_id.
    ## \param slmwindow_id The SLM window this SLM screen belongs to. Default is HEDS_SLMWINDOW_ID_INVALID.
    ## \param slmscreen_id The ID of the SLM screen, counted within slmwindow_id. Default is 0.
    def __init__(self, slmwindow_id=HEDS_SLMWINDOW_ID_INVALID, slmscreen_id=0):
        ## The SLM window this SLM screen belongs to.
        self.slmwindow_id = ctypes.c_uint(slmwindow_id)

        ## The ID of the SLM screen, counted within slmwindow_id.
        self.slmscreen_id = ctypes.c_uint(slmscreen_id)



## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_datahandle_id(ctypes.Structure):
    ## ctypes internal struct field map:
    _fields_ = [
        ("slmwindow_id", ctypes.c_uint),
        ("slmscreen_id", ctypes.c_uint),
        ("datahandle_id", ctypes.c_uint),
    ]

    ## Constructs a new ctypes struct object of type heds_datahandle_id.
    ## \param slmwindow_id The SLM window the data related to this handle was uploaded into. Default is HEDS_SLMWINDOW_ID_INVALID.
    ## \param slmscreen_id The index of the SLM screen this data handle belongs to, counted within slmwindow_id. Default is 0.
    ## \param datahandle_id The index of the data handle, counted within slmwindow_id. Default is 0.
    def __init__(self, slmwindow_id=HEDS_SLMWINDOW_ID_INVALID, slmscreen_id=0, datahandle_id=0):
        ## The SLM window the data related to this handle was uploaded into.
        self.slmwindow_id = ctypes.c_uint(slmwindow_id)

        ## The index of the SLM screen this data handle belongs to, counted within slmwindow_id.
        self.slmscreen_id = ctypes.c_uint(slmscreen_id)

        ## The index of the data handle, counted within slmwindow_id.
        self.datahandle_id = ctypes.c_uint(datahandle_id)



## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_rgb24(ctypes.Structure):
    ## ctypes internal struct field map:
    _fields_ = [
        ("r", ctypes.c_ubyte),
        ("g", ctypes.c_ubyte),
        ("b", ctypes.c_ubyte),
    ]

    ## Constructs a new ctypes struct object of type heds_rgb24.
    ## \param r The 8-bit color intensity value for the red color channel. Default is 0.
    ## \param g The 8-bit color intensity value for the green color channel. Default is 0.
    ## \param b The 8-bit color intensity value for the blue color channel. Default is 0.
    def __init__(self, r=0, g=0, b=0):
        ## The 8-bit color intensity value for the red color channel.
        self.r = ctypes.c_ubyte(r)

        ## The 8-bit color intensity value for the green color channel.
        self.g = ctypes.c_ubyte(g)

        ## The 8-bit color intensity value for the blue color channel.
        self.b = ctypes.c_ubyte(b)



## \ingroup SLMDisplaySDK_LIBAPI_Python
class heds_rgba32(ctypes.Structure):
    ## ctypes internal struct field map:
    _fields_ = [
        ("r", ctypes.c_ubyte),
        ("g", ctypes.c_ubyte),
        ("b", ctypes.c_ubyte),
        ("a", ctypes.c_ubyte),
    ]

    ## Constructs a new ctypes struct object of type heds_rgba32.
    ## \param r The 8-bit color intensity value for the red color channel. Default is 0.
    ## \param g The 8-bit color intensity value for the green color channel. Default is 0.
    ## \param b The 8-bit color intensity value for the blue color channel. Default is 0.
    ## \param a The 8-bit alpha channel. This value is ignored in SLM Display SDK API functions That means it behaves like if a is 255. Default is 255.
    def __init__(self, r=0, g=0, b=0, a=255):
        ## The 8-bit color intensity value for the red color channel.
        self.r = ctypes.c_ubyte(r)

        ## The 8-bit color intensity value for the green color channel.
        self.g = ctypes.c_ubyte(g)

        ## The 8-bit color intensity value for the blue color channel.
        self.b = ctypes.c_ubyte(b)

        ## The 8-bit alpha channel. This value is ignored in SLM Display SDK API functions That means it behaves like if a is 255.
        self.a = ctypes.c_ubyte(a)

