
# Style Sheet Classes
class StyleSheets:
  def __init__(self):
    self.styleSheet = ""
    self.styleSheet += "QWidget { background-color: #353535; color: white; }"
    self.styleSheet += "QLabel { background-color: transparent; color: white; }"
    self.styleSheet += "QPushButton { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
    self.styleSheet += "QPushButton:hover { background-color: #303030; color: white; }"
    self.styleSheet += "QFrame { background-color: #353535; color: white; border: 1px solid #202020; border-radius: 5px; }"
    self.styleSheet += "QListWidget { background-color: transparent; color: white; border: 0px; }"
    self.styleSheet += "QListWidget::item { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
    self.styleSheet += "QListWidget::item:selected { background-color: #303030; color: white; border: 1px solid #303030; border-radius: 5px; }"
    self.styleSheet += "QListWidget::item:hover { background-color: #303030; color: white; border: 1px solid #303030; border-radius: 5px; }"
    self.styleSheet += "QListWidget::item:selected:hover { background-color: #404040; color: white; border: 1px solid #404040; border-radius: 5px; }"
    self.styleSheet += "QSizeGrip { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
    self.styleSheet += "QSizeGrip:hover { background-color: #303030; color: white; }"
    self.styleSheet += "QSizeGrip:pressed { background-color: #404040; color: white; }"
    self.styleSheet += "QSizeGrip:active { background-color: #404040; color: white; }"
    self.styleSheet += "QSizeGrip:off { background-color: #202020; color: white; }"
    self.styleSheet += "QSizeGrip:on { background-color: #303030; color: white; }"
  def getStyleSheet(self, objType):
    retStyleSheet = ""
    if objType == "x":
      retStyleSheet += "QPushButton { background-color: #350000; color: white; border: 1px solid #202020; border-radius: 5px; }"
      retStyleSheet += "QPushButton:hover { background-color: #501010; color: white; }"
      retStyleSheet += "QPushButton:pressed { background-color: #703535; color: white; }"
      retStyleSheet += "QPushButton:active { background-color: #703535; color: white; }"
      retStyleSheet += "QPushButton:off { background-color: #350000; color: white; }"
    elif objType == "statusButton":
      retStyleSheet += "QPushButton { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
      retStyleSheet += "QPushButton:hover { background-color: #303030; color: white; }"
      retStyleSheet += "QPushButton:pressed { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:active { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:off { background-color: #202020; color: white; }"
    elif objType == "icon":
      retStyleSheet += "QLabel { background-color: transparent; color: white; }"
    elif objType == "header":
      retStyleSheet += "QLabel { background-color: transparent; color: white; }"
    elif objType == "description":
      retStyleSheet += "QLabel { background-color: transparent; color: white; }"
    elif objType == "statusButton":
      retStyleSheet += "QPushButton { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
      retStyleSheet += "QPushButton:hover { background-color: #303030; color: white; }"
      retStyleSheet += "QPushButton:pressed { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:active { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:off { background-color: #202020; color: white; }"
    elif objType == "priorityButton":
      retStyleSheet += "QPushButton { background-color: #202020; color: white; border: 1px solid #202020; border-radius: 5px; }"
      retStyleSheet += "QPushButton:hover { background-color: #303030; color: white; }"
      retStyleSheet += "QPushButton:pressed { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:active { background-color: #404040; color: white; }"
      retStyleSheet += "QPushButton:off { background-color: #202020; color: white; }"
    else:
      retStyleSheet += "QLabel { background-color: transparent; color: white; }"



    return retStyleSheet