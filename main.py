###
#
# Title: Task Organizer :: 0.1.0
# Author: Kevin Edzenga; Frayed Fables LLC.
# Date: 2024-09-02
# Description: A task organizer with a list of tasks, notes, ideas, bugs, email needs, and more.
#
# Reasoning? I seem to get overwhelmed when it comes to the litany of input sources of notifications and rate of notifications.
# If I don't want to open my email because of how my email client provides the emails to me, then business is going to fail.
# "Too much, its too much!" - Arin (egoraptor) Hanson of Game Grumps
#
# So, if I can't bring myself to do menial tasks without some weirdly implicit level of stress simply from opening the program,
#   Then I need to do something about that for myself.
#
# Hide email counts, adress emails quickly.
# Tasks should only show up when they are due without a notification that they are due, unless a critical deadline.
# Some potential pavlovian response to the sound of a notifications, want to always stretch and stand at a certain time, then do it at a ding.
#
# I know, there are 1001 different task managers out there, 
#   But if my brain doesn't seem to align well with them, then I need to make my own.
#
# Plus visually seeing how long you've been working in a day is way easier than some mental guestimation.
#
###

import os, sys, atexit
from datetime import datetime, timezone, timedelta
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QListWidget, QListWidgetItem, QSizePolicy, QFrame, QSizeGrip, QSpacerItem, QComboBox, QLineEdit, QTextEdit
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, QUrl, pyqtSlot
from PyQt6.QtMultimedia import QSoundEffect
from PyQt6.QtGui import QMouseEvent, QKeyEvent

from source.PixmapManager import PixmapManager
from source.ExtraNote import ExtraNote 
from source.TaskListManager import TaskListManager
#from source.TaskListItem import TaskListItem
#from source.EditTaskWidget import EditTaskWidget

extra_noteKeys = ['text', 'time', 'url']

script_dir = os.path.dirname(os.path.abspath(__file__))
image_rootPath = os.path.join( script_dir, "assets", "images" )
sound_rootPath =  os.path.join( script_dir, "assets", "sounds" )
backup_path = "backups"
save_fileName = "taskList.json"
save_taskData = "taskData"
backup_path = os.path.join(backup_path, "taskList.json")
backup_frequency = 24 * 60 * 60  # 24 hours

# Caution, running two instances will stomp on each other's feet when saving
runLockCheck = True

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



class ITEM_TYPE:
  TASK = 0
  ALARM = 1
  TODO = 2
  NOTE = 3
  IDEA = 4
  EVENT = 5
  EMAIL = 6
  BUG = 7
  DOCUMENT = 8
  SOCIAL_MEDIA = 9

class ITEM_STATUS:
  INIT = 0
  IN_PROGRESS = 1
  PAUSED = 2
  BLOCKED = 3
  DONE = 4

class ITEM_PRIORITY:
  TIMELESS = 0
  TRIVIAL = 1
  LOW = 2
  MEDIUM = 3
  HIGH = 4
  CRITICAL = 5

# Dictionary for ITEM_TYPE icons
typeDir_name = "type"
type_icons = {
  ITEM_TYPE.TASK : os.path.join(image_rootPath, typeDir_name, "task.png"),
  ITEM_TYPE.ALARM : os.path.join(image_rootPath, typeDir_name, "alarm.png"),
  ITEM_TYPE.NOTE : os.path.join(image_rootPath, typeDir_name, "note.png"),
  ITEM_TYPE.IDEA : os.path.join(image_rootPath, typeDir_name, "idea.png"),
  ITEM_TYPE.EVENT : os.path.join(image_rootPath, typeDir_name, "event.png"),
  ITEM_TYPE.EMAIL : os.path.join(image_rootPath, typeDir_name, "email.png"),
  ITEM_TYPE.BUG : os.path.join(image_rootPath, typeDir_name, "bug.png"),
  ITEM_TYPE.DOCUMENT : os.path.join(image_rootPath, typeDir_name, "document.png"),
  ITEM_TYPE.SOCIAL_MEDIA : os.path.join(image_rootPath, typeDir_name, "socialMedia.png")
}

# Dictionary for ITEM_STATUS icons
statusDir_name = "status"
status_icons = {
  ITEM_STATUS.INIT : os.path.join(image_rootPath, statusDir_name, "init.png"),
  ITEM_STATUS.IN_PROGRESS : os.path.join(image_rootPath, statusDir_name, "inProgress.png"),
  ITEM_STATUS.PAUSED : os.path.join(image_rootPath, statusDir_name, "paused.png"),
  ITEM_STATUS.BLOCKED : os.path.join(image_rootPath, statusDir_name, "blocked.png"),
  ITEM_STATUS.DONE : os.path.join(image_rootPath, statusDir_name, "done.png")
}

# Dictionary for ITEM_PRIORITY icons
priorityDir_name = "priority"
priority_icons = {
  ITEM_PRIORITY.TIMELESS : os.path.join(image_rootPath, priorityDir_name, "timeless.png"),
  ITEM_PRIORITY.TRIVIAL : os.path.join(image_rootPath, priorityDir_name, "trivial.png"),
  ITEM_PRIORITY.LOW : os.path.join(image_rootPath, priorityDir_name, "low.png"),
  ITEM_PRIORITY.MEDIUM : os.path.join(image_rootPath, priorityDir_name, "medium.png"),
  ITEM_PRIORITY.HIGH : os.path.join(image_rootPath, priorityDir_name, "high.png"),
  ITEM_PRIORITY.CRITICAL : os.path.join(image_rootPath, priorityDir_name, "critical.png")
}


## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



default_extra_note = ExtraNote("Default Note", "2024-09-02;12:01pm", "frayed-fables.com")



default_data = {
  'status': ITEM_STATUS.INIT,
  'type': ITEM_TYPE.TASK,
  'priority': ITEM_PRIORITY.MEDIUM,
  'header': 'Task 1',
  'description': 'This is a task',
  'date': '',
  'time': '0:00:00:00',
  'creationTime': '2024-09-00;12:01pm',
  'lastModified': '2024-09-00;12:01pm',
  'deadline': '2024-09-00;12:01pm',
  'notes': None
}


default_test_data = {
  'tasks': [
    {
      'status': ITEM_STATUS.INIT,
      'type': ITEM_TYPE.TASK,
      'priority': ITEM_PRIORITY.MEDIUM,
      'header': 'Task 1',
      'description': 'This is a task',
      'date': '',
      'time': '0:00:00:00',
      'creationTime': '2024-09-00;12:01pm',
      'lastModified': '2024-09-00;12:01pm',
      'deadline': '2024-09-00;12:01pm',
      'notes': [
         ExtraNote("-Default Note-", "2024-09-02;12:01pm", "http://frayed-fables.com")
      ]
    },
    {
      'status': ITEM_STATUS.IN_PROGRESS,
      'type': ITEM_TYPE.NOTE,
      'priority': ITEM_PRIORITY.CRITICAL,
      'header': 'TODO',
      'description': 'Work out the Flib Flubs!',
      'date': '',
      'time': '0:00:00:00',
      'creationTime': '2024-09-00;12:01pm',
      'lastModified': '2024-09-00;12:01pm',
      'deadline': '2024-09-00;12:01pm',
      'notes': [
         ExtraNote("-Test Note 2-", "2024-09-02;12:58pm", "http://frayed-fables.com")
      ]
    }
  ]
}




## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



# Verify if task organizer can open or not,
#   If there is a .lock file, then pxlOrganizer is already running some somewhere.
TaskManager = TaskListManager( os.path.join(script_dir,"taskList.json"), extra_noteKeys, backup_path, backup_frequency)
if runLockCheck:
  if not TaskManager.lockTaskFile():
    print("Error: Lock file already exists-")
    print("  "+TaskManager.lockPath)
    print("Another instance may be running, please check your other command prompts or Task Manager.")
    print("  Exiting...")
    sys.exit()
  else:
    print("Lock file created successfully.")

TaskManager.importData()
#TaskManager.data = default_test_data
#TaskManager.exportData()




## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



class EditTaskWidget(QWidget):
  def __init__(self, task, pixmapManager):
    super().__init__()
    self.pixmapManager = pixmapManager

    self.active = False

    self.iconSize = 32
    self.statusSize = 24
    self.prioritySize = 24

    self.data = task

    self.iconLabel = None
    self.headerLabel = None
    self.descriptionLabel = None 
    self.statusIcon = None
    self.priorityIcon = None
    self.timerLabel = None
    self.timerButton = None

    self.initUI()

  def initUI(self):
    typeIcon = self.pixmapManager.loadIcon( "type", self.data['type']  )
    statusIcon = self.pixmapManager.loadIcon( "status", self.data['status'] )
    priorityIcon = self.pixmapManager.loadIcon( "priority", self.data['priority'] )

    # Create the layout for the widget
    mainLayout = QVBoxLayout()

    # First row: Icon, header, status, and priority
    firstRowLayout = QHBoxLayout()

    self.iconLabel = QLabel()
    self.iconLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    self.iconLabel.setPixmap(typeIcon.scaled(self.iconSize, self.iconSize))
    firstRowLayout.addWidget(self.iconLabel)

    self.headerLabel = QLabel(self.data['header'])
    self.headerLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")

    firstRowLayout.addWidget(self.headerLabel)

    self.statusIcon = QLabel()
    self.statusIcon.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    self.statusIcon.setPixmap(statusIcon.scaled(self.statusSize, self.statusSize))
    firstRowLayout.addWidget(self.statusIcon)

    self.priorityIcon = QLabel()
    self.priorityIcon.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    self.priorityIcon.setPixmap(priorityIcon.scaled(self.prioritySize, self.prioritySize))
    firstRowLayout.addWidget(self.priorityIcon)
    mainLayout.addLayout(firstRowLayout)

    # Second row: Description
    self.descriptionLabel = QLabel(self.data['description'])
    self.descriptionLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    mainLayout.addWidget(self.descriptionLabel)

    # Third row: Timer display and button
    thirdRowLayout = QHBoxLayout()
    self.timerLabel = QLabel(self.data['time'])
    thirdRowLayout.addWidget(self.timerLabel)
    self.timerButton = QPushButton("Start/Stop")
    thirdRowLayout.addWidget(self.timerButton)
    mainLayout.addLayout(thirdRowLayout)

    self.setLayout(mainLayout)

  def displayTask(self, taskListItem):
    self.data = taskListItem.data
    self.iconLabel.setPixmap(self.pixmapManager.loadIcon( "type", self.data['type']  ).scaled(self.iconSize, self.iconSize))
    self.headerLabel.setText(self.data['header'])
    self.descriptionLabel.setText(self.data['description'])
    self.statusIcon.setPixmap(self.pixmapManager.loadIcon( "status", self.data['status'] ).scaled(self.statusSize, self.statusSize))
    self.priorityIcon.setPixmap(self.pixmapManager.loadIcon( "priority", self.data['priority'] ).scaled(self.prioritySize, self.prioritySize))
    self.timerLabel.setText(self.data['time'])

    


## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --


class TaskListItem(QWidget):
  def __init__(self, pixmapManager, taskData):
    super().__init__()
    self.pixmapManager = pixmapManager
    self.data = taskData

    self.iconSize = 32
    self.statusSize = 24
    self.prioritySize = 24

    self.iconLabel = None
    self.headerLable = None
    self.descriptionLabel = None
    self.statusWidget = None
    self.statusLabel = None
    self.priorityWidget = None
    self.priorityLabel = None

    self.initUI()

  def initUI(self):
    self.setContentsMargins(0, 0, 0, 0)
    self.setStyleSheet("border: 1px solid #202020; background-color: transparent;  color: white; border-radius: 5px;")
    self.setStyleSheet("border: 0px; color: white; padding: 0px;")

    typeIcon = self.pixmapManager.loadIcon( "type", self.data['type']  )
    statusIcon = self.pixmapManager.loadIcon( "status", self.data['status'] )
    priorityIcon = self.pixmapManager.loadIcon( "priority", self.data['priority'] )

    # Create the layout for the item
    taskItemLayout = QHBoxLayout()
    taskItemLayout.setContentsMargins(0, 0, 0, 0)

    # Create a widget to hold the centered contents
    self.iconWidget, self.iconLabel = self.addCenteredWidget(typeIcon, self.iconSize)
    taskItemLayout.addWidget( self.iconWidget )

    # Column 2: Header and Description

    taskInfoWidget = QWidget()
    taskInfoWidget.setStyleSheet("background-color: transparent;")
    taskInfoWidget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    headerLayout = QVBoxLayout()
    headerLayout.setContentsMargins(0, -3, 0, 1)
    self.headerLabel = QLabel(self.data['header'])
    self.headerLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    self.descriptionLabel = QLabel(self.data['description'])
    self.descriptionLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    headerLayout.addWidget(self.headerLabel)
    headerLayout.addWidget(self.descriptionLabel)
    taskInfoWidget.setLayout(headerLayout)
    taskItemLayout.addWidget(taskInfoWidget)

    # Column 3: Icons
    
    self.statusWidget, self.statusLabel = self.addCenteredWidget(statusIcon, self.statusSize)
    taskItemLayout.addWidget( self.statusWidget )

    self.priorityWidget, self.priorityLabel = self.addCenteredWidget(priorityIcon, self.statusSize)
    taskItemLayout.addWidget( self.priorityWidget )

    # Set the layout for the item
    self.sizePolicy().setVerticalPolicy(QSizePolicy.Policy.Fixed)
    self.sizePolicy().setHorizontalPolicy(QSizePolicy.Policy.Fixed)

    self.setLayout(taskItemLayout)

  def addCenteredWidget(self, pix, pixSize):
    # Create a widget to hold the centered contents
    curWidget = QWidget()
    curWidget.setStyleSheet("background-color: transparent;")

    # Create a layout for the centered contents
    centeredIconLayout = QVBoxLayout()
    centeredIconLayout.setContentsMargins(0, 0, 0, 0)
    centeredIconLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

    curLabel = QLabel()
    curLabel.setStyleSheet("border: 0px solid black; background-color: transparent;  color: white;")
    curLabel.setPixmap(pix.scaled(pixSize, pixSize))
    curLabel.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    curLabel.resize(pixSize, pixSize)
    curLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
    centeredIconLayout.addWidget(curLabel)
    curWidget.setLayout(centeredIconLayout)

    return curWidget, curLabel

  def setIconPadding(self, padding):
    self.iconWidget.resize(padding, padding)
    iconPadding = (padding-self.iconSize) // 2
    self.iconLabel.setContentsMargins(5, iconPadding, 0, iconPadding)

    statusPadding = (padding-self.statusSize) // 2
    self.statusLabel.setContentsMargins(0, statusPadding, 0, statusPadding)

    priorityPadding = (padding-self.prioritySize) // 2
    self.priorityLabel.setContentsMargins(0, priorityPadding, 5, priorityPadding)



## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --



class PromptWindow(QWidget):
  def __init__(self, parent=None, previousType="Task"):
    super().__init__(parent)
    self.type=ITEM_TYPE.TASK
    self.header = ""
    self.description = ""
    self.status = ITEM_STATUS.INIT
    self.priority = ITEM_PRIORITY.MEDIUM
    self.time = "0:00:00:00"
    self.creationTime = parent.GetDateTime()
    self.lastModified = parent.GetDateTime()
    self.deadline = parent.GetDateTime(7)

    self.data = default_data.copy()
    self.data['notes'] = []

    self.dragPos = QPoint()


    self.typeDropdown = None
    self.priorityDropdown = None

    self.initUI()

  def initUI(self):
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    self.setStyleSheet("background-color: transparent;")
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    self.setFixedSize(300, 400)

    parentSize = QSize(self.parent().geometry().width(), self.parent().geometry().height())
    moveX = (parentSize.width() - self.rect().width()) // 2
    moveY = (parentSize.height() - self.rect().height()) // 2
    self.move(moveX, moveY)


    mainLayout = QVBoxLayout()
    mainLayout.setContentsMargins(0, 0, 0, 0)

    # Frame with border and rounded corners
    frame = QFrame(self)
    frame.setStyleSheet("border: 1px solid black; background-color: #353535;  color: white; border-radius: 10px;")
    frameLayout = QVBoxLayout(frame)

    # Custom top bar
    topBar = QHBoxLayout()

    # Create dropdown for Task type
    self.typeDropdown = QComboBox()
    self.typeDropdown.addItem("Task")
    self.typeDropdown.addItem("Alarm")
    self.typeDropdown.addItem("Todo")
    self.typeDropdown.addItem("Note")
    self.typeDropdown.addItem("Idea")
    self.typeDropdown.addItem("Event")
    self.typeDropdown.addItem("Email")
    self.typeDropdown.addItem("Bug")
    self.typeDropdown.addItem("Document")
    self.typeDropdown.addItem("Social Media")
    topBar.addWidget(self.typeDropdown)

    # Create dropdown for Priority type
    self.priorityDropdown = QComboBox()
    self.priorityDropdown.addItem("Timeless")
    self.priorityDropdown.addItem("Trivial")
    self.priorityDropdown.addItem("Low")
    self.priorityDropdown.addItem("Medium")
    self.priorityDropdown.addItem("High")
    self.priorityDropdown.addItem("Critical")
    topBar.addWidget(self.priorityDropdown)
    self.priorityDropdown.setCurrentIndex(3)  # Set the default selected option to the fourth item
    


    # Create editable text entries for Header and Description
    self.headerEntry = QLineEdit()
    self.headerEntry.setPlaceholderText("Enter header")
    self.headerEntry.textChanged.connect(self.updateHeader)

    self.descriptionEntry = QTextEdit()
    self.descriptionEntry.setPlaceholderText("Enter description")
    self.descriptionEntry.textChanged.connect(self.updateDescription)

    # Buttons
    buttonLayout = QHBoxLayout()

    newButton = QPushButton("New Task")
    newButton.clicked.connect(lambda: self.buttonClicked("New Task"))
    buttonLayout.addWidget(newButton)

    cancelButton = QPushButton("Cancel")
    cancelButton.clicked.connect(lambda: self.buttonClicked("Cancel"))
    buttonLayout.addWidget(cancelButton)

    # Add layouts to frame layout
    frameLayout.addLayout(topBar)
    frameLayout.addWidget(self.headerEntry)
    frameLayout.addWidget(self.descriptionEntry)
    frameLayout.addLayout(buttonLayout)

    mainLayout.addWidget(frame)
    self.setLayout(mainLayout)

  def mousePressEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
      self.dragPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
      event.accept()

  def mouseMoveEvent(self, event: QMouseEvent):
    if event.buttons() == Qt.MouseButton.LeftButton:
      self.move(event.globalPosition().toPoint() - self.dragPos)
      event.accept()

  def updateHeader(self):
    self.header = self.headerEntry.text()
    self.data['header'] = self.headerEntry.text()

  def updateDescription(self):
    self.description = self.descriptionEntry.toPlainText()
    self.data['description'] = self.descriptionEntry.toPlainText()

  def buttonClicked(self, buttonName):
    toType = self.typeDropdown.currentText()
    self.data['type'] = self.typeDropdown.currentIndex()
    self.data['priority'] = self.priorityDropdown.currentIndex()

    if buttonName == "Cancel":
      toType = "Cancel"
    self.parent().handlePromptButton(toType, self.data)
    self.close()





class TaskOrganizer(QWidget):
  def __init__(self):
    super().__init__( )
    self.pixmapManager = PixmapManager( image_rootPath )
    self.pixmapManager.addIconPaths( "type", type_icons )
    self.pixmapManager.addIconPaths( "status", status_icons )
    self.pixmapManager.addIconPaths( "priority", priority_icons )
    

    self.dragPos = QPoint()
    self.timer = QTimer()
    self.sound = QSoundEffect()
    self.soundLibrary = self.parseSoundLibrary()
    self.selectedTask = None
    self.topBarParent = None
    self.editTaskWidget = None
    self.taskList = None
    self.curItem = None
    self.initUI()

  def initUI(self):
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
    self.setGeometry(100, 100, 400, 600)
    self.setStyleSheet("background-color: transparent;")
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
    #self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)
    self.setMinimumSize(200, 200)  # Set minimum size
    self.setMaximumSize(app.primaryScreen().availableSize())
    self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)


    # Main layout
    mainLayout = QVBoxLayout()

    # Frame with border and rounded corners
    frame = QFrame(self)
    frame.setContentsMargins(0, 0, 0, 0)
    frame.setStyleSheet("border: 1px solid black; background-color: #353535;  color: white; border-radius: 10px;")
    frameLayout = QVBoxLayout(frame)

    # Custom top bar
    self.topBarParent = QWidget()
    self.topBarParent.setStyleSheet("border: 0px; background-color: transparent;  color: white;")
    self.topBarParent.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
    self.topBarParent.resize(70, 65)

    topBar = QHBoxLayout()
    topBar.setContentsMargins(0, 0, 0, 0)
    
    topSizeGrip =  QSizeGrip(self)
    topBar.addWidget(topSizeGrip)

    self.dragLabel = QLabel("Drag Here")
    self.dragLabel.setStyleSheet("border-width:0px; background-color: gray; color: white; padding: 0px; border-radius: 5px;")
    self.dragLabel.mousePressEvent = self.mousePressEvent
    self.dragLabel.mouseMoveEvent = self.mouseMoveEvent
    self.dragLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    self.dragLabel.resize(70, 55)
    closeButton = QPushButton("X")
    closeButton.clicked.connect(self.close)
    closeButton.setStyleSheet("background-color: red; color: white; padding-left: 3px; padding-right: 3px; border-radius: 5px;")
    closeButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
    closeButton.resize(70, 65)
    topBar.addWidget(self.dragLabel)
    topBar.addWidget(closeButton)
    self.topBarParent.setLayout(topBar)


    selectedTask = TaskManager.data['tasks'][0]  # Get a task from the data
    self.editTaskWidget = EditTaskWidget(selectedTask, self.pixmapManager)  # Create the custom widget with the task data

    # Task list
    
    self.taskList = QListWidget( self )

    # Enable drag and drop
    self.taskList.setDragEnabled(True)
    self.taskList.setAcceptDrops(True)
    self.taskList.setDropIndicatorShown(True)
    self.taskList.setDragDropMode(QListWidget.DragDropMode.InternalMove)

    self.taskList.setContentsMargins(0, 0, 0, 0)
    self.taskList.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.MinimumExpanding)
    


    # General Action Buttons
    buttonsLayout = QHBoxLayout()

    newButton = QPushButton("New...")
    newButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    newButton.resize(85, 45)
    newButton.clicked.connect(self.newPrompt)
    buttonsLayout.addWidget(newButton)

    sortButton = QPushButton("Sort")
    sortButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    sortButton.resize(85, 45)
    sortButton.clicked.connect(self.playNotification)
    buttonsLayout.addWidget(sortButton)

    duplicateButton = QPushButton("Dupe")
    duplicateButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    duplicateButton.resize(85, 45)
    duplicateButton.clicked.connect(self.dupelicateTask)
    buttonsLayout.addWidget(duplicateButton)

    spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    buttonsLayout.addItem(spacer)

    deleteButton = QPushButton("Delete")
    deleteButton.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    deleteButton.resize(85, 45)
    deleteButton.clicked.connect(self.playNotification)
    buttonsLayout.addWidget(deleteButton)

    spacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    buttonsLayout.addItem(spacer)


    sizeGrip =  QSizeGrip(self) # ResizeHandle(self)
    #bottomBar.addWidget(sizeGrip)
    buttonsLayout.addWidget(sizeGrip)

    # Add layouts to frame layout
    frameLayout.addWidget(self.topBarParent)
    frameLayout.addWidget(self.editTaskWidget)
    frameLayout.addWidget(self.taskList)
    frameLayout.addLayout(buttonsLayout)

    mainLayout.addWidget(frame)
    self.setLayout(mainLayout)

    self.topBarParent.setVisible(False)

    # Timer for notifications
    self.timer = QTimer(self)
    self.sound = QSoundEffect()

  def keyPressEvent(self, event: QKeyEvent):
    altModifier = Qt.KeyboardModifier.AltModifier
    if event.key() == Qt.Key.Key_Q and altModifier:
      self.close()
  
  def keyReleaseEvent(self, event: QKeyEvent ):
    if event.key() == Qt.Key.Key_Alt:
      self.topBarParent.setVisible(not self.topBarParent.isVisible())
    return super().keyReleaseEvent(event)

  def registerExit(self):
    atexit.register(self.saveTasksData)

  def buildListItems(self):
    hasSelection = False
    selectedTask = None
    for task in TaskManager.data['tasks']:
      taskItemWidget, taskItem = self.addNewTask( task )
      if not hasSelection:
        self.selectedTask = taskItemWidget
        taskItemWidget.setSelected(True)
        hasSelection = True

    self.taskList.currentItemChanged.connect(self.selectedItemChanged)

  @pyqtSlot(QListWidgetItem, QListWidgetItem)
  def selectedItemChanged(self, current, previous):
    if current != None:
      curItem = self.taskList.currentItem()
      curWidget = self.taskList.itemWidget(curItem)
      self.selectedTask = curWidget
      self.editTaskWidget.displayTask(curWidget)
      
      self.playAudio("task_nudge")

  def gatherTaskData(self):
    taskData = {'tasks': []}
    for index in range(self.taskList.count()):
      itemWidget = self.taskList.itemWidget(self.taskList.item(index))
      taskData['tasks'].append(itemWidget.data)
    return taskData
  
  def saveTasksData(self):
    TaskManager.exportData( self.gatherTaskData() )

  def parseSoundLibrary(self):
    self.soundLibrary = {}
    for sound in os.listdir(sound_rootPath):
      key = sound.split(".")[0]
      self.soundLibrary[key] = os.path.join(sound_rootPath, sound)
    return self.soundLibrary

  def playAudio(self, sound):
    if sound in self.soundLibrary:
      if self.sound.isPlaying():
        self.sound.stop()
      self.sound.setSource(QUrl.fromLocalFile(self.soundLibrary[sound]))
      self.sound.play()

  def mousePressEvent(self, event: QMouseEvent):
    if event.button() == Qt.MouseButton.LeftButton:
        self.dragPos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
        event.accept()

  def mouseMoveEvent(self, event: QMouseEvent):
    if event.buttons() == Qt.MouseButton.LeftButton:
      self.move(event.globalPosition().toPoint() - self.dragPos)
      event.accept()

  def playNotification(self):
    self.sound.play()


  def newPrompt(self):
    promptType = "Task"
    promptWindow = PromptWindow(self, previousType=promptType)
    promptWindow.show()

  def handlePromptButton(self, createType, data={}):
    if createType != "Cancel":
      self.addNewTask( data )
      self.playNotification()
    else:
      pass
        
  def addNewTask(self, taskData):
    curItem = TaskListItem( self.pixmapManager, taskData )
    curItemWidget = QListWidgetItem(self.taskList)
    curItemWidget.setSizeHint(curItem.sizeHint())
    self.taskList.addItem( curItemWidget )
    self.taskList.setItemWidget( curItemWidget, curItem )
    curItemWidget.setSelected(True)
    curItemMove = self.taskList.currentRow()
    self.taskList.insertItem(0, curItemWidget)
    curItem.setIconPadding( curItem.sizeHint().height() )

    return curItemWidget, curItem

  def dupelicateTask(self):
    if self.selectedTask != None:
      self.addNewTask( self.selectedTask.data )

  def GetDateTime(self, dayOffset=0):
    current_datetime = datetime.now(timezone.utc)
    print("Current datetime:", current_datetime)

    # Offset the current datetime by 3 days
    offset = timedelta(days=3)
    new_datetime = current_datetime + offset
    print("Offset datetime:", new_datetime)

    return current_datetime.strftime("%Y-%m-%d %H:%M:%S")
  def GetReadableRunTime( self, runtime ):
    outStr = "0:00:00:00"


  def GetLongReadableRunTime( self, runtime ):
    seconds = runtime // 1000
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    runtime_str = ""
    if days > 0:
      runtime_str += f"{days} day{'s' if days > 1 else ''} "
    if hours > 0:
      runtime_str += f"{hours % 24} hour{'s' if hours % 24 > 1 else ''} "
    if minutes > 0:
      runtime_str += f"{minutes % 60} minute{'s' if minutes % 60 > 1 else ''} "
    if seconds > 0:
      runtime_str += f"{seconds % 60} second{'s' if seconds % 60 > 1 else ''}"

    return runtime_str.strip()

  def GetReadableRunTime(self, runtime):
    seconds = runtime // 1000
    minutes = seconds // 60
    hours = minutes // 60
    days = hours // 24

    seconds = str(seconds % 60).zfill(2)
    minutes = str(minutes % 60).zfill(2)
    hours = str(hours % 24).zfill(2)
    days = str(days).zfill(2)
    
    runtime_str = f"{days}:{hours}:{minutes}:{seconds}"


    return runtime_str.strip()



if __name__ == '__main__':
  app = QApplication(sys.argv)

  organizer = TaskOrganizer()
  organizer.show()
  organizer.buildListItems()
  organizer.registerExit()
  sys.exit(app.exec())