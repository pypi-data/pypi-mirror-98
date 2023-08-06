# -*- coding: utf-8 -*-
##########################################################################
# NSAp - Copyright (C) CEA, 2019
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

"""
This module checks that all the dependencies are installed properly.
"""

# System import
import logging
import importlib
import distutils

# Package import
from .info import __version__
from .info import REQUIRES
from .info import LICENSE
from .info import AUTHOR
from .utils import logo


# Global parameters
MAP = {
    "progressbar2": "progressbar",
    "scikit-learn": "sklearn",
    "Pillow": "PIL",
    "scikit-image": "skimage"
}
logger = logging.getLogger("pynet")


def _check_python_versions():
    """ Check that all the Python dependencies are satisfied.

    A dependency is expected to be formatted as follows:
    <mod_name>>==<mod_min_version>
    <mod_name>>>=<mod_min_version>

    Returns
    -------
    versions: dict with 2-uplet
        the minimum required version and the installed version for each module.
        '?' means no package found.
    """
    versions = {}
    logger.debug("Checking install dependencies:")
    logger.debug("Declared dependencies:\n{0}".format(REQUIRES))
    for dependency in REQUIRES:
        if ">=" in dependency:
            operator = ">="
        elif "==" in dependency:
            operator = "=="
        else:
            raise ValueError("'{0}' dependency no formatted correctly.".format(
                dependency))
        mod_name, mod_min_version = dependency.split(operator)
        if mod_name in MAP:
            mod_name = MAP[mod_name]
        logger.debug("  {0} {1} {2}.".format(
            mod_name, operator, mod_min_version))
        try:
            mod_install_version = importlib.import_module(mod_name).__version__
        except:
            mod_install_version = "?"
        logger.debug("  found {0}...".format(mod_install_version))
        versions[mod_name] = (operator + mod_min_version, mod_install_version)
    logger.debug("Check done.")
    return versions


def info():
    """ Dispaly some usefull information about the package.

    Returns
    -------
    info: str
        package information.
    """
    logger.debug("Check module metadata & dependencies:")
    logger.debug("  dependencies.")
    dependencies = "Dependencies: \n\n"
    dependencies_info = _check_python_versions()
    for name, (min_version, install_version) in dependencies_info.items():
        dependencies += "{0:15s}: {1:9s} - required | {2:9s} installed".format(
            name, min_version, install_version)
        dependencies += "\n"
    logger.debug("  metadata.")
    version = "Package version: {0}\n\n".format(__version__)
    license = "License: {0}\n\n".format(LICENSE)
    authors = "Authors: \n{0}\n".format(AUTHOR)
    return logo() + "\n\n" + version + license + authors + dependencies
