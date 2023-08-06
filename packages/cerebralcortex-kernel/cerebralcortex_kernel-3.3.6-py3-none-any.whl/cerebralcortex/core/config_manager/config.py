# Copyright (c) 2020, MD2K Center of Excellence
# - Nasir Ali <nasir.ali08@gmail.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import os.path
import pathlib

from cerebralcortex.core.config_manager.config_handler import ConfigHandler


class Configuration(ConfigHandler):
    def __init__(self, config_dir:str, cc_configs:dict="", config_file_name:str="cerebralcortex.yml"):
        """
        Constructor
        Args:
            config_dir (str): Directory path of cerebralcortex configuration files.
            cc_configs (dict or str): if sets to cc_configs="default" all defaults configs would be loaded. Or you can provide a dict of all available cc_configs as a param
            config_file_name (str): configuration file name that should be loaded
        """

        if cc_configs=="default":
            self.load_file(str(pathlib.Path(__file__).parent.absolute())+"/default.yml", default_configs=True)

        elif isinstance(cc_configs, dict):
            self.load_file(str(pathlib.Path(__file__).parent.absolute())+"/default.yml", default_configs=True)
            self.config.update(cc_configs)

        elif config_dir:
            if config_dir[-1]!="/":
                config_dir+="/"

            self.config_filepath = config_dir+config_file_name

            if not os.path.exists(self.config_filepath):
                raise Exception(self.config_filepath+" does not exist. Please check configuration directory path and configuration file name.")

            if config_dir is not None:
                self.load_file(self.config_filepath)
            else:
                self.config = None
        else:
            raise Exception("Cannot load configuration files.")
