from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class EditTaskWidget(QWidget):
  def __init__(self, task, pixmapManager):
    super().__init__()
    self.pixmapManager = pixmapManager

    self.data = task

    self.initUI()

  def initUI(self):
    typeIcon = self.pixmapManager.loadIcon( "type", self.data['type']  )
    statusIcon = self.pixmapManager.loadIcon( "status", self.data['status'] )
    priorityIcon = self.pixmapManager.loadIcon( "priority", self.data['priority'] )

    # Create the layout for the widget
    mainLayout = QVBoxLayout()

    # First row: Icon, header, status, and priority
    firstRowLayout = QHBoxLayout()

    iconLabel = QLabel()
    iconLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    iconLabel.setPixmap(typeIcon.scaled(32, 32))
    firstRowLayout.addWidget(iconLabel)

    headerLabel = QLabel(self.data['header'])
    headerLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")

    firstRowLayout.addWidget(headerLabel)

    statusIconLabel = QLabel()
    statusIconLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    statusIconLabel.setPixmap(statusIcon.scaled(24, 24))
    firstRowLayout.addWidget(statusIconLabel)

    priorityIconLabel = QLabel()
    priorityIconLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    priorityIconLabel.setPixmap(priorityIcon.scaled(24, 24))
    firstRowLayout.addWidget(priorityIconLabel)
    mainLayout.addLayout(firstRowLayout)

    # Second row: Description
    descriptionLabel = QLabel(self.data['description'])
    descriptionLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    mainLayout.addWidget(descriptionLabel)

    # Third row: Timer display and button
    thirdRowLayout = QHBoxLayout()
    timerLabel = QLabel(self.data['time'])
    thirdRowLayout.addWidget(timerLabel)
    timerButton = QPushButton("Start/Stop")
    thirdRowLayout.addWidget(timerButton)
    mainLayout.addLayout(thirdRowLayout)

    self.setLayout(mainLayout)