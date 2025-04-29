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


# Please import this file in your scripts before actually importing the HOLOEYE SLM Display SDK,
# i. e. copy this file to your project and use this code in your scripts:
#
# import detect_heds_module_path
# from holoeye import slmdisplaysdk
#
#
# Another option is to copy the holoeye module directory into your project and import by only using
# import holoeye
# This way, code completion etc. might work better.


import os, sys
from platform import system

# Import the SLM Display SDK:
# define the module path for the Python API bindings:
env_path = os.getenv("HEDS_4_0_PYTHON")
if env_path is None or not os.path.isdir(env_path):
    env_path = os.path.abspath("../..")
importpath =  os.path.join(env_path, "api", "python")
sys.path.append(importpath)
#print(sys.path)
