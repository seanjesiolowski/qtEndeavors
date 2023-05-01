from PySide6.QtGui import QFont


def heading_font():
    heading_font = QFont()
    heading_font.setPointSize(20)
    heading_font.setBold(True)
    return heading_font
