#!/usr/bin/env python3

# Copyright 2021 Open Source Robotics Foundation, Inc.
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

import sys
import os
import argparse

from jinja2 import Template
import glob

###############################################################################


def main(argv=None):
    """
    This script will load a list of json schemas for py module generation.
    According to the jinja2 py template, it will then generate a schemas.py
    script locally for pkg installation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pkg_dir', required=True,
                        type=str, help='rmf_api_msgs pkg dir')
    args = parser.parse_args(argv[1:])

    # collections of file paths for IO
    template_path = f'{args.pkg_dir}/scripts/schemas_template.jinja2'
    schemas_files_dir = f'{args.pkg_dir}/schemas/*.json'
    output_script_path = f'{args.pkg_dir}/rmf_api_msgs/schemas.py'

    # open template
    file = open(template_path)
    schema_template = file.read()
    file.close()

    t = Template(schema_template)
    print("py template for json schema is loaded, now load json schemas... \n")

    # get all json schemas filenames in the target dir
    file_paths = glob.glob(schemas_files_dir)
    print(" - Target Schemas: ", [os.path.basename(x) for x in file_paths])

    # Create json string
    schemas_dict = {}
    for file_path in file_paths:
        file = open(file_path)
        json_body = (file.read())
        file.close()

        # get raw file name from file path
        filename = os.path.basename(file_path)
        mod_name = os.path.splitext(filename)[0]
        schemas_dict[mod_name] = json_body

    output_script = t.render(schemas_dict=schemas_dict)

    with open(output_script_path, 'w') as f:
        f.write(output_script)
        print(f" py schemas module is created: {output_script_path}")

    print("\n Done with py schema modules generation!")


###############################################################################

if __name__ == "__main__":
    main(sys.argv)
