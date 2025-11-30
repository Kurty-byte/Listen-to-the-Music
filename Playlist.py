from datetime import datetime
from Track import Track

class Playlist:
    """
    Represents a playlist containing tracks in a dynamic list structure.
    
    Playlists maintain tracks in insertion order.
    Prevents duplicate entries and supports sorting by various criteria.
    
    Attributes:
        __playlistName: Name of the playlist
        __trackList: List of tuples containing (track, timestamp)
        __trackIdentifiers: Set for fast duplicate detection
        __creationTimestamp: Timestamp when playlist was created
    """
    def __init__(self, name, creationTime=None):
        self.__playlistName = name
        self.__trackList = []  # Dynamic list storing (track, timestamp) pairs
        self.__trackIdentifiers = set()  # Hash set for duplicate prevention
        self.__creationTimestamp = creationTime if creationTime else datetime.now()
    
    # Accessor methods
    def getName(self):
        return self.__playlistName
    
    def getSize(self):
        return len(self.__trackList)
    
    def getCreationTime(self):
        return self.__creationTimestamp
    
    # Verify if track exists in playlist
    def __trackExists(self, track):
        # Generate unique identifier from title and artist
        identifier = track.getTitle().lower() + str(track.getArtist()).lower()
        return identifier in self.__trackIdentifiers
    
    # Append track to playlist
    def appendTrack(self, track):
        if self.__trackExists(track):
            return False  # Track already present
        
        identifier = track.getTitle().lower() + str(track.getArtist()).lower()
        self.__trackIdentifiers.add(identifier)
        
        # Append to list with current timestamp
        timestamp = datetime.now()
        self.__trackList.append((track, timestamp))
        
        return True
    
    # Retrieve all tracks
    def getTracks(self):
        return [track for track, _ in self.__trackList]
    
    # Compute total duration
    def calculateTotalDuration(self):
        totalSecs = sum(track.convertDurationToSeconds() for track, _ in self.__trackList)
        
        # Format duration
        hrs = totalSecs // 3600
        mins = (totalSecs % 3600) // 60
        secs = totalSecs % 60
        
        if hrs > 0:
            return f"{hrs} hr {mins} min {secs} sec"
        else:
            return f"{mins} min {secs} sec"
    
    # Show playlist details
    def showPlaylist(self):
        print(f"\n<----- Playlist: {self.__playlistName} ----->")
        print(f"Total Duration: {self.calculateTotalDuration()}")
        print("Tracks:")
        
        for idx, (track, _) in enumerate(self.__trackList, 1):
            print(f"    ({idx}) {track.formatDisplay()}")
        print()
    
    # Sort tracks by specified criteria
    def sortTracks(self, sortCriteria="date_added"):
        """
        Arrange tracks based on specified criteria.
        sortCriteria: "date_added", "title", "artist", "duration"
        Implements 5-level tie-breaking: title -> artist -> album -> duration -> date
        """
        if not self.__trackList:
            return
        
        # Define comparison key function
        # Python's sort uses this to determine order - it returns a tuple
        # Python compares tuples element by element: (1st item, 2nd item, 3rd item...)
        def getSortKey(entry):
            trackObj, addedTimestamp = entry
            
            if sortCriteria == "date_added":
                return (
                    addedTimestamp,
                    trackObj.getTitle().lower(),
                    trackObj.getPrimaryArtist().lower(),
                    trackObj.getAlbum().lower(),
                    trackObj.convertDurationToSeconds()
                )
            elif sortCriteria == "title":
                return (
                    trackObj.getTitle().lower(),
                    trackObj.getPrimaryArtist().lower(),
                    trackObj.getAlbum().lower(),
                    trackObj.convertDurationToSeconds(),
                    addedTimestamp
                )
            elif sortCriteria == "artist":
                return (
                    trackObj.getPrimaryArtist().lower(),
                    trackObj.getTitle().lower(),
                    trackObj.getAlbum().lower(),
                    trackObj.convertDurationToSeconds(),
                    addedTimestamp
                )
            elif sortCriteria == "duration":
                return (
                    trackObj.convertDurationToSeconds(),
                    trackObj.getTitle().lower(),
                    trackObj.getPrimaryArtist().lower(),
                    trackObj.getAlbum().lower(),
                    addedTimestamp
                )
        
        # Perform in-place sorting
        self.__trackList.sort(key=getSortKey)
    
    # Serialize to dictionary
    def toDict(self):
        serializedTracks = [
            {
                "track": track.toDict(),
                "added_at": timestamp.isoformat()
            }
            for track, timestamp in self.__trackList
        ]
        
        return {
            "name": self.__playlistName,
            "created_at": self.__creationTimestamp.isoformat(),
            "tracks": serializedTracks
        }
    
    # Deserialize from dictionary
    @staticmethod
    def fromDict(data):
        creationTime = datetime.fromisoformat(data["created_at"])
        playlist = Playlist(data["name"], creationTime)
        
        for trackEntry in data["tracks"]:
            track = Track.fromDict(trackEntry["track"])
            timestamp = datetime.fromisoformat(trackEntry["added_at"])
            
            # Manually populate list to preserve timestamp
            identifier = track.getTitle().lower() + str(track.getArtist()).lower()
            playlist._Playlist__trackIdentifiers.add(identifier)
            playlist._Playlist__trackList.append((track, timestamp))
        
        return playlist
