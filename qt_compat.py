"""Compatibilidad con PySide6."""
try:
    from PySide6 import QtWidgets, QtCore, QtGui
except ImportError as exc:
    raise SystemExit("Falta PySide6: instala dependencias con ejecutar.bat") from exc

Qt = QtCore.Qt
AlignmentFlag = Qt.AlignmentFlag
