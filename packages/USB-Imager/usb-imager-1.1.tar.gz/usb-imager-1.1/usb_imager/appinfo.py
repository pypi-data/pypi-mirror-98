# -*- coding: utf-8 -*-
"""Project-Info"""

from importlib import resources


__appname__         = "usb-imager"
__version__         = "1.1"
__license__         = "GPLv3"
__copyright__       = "\u00A9 2021"

__description__     = "GUI-Application to write bootable disk images to USB key."
__url_source__      = "https://gitlab.com/skynet-devel/usb-imager"
__url_pip__         = "https://pypi.org/project/USB-Imager"

__author__          = "skynet-devel"
__author_email__    = "skynet-devel@mailbox.org"

__contributors__    = ["Rico (testing)"]

__organisation__    = "Skynet-Research"
__domain__          = "usbimager.app.skynet"

__donation_paypal__ = "skynet-devel@mailbox.org"


def get_app_version() -> str:
    version = "unknown"

    try:
        context_manager = resources.path("resources",
                                         'app_version_git.txt')
    except ModuleNotFoundError:
        context_manager = resources.path("usb_imager.resources",
                                         'app_version_git.txt')

    try:
        with context_manager as version_path:
            with open(version_path) as file:
                version = file.read().strip()
    except FileNotFoundError:
        version = __version__

    return version


# Developer version informations
"""
pathlib >= Python 3.4
pathlib.Path.home() >= Python 3.5
importlib.resources >= 3.7

Accepts a path-like object (Python >= 3.6):
    open()
    os.open()
    os.path.getsize()
"""
