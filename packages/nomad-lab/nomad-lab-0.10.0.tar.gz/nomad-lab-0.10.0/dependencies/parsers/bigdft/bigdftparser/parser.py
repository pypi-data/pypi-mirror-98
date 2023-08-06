#
# Copyright The NOMAD Authors.
#
# This file is part of NOMAD.
# See https://nomad-lab.eu for further info.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
import re
import logging
import importlib
from nomadcore.baseclasses import ParserInterface
logger = logging.getLogger("nomad")


class BigDFTParser(ParserInterface):
    """This class handles the initial setup before any parsing can happen. It
    determines which version of BigDFT was used to generate the output and then
    sets up a correct main parser.

    After the implementation has been setup, you can parse the files with
    parse().
    """
    def __init__(self, metainfo_to_keep=None, backend=None, default_units=None, metainfo_units=None, debug=True, log_level=logging.ERROR, store=True):
        super(BigDFTParser, self).__init__(metainfo_to_keep, backend, default_units, metainfo_units, debug, log_level, store)

    def setup_version(self):
        """Setups the version by looking at the output file and the version
        specified in it.
        """
        # Search for the BigDFT version specification. The correct parser is
        # initialized based on this information.
        regex_version = re.compile(" Version Number\s+: (\d\.\d)")
        version_id = None
        with open(self.parser_context.main_file, 'r') as outputfile:
            header = outputfile.read(50*80)
            for line in header.split("\n"):

                # Look for version definition
                result_version = regex_version.match(line)
                if result_version:
                    version_id = result_version.group(1).replace('.', '')

        if version_id is None:
            msg = "Could not find a version specification from the given main file."
            logger.exception(msg)
            raise RuntimeError(msg)

        # Setup the root folder to the fileservice that is used to access files
        dirpath, filename = os.path.split(self.parser_context.main_file)
        dirpath = os.path.abspath(dirpath)
        self.parser_context.file_service.setup_root_folder(dirpath)
        self.parser_context.file_service.set_file_id(filename, "output")

        # Setup the correct main parser based on the version id. If no match
        # for the version is found, use the main parser for NWChem 6.6
        self.setup_main_parser(version_id)

    def get_metainfo_filename(self):
        return "bigdft.nomadmetainfo.json"

    def get_parser_info(self):
        return {'name': 'big-dft-parser', 'version': '1.0'}

    def setup_main_parser(self, version_id):
        # Currently the version id is a pure integer, so it can directly be mapped
        # into a package name.
        base = "bigdftparser.versions.bigdft{}.mainparser".format(version_id)
        parser_module = None
        parser_class = None
        try:
            parser_module = importlib.import_module(base)
        except ImportError:
            logger.warning("Could not find a parser for version '{}'. Trying to default to the base implementation for BigDFT 1.8.0".format(version_id))
            base = "bigdftparser.versions.bigdft18.mainparser"
            try:
                parser_module = importlib.import_module(base)
            except ImportError:
                logger.exception("Could not find the module '{}'".format(base))
                raise
        try:
            class_name = "BigDFTMainParser"
            parser_class = getattr(parser_module, class_name)
        except AttributeError:
            logger.exception("A parser class '{}' could not be found in the module '[]'.".format(class_name, parser_module))
            raise
        self.main_parser = parser_class(self.parser_context)
