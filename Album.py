class Album:
    """
    Represents a music album containing multiple tracks.
    
    Albums organize tracks by album name and compute aggregate duration.
    Prevents duplicate tracks within the same album.
    
    Attributes:
        __albumName: Name of the album
        __albumTracks: Collection of tracks in this album
    """
    def __init__(self, name):
        self.__albumName = name
        self.__albumTracks = []  # Track collection for this album
    
    # Accessor methods
    def getName(self):
        return self.__albumName
    
    def getTracks(self):
        return self.__albumTracks
    
    def getTrackCount(self):
        return len(self.__albumTracks)
    
    # Append track to album
    def appendTrack(self, track):
        # Verify track doesn't already exist
        for existingTrack in self.__albumTracks:
            if existingTrack == track:
                return False
        
        self.__albumTracks.append(track)
        return True
    
    # Compute cumulative duration
    def calculateTotalDuration(self):
        totalSecs = 0
        for track in self.__albumTracks:
            totalSecs += track.convertDurationToSeconds()
        
        hrs = totalSecs // 3600
        mins = (totalSecs % 3600) // 60
        secs = totalSecs % 60
        
        if hrs > 0:
            return f"{hrs} hr {mins} min {secs} sec"
        else:
            return f"{mins} min {secs} sec"
    
    # Show album information
    def showAlbum(self):
        print(f"\n<----- Album: {self.__albumName} ----->")
        print(f"Total Tracks: {self.getTrackCount()}")
        print(f"Total Duration: {self.calculateTotalDuration()}")
        print("Tracks:")
        
        for idx, track in enumerate(self.__albumTracks, 1):
            print(f"    ({idx}) {track.formatDisplay()}")
        print()
    
    # Serialize to dictionary
    def toDict(self):
        return {
            "name": self.__albumName,
            "tracks": [track.toDict() for track in self.__albumTracks]
        }
    
    # Deserialize from dictionary
    @staticmethod
    def fromDict(data, trackObjects):
        album = Album(data["name"])
        # Match tracks from data with track objects
        for trackData in data["tracks"]:
            for track in trackObjects:
                if (track.getTitle() == trackData["title"] and
                    str(track.getArtist()) == str(trackData["artist"]) and
                    track.getAlbum() == trackData["album"]):
                    album.appendTrack(track)
                    break
        return album
