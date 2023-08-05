#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2020-2021 Alibaba Group Holding Limited.
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

from .version import __version__

import logging
import os
import traceback


def _init_global_context():
    import os as _dl_flags
    import sys

    if not hasattr(_dl_flags, 'RTLD_GLOBAL') or not hasattr(_dl_flags, 'RTLD_LAZY'):
        try:
            # next try if DLFCN exists
            import DLFCN as _dl_flags
        except ImportError:
            _dl_flags = None

    if _dl_flags is not None:
        old_flags = sys.getdlopenflags()

        # import the extension module
        sys.setdlopenflags(_dl_flags.RTLD_GLOBAL | _dl_flags.RTLD_LAZY)
        from . import _C

        # See Note [Import pyarrow before _C]
        sys.setdlopenflags(_dl_flags.RTLD_GLOBAL | _dl_flags.RTLD_LAZY)
        import pyarrow
        del pyarrow

        # restore
        sys.setdlopenflags(old_flags)


if os.environ.get('VINEYARD_DEV', None) is not None:
    _init_global_context()
del _init_global_context


from ._C import connect, IPCClient, RPCClient, \
    Object, ObjectBuilder, ObjectID, ObjectName, ObjectMeta, \
    InstanceStatus, Blob, BlobBuilder
from ._C import ArrowErrorException, \
    AssertionFailedException, \
    ConnectionErrorException, \
    ConnectionFailedException, \
    EndOfFileException, \
    EtcdErrorException, \
    IOErrorException, \
    InvalidException, \
    InvalidStreamStateException, \
    KeyErrorException, \
    MetaTreeInvalidException, \
    MetaTreeLinkInvalidException, \
    MetaTreeNameInvalidException, \
    MetaTreeNameNotExistsException, \
    MetaTreeSubtreeNotExistsException, \
    MetaTreeTypeInvalidException, \
    MetaTreeTypeNotExistsException, \
    NotEnoughMemoryException, \
    NotImplementedException, \
    ObjectExistsException, \
    ObjectNotExistsException, \
    ObjectNotSealedException, \
    ObjectSealedException, \
    StreamDrainedException, \
    StreamFailedException, \
    TypeErrorException, \
    UnknownErrorException, \
    UserInputErrorException, \
    VineyardServerNotReadyException

from . import _vineyard_docs
del _vineyard_docs

from .core import default_builder_context, default_resolver_context, default_driver_context
from .data import register_builtin_types
from .data.graph import Graph

logger = logging.getLogger('vineyard')


def _init_vineyard_modules():
    ''' Resolve registered vineyard modules in the following order:

        * /etc/vineyard/config.py
        * {sys.prefix}/etc/vineyard/config.py
        * /usr/share/vineyard/01-xxx.py
        * /usr/local/share/vineyard/01-xxx.py
        * {sys.prefix}/share/vineyard/02-xxxx.py
        * $HOME/.vineyard/03-xxxxx.py

        Then import packages like vineyard.drivers.*:

        * vineyard.drivers.io
    '''

    import glob
    import importlib.util
    import os
    import pkgutil
    import site
    import sys
    import sysconfig

    def _import_module_from_file(filepath):
        filepath = os.path.expanduser(os.path.expandvars(filepath))
        if os.path.exists(filepath):
            try:
                spec = importlib.util.spec_from_file_location("vineyard._contrib", filepath)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
            except Exception as e:  # pylint: disable=broad-except
                logger.debug("Failed to load %s: %s\n%s", filepath, e, traceback.format_exc())

    def _import_module_from_qualified_name(module):
        try:
            importlib.import_module(module)
        except Exception as e:
            logger.debug('Failed to load module %s: %s\n%s', module, e, traceback.format_exc())

    _import_module_from_file('/etc/vineyard/config.py')
    _import_module_from_file(os.path.join(sys.prefix, '/etc/vineyard/config.py'))
    for filepath in glob.glob('/usr/share/vineyard/*-*.py'):
        _import_module_from_file(filepath)
    for filepath in glob.glob('/usr/local/share/vineyard/*-*.py'):
        _import_module_from_file(filepath)
    for filepath in glob.glob(os.path.join(sys.prefix, '/share/vineyard/*-*.py')):
        _import_module_from_file(filepath)
    for filepath in glob.glob(os.path.expanduser('$HOME/.vineyard/*-*.py')):
        _import_module_from_file(filepath)

    package_sites = set()
    pkg_sites = site.getsitepackages()
    if not isinstance(pkg_sites, (list, tuple)):
        pkg_sites = [pkg_sites]
    package_sites.update(pkg_sites)
    pkg_sites = site.getusersitepackages()
    if not isinstance(pkg_sites, (list, tuple)):
        pkg_sites = [pkg_sites]
    package_sites.update(pkg_sites)

    paths = sysconfig.get_paths()
    if 'purelib' in paths:
        package_sites.add(paths['purelib'])
    if 'platlib' in paths:
        package_sites.add(paths['purelib'])

    # add relative path
    package_sites.add(os.path.join(os.path.dirname(__file__), '..'))

    # dedup
    deduped = set()
    for pkg_site in package_sites:
        deduped.add(os.path.abspath(pkg_site))

    for pkg_site in deduped:
        for _, mod, _ in pkgutil.iter_modules([os.path.join(pkg_site, 'vineyard', 'drivers')]):
            _import_module_from_qualified_name('vineyard.drivers.%s' % mod)


try:
    _init_vineyard_modules()
except:
    pass
del _init_vineyard_modules
