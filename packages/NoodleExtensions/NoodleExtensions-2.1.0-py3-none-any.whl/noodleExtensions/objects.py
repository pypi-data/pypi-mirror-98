class Note:
    def __init__(self, _time, _lineIndex, _lineLayer, _type, _cutDirection, **_customData):
        '''a note object which contains info on a note.\n
        `beat` - The beat of the note.\n
        `index` - The lineIndex of the note\n
        `layer` - The lineLayer of the note\n
        `type` - The note type\n
        `cutDirection` - The cut direction of the note\n
        `customData` - The note's custom data\n
        '''
        newNote = {
            "_time":_time,
            "_lineIndex":_lineIndex,
            "_lineLayer":_lineLayer,
            "_type":_type,
            "_cutDirection":_cutDirection
        }

        if _customData != {}:
            newNote["_customData"] = _customData
        
        self.note = newNote

        self._time = _time
        self._lineIndex = _lineIndex
        self._lineLayer = _lineLayer
        self._type = _type
        self._cutDirection = _cutDirection
        self._customData = _customData
        
    @classmethod # allows to call method without needing to call __init__
    def fromDict(cls, data:dict):
        '''Will return a Note object from a note dict data.'''
        noteObjFromDict = cls(**data)
        return noteObjFromDict

class Obstacle:
    def __init__(self, _time, _lineIndex, _type, _duration, _width, **_customData):
        '''a note object which contains info on a note.\n
        `beat` - The start beat of the wall.\n
        `index` - The starting left position of the wall.\n
        `type` - The wall type type\n
        `duration` - How many beats the wall lasts.\n
        `width` - How wide the wall should be\n
        `customData` - The note's custom data\n
        '''
        newWall = {
            "_time":_time,
            "_lineIndex":_lineIndex,
            "_type":_type,
            "_duration":_duration,
            "_width":_width
        }

        if _customData != {}:
            newWall["_customData"] = _customData
        
        self.obstacle = newWall

        self._time = _time
        self._lineIndex = _lineIndex
        self._type = _type
        self._duration = _duration
        self._width = _width
        self._customData = _customData
        
    @classmethod
    def fromDict(cls, data:dict):
        '''Will return a Obstacle object from dict data.'''
        noteObjFromDict = cls(**data)
        return noteObjFromDict