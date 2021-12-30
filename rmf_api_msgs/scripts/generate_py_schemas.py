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
    This will load schema_template, and a list of schemas, then generate and 
    output a schemas.py script locally for pkg installation.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--pkg_dir', required=True,
                    type=str, help='rmf_api_msgs pkg dir')
    args = parser.parse_args(argv[1:])
    pkg_dir = args.pkg_dir

    # open template
    file = open(f"{pkg_dir}/scripts/schemas_template.jinja2")
    schema_template = file.read()
    file.close()

    t = Template(schema_template)
    print("py template for json schema is loaded, now load json schemas... \n")

    # get all json schemas filenames in the target dir
    filenames = [
        os.path.basename(x) for x in glob.glob(f"{pkg_dir}/schemas/*.json")
    ]

    print(" - Target Schemas: " , filenames)

    # Create json string
    schemas_dict = {}
    for file_name in filenames:
        file = open(f"{pkg_dir}/schemas/{file_name}")
        json_body = (file.read())
        file.close()
        mod_name = os.path.splitext(file_name)[0]
        schemas_dict[mod_name] = json_body

    output_script = t.render(schemas_dict=schemas_dict)

    with open(f'{pkg_dir}/rmf_api_msgs/schemas.py', 'w') as f:
        f.write(output_script)

    print("\n Done with py schema modules generation!")


###############################################################################

if __name__ == "__main__":
    main(sys.argv)
