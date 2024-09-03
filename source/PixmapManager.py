
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class PixmapManager:
  def __init__( self, rootPath ):
    self.imageRootPath = rootPath
    self.pixmapCache = {}
    self.imagePaths = {}
    self.iconPaths = {}

  def addIconPaths(self, pathLabel, iconPaths):
    self.iconPaths[pathLabel] = iconPaths
  
  def loadIcon(self, pathLabel, iconName):
    if pathLabel in self.iconPaths:
      if iconName in self.iconPaths[pathLabel]:
        imagePath = self.iconPaths[pathLabel][iconName]
        return self.loadPixmap(imagePath)
    return None

  def loadPixmap(self, imagePath):
    if imagePath in self.pixmapCache:
      return self.pixmapCache[imagePath]
    else:
      pixmap = QPixmap(imagePath)
      self.pixmapCache[imagePath] = pixmap
      return pixmap

  def resizePixmap(self, imagePath, width, height):
    pixmap = self.loadPixmap(imagePath)
    resizedPixmap = pixmap.scaled(width, height, Qt.AspectRatioMode.KeepAspectRatio)
    return resizedPixmap

  def addImagePath(self, iconName, imagePath):
    self.imagePaths[iconName] = imagePath

  def getPixmapByIconName(self, iconName):
    if iconName in self.imagePaths:
      imagePath = self.imagePaths[iconName]
      return self.loadPixmap(imagePath)
    else:
      return None