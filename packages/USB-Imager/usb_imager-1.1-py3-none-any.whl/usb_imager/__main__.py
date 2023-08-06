#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""__main__"""

import os
import sys
from PySide2.QtCore import QCoreApplication, Qt
from PySide2.QtWidgets import QApplication

try:
    import appinfo
    from gui_qt import Application
    from modules.udisks2 import UDisks2
    from modules.msgbox import MsgBox
except ImportError:
    # Works for pip installation
    from usb_imager import appinfo
    from usb_imager.gui_qt import Application
    from usb_imager.modules.udisks2 import UDisks2
    from usb_imager.modules.msgbox import MsgBox


def _check_deps() -> None:
    # Check for platform 'linux'
    if not sys.platform.startswith('linux'):
        MsgBox().error("Programm only supports Unix!")
        sys.exit()

    # Check for installed UDisks2/D-Bus
    if not UDisks2.has_udisks2():
        MsgBox().error("UDisks2 was not found!")
        sys.exit()


def main() -> int:
    """Start application"""

    # Check dependencies
    _check_deps()

    # Suppress some Qt logging messages when using QFileDialog
    os.environ["QT_LOGGING_RULES"] = "qt.qpa.*=false;kf.kio.*=false"

    # Build application
    app = QApplication.instance()
    if app is None:
        # Application settings
        QApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        # print(QStyleFactory.keys())
        # QApplication.setStyle('Fusion')

        QCoreApplication.setApplicationName("USB-Imager")
        QCoreApplication.setApplicationVersion(appinfo.get_app_version())
        QCoreApplication.setOrganizationName(appinfo.__organisation__)
        QCoreApplication.setOrganizationDomain(appinfo.__domain__)

        app = Application(sys.argv)

    # Execute application
    app.show_mainwindow()

    return app.exec_()


if __name__ == "__main__":
    main()
