import os
import json
import atexit
from source.ExtraNote import ExtraNote 

class TaskListManager:
  def __init__(self, filePath, extraKeys, backupPath, backupFrequency):
    self.filePath = filePath
    self.lockPath = filePath + ".lock"
    self.extraKeys = extraKeys
    self.data = {}

    self.backupPath = os.path.join(backupPath, "taskList.json")
    self.backupFrequency = backupFrequency

  def importData(self):
    self.touchFile( self.filePath )
    with open(self.filePath, 'r') as file:
      self.data = json.load(file)
    self.parseNoteData()

  def exportData(self, data=None):
    if data == None:
      data = self.data
    rebuild_data = { 'tasks': [] }
    
    for task in data['tasks']:
      rebuilt_task = {
        'status': task['status'],
        'type': task['type'],
        'priority': task['priority'],
        'header': task['header'],
        'description': task['description'],
        'date': task['date'],
        'time': task['time'],
        'notes': []
      }

      rebuiltNotes = []
      for _ in task['notes']:
        curDict = {}
        for note in self.extraKeys:
          taskText = task.get(note)
          curDict[note] = taskText
        rebuiltNotes.append(curDict)

      rebuilt_task['notes'] = rebuiltNotes

      rebuild_data['tasks'].append(rebuilt_task)

    self.data = rebuild_data
    with open(self.filePath, 'w') as file:
      json.dump(self.data, file, indent=4)

  def parseNotes(self, notesData):
    notes = []
    for note in notesData:
      noteObj = ExtraNote( noteData=note )
      notes.append( noteObj )
    return notes

  def parseNoteData(self):
    for task in self.data['tasks']:
      task['notes'] = self.parseNotes(task['notes'])

  # -- -- --

  def touchFile(self, filePath):
    if not os.path.exists(filePath):
      open(filePath, 'w').close()

  def checkLockFile(self):
    if os.path.exists(self.lockPath):
      return True
    else:
      return False
    
  def lockTaskFile(self):
    if self.checkLockFile():
      return False
    else:
      open(self.lockPath, 'w').close()
      atexit.register(self.removeLockFile)
      return True

  def removeLockFile(self):
    if os.path.exists(self.lockPath):
      os.remove(self.lockPath)
    else:
      print("Lock file does not exist.")
