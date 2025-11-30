import json

class Track:
    def __init__(self, title, artist, album, duration):
        """
        Represents a music track with metadata including title, artist, album and duration.
        
        This class encapsulates track information and provides accessor methods.
        Supports both single and multiple artists per track.
        
        Attributes:
            __trackTitle: The track's title
            __trackArtist: Artist name(s) - can be string or list
            __trackAlbum: Album name this track belongs to
            __trackDuration: Track length in mm:ss format
        """
        # Private attributes (double underscore triggers name mangling)
        self.__trackTitle = title
        # Artist can be a string like "Taylor Swift" or a list like ["Taylor Swift", "Ed Sheeran"]
        self.__trackArtist = artist
        self.__trackAlbum = album
        self.__trackDuration = duration  # format: "mm:ss"
    
    # Accessor methods for encapsulation
    def getTitle(self):
        return self.__trackTitle
    
    def getArtist(self):
        return self.__trackArtist
    
    def getAlbum(self):
        return self.__trackAlbum
    
    def getDuration(self):
        return self.__trackDuration
    
    # Mutator methods
    def setTitle(self, title):
        self.__trackTitle = title
    
    def setArtist(self, artist):
        self.__trackArtist = artist
    
    def setAlbum(self, album):
        self.__trackAlbum = album
    
    def setDuration(self, duration):
        self.__trackDuration = duration
    
    # Calculate duration in seconds
    def convertDurationToSeconds(self):
        timeParts = self.__trackDuration.split(":")
        mins = int(timeParts[0])
        secs = int(timeParts[1])
        return (mins * 60) + secs
        
    # Extract primary artist for sorting
    def getPrimaryArtist(self):
        if type(self.__trackArtist) == list:
            return self.__trackArtist[0]
        return self.__trackArtist
    
    # Format for display
    def formatDisplay(self):
        artistDisplay = self.__trackArtist
        if type(self.__trackArtist) == list:
            artistDisplay = ", ".join(self.__trackArtist)
        return f"{self.__trackTitle} - {artistDisplay} ({self.__trackDuration})"
    
    # Convert to dictionary for serialization
    def toDict(self):
        # Converts track to a dictionary so it can be saved as JSON
        return {
            "title": self.__trackTitle,
            "artist": self.__trackArtist,
            "album": self.__trackAlbum,
            "duration": self.__trackDuration
        }
    
    # Create Track from dictionary
    @staticmethod
    def fromDict(data):
        return Track(data["title"], data["artist"], data["album"], data["duration"])
    
    # Equality comparison
    def __eq__(self, other):
        if not isinstance(other, Track):
            return False
        return (self.__trackTitle == other.__trackTitle and 
                str(self.__trackArtist) == str(other.__trackArtist) and
                self.__trackAlbum == other.__trackAlbum and
                self.__trackDuration == other.__trackDuration)
    
    # String representation
    def __str__(self):
        return self.formatDisplay()
