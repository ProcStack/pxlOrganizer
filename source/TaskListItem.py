from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

class TaskListItem(QWidget):
  def __init__(self, pixmapManager, typeIcon, header, description, statusIcon, priorityIcon):
    super().__init__()
    self.pixmapManager = pixmapManager
    self.data = {
      'type': typeIcon,
      'header': header,
      'description': description,
      'status': statusIcon,
      'priority': priorityIcon
    }

    self.initUI()

  def initUI(self):
    self.setContentsMargins(0, 0, 0, 0)
    self.setStyleSheet("border: 1px solid #202020; background-color: transparent;  color: white; border-radius: 5px;")

    typeIcon = self.pixmapManager.loadIcon( "type", self.data['type']  )
    statusIcon = self.pixmapManager.loadIcon( "status", self.data['status'] )
    priorityIcon = self.pixmapManager.loadIcon( "priority", self.data['priority'] )

    # Create the layout for the item
    itemLayout = QHBoxLayout()
    itemLayout.setContentsMargins(0, 0, 0, 0)

    # Column 1: Icon
    iconLabel = QLabel()
    iconLabel.setStyleSheet("border: 0px; background-color: transparent;  color: white;")
    iconLabel.setPixmap(typeIcon.scaled(32, 32))
    itemLayout.addWidget(iconLabel)

    # Column 2: Header and Description
    headerLayout = QVBoxLayout()
    headerLabel = QLabel(self.data['header'])
    headerLabel.setStyleSheet("border: 0px; background-color: transparent;  color: white;")
    descriptionLabel = QLabel(self.data['description'])
    descriptionLabel.setStyleSheet("border: 0px; background-color: transparent;  color: white;")
    headerLayout.addWidget(headerLabel)
    headerLayout.addWidget(descriptionLabel)
    itemLayout.addLayout(headerLayout)

    # Column 3: Icons
    iconsLayout = QHBoxLayout()

    statusIconLabel = QLabel()
    statusIconLabel.setPixmap(statusIcon.scaled(24, 24))
    priorityIconLabel = QLabel()
    priorityIconLabel.setPixmap(priorityIcon.scaled(24, 24))
    iconsLayout.addWidget(statusIconLabel)
    iconsLayout.addWidget(priorityIconLabel)
    itemLayout.addLayout(iconsLayout)

    # Set the layout for the item
    self.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Fixed)
    self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Fixed)

    self.setLayout(itemLayout)
