class ExtraNote:
  def __init__(self, text="", time="", url="", noteData=None):
    self.text = text if text != None else ""
    self.time = time if time != None else ""
    self.url = url if url != None else ""
    if noteData != None:
      self.setKeys(noteData)
  
  def setKeys(self, noteDta):
    self.text = noteDta['text']
    self.time = noteDta['time']
    self.url = noteDta['url']
  
  def dupe(self):
    return ExtraNote(self.text, self.time, self.url)
  
  def get(self, key):
    if key == 'text':
      return self.text
    elif key == 'time':
      return self.time
    elif key == 'url':
      return self.url
    return None