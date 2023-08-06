#    Copyright 2021 Moisés Guimarães de Medeiros
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import sys

import cerberus
import yaml

from cerberus_cli import config


def main():
    status = 0
    new_line = "\n\t"
    conf = config.get_config()

    conf(project="cerberus")

    if not conf.resolve_tags:
        yaml.SafeLoader.add_multi_constructor(
            "!",
            lambda loader, suffix, node: loader.construct_mapping(node)
        )

    with open(conf.schema, "r") as fd:
        schema = yaml.safe_load(fd)

    validator = cerberus.Validator(schema)

    for fname in conf.files:
        with open(fname, "r") as fd:
            if not validator.validate(yaml.safe_load(fd)):
                print(fname)
                for k, e in validator.errors.items():
                    print(f"{k}:{new_line}{new_line.join(e)}")
                status = 1

    sys.exit(status)


if __name__ == "__main__":
    main()
