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

from oslo_config import cfg

_validator_opts = [
    cfg.StrOpt(
        "schema",
        short="s",
        required=True,
    ),
    cfg.BoolOpt(
        "resolve-tags",
    ),
    cfg.MultiStrOpt(
        "files",
        positional=True,
    ),
]


def list_opts():
    """Returns a list of config options available in the library.

    The returned list includes all oslo.config options which may be registered
    at runtime by the library.

    Each element of the list is a tuple. The first element is the name of the
    group under which the list of elements in the second element will be
    registered. A group name of None corresponds to the [DEFAULT] group in
    config files.

    The purpose of this is to allow tools like the Oslo sample config file
    generator to discover the options exposed to users by this library.

    :returns: a list of (group_name, opts) tuples
    """
    return [(None, _validator_opts)]


def register_opts(conf):
    """Registers config options to a config object.

    :param conf: an oslo_config.cfg.ConfigOpts object
    """
    for group, opts in list_opts():
        conf.register_cli_opts(opts, group)


def get_config():
    """
    Returns a new config object with registered config options.

    :returns: an oslo_config.cfg.ConfigOpts object
    """
    conf = cfg.ConfigOpts()

    register_opts(conf)

    return conf
