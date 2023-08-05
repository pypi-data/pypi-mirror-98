try:
    # pylint: disable=unused-import
    from PySide6 import QtCore, QtGui, QtWidgets
    from PySide6.QtGui import QAction
except ImportError:
    from PySide2 import QtCore, QtGui, QtWidgets  # type: ignore
    from PySide2.QtWidgets import QAction  # type: ignore
