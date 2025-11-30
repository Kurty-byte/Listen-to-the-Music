import json
import os
import csv

# AlbumManager handles album organization
class AlbumManager:
    def __init__(self):
        # Dictionary (hash map) allows fast lookup: given album name, find Album object instantly
        # Example: {"Red": Album("Red"), "1989": Album("1989")}
        self.__albumCollection = {}  # Hash map: album name -> Album object
        self.__albumFilePath = "storage/album_data.json"
    
    # Retrieve or instantiate album
    def getOrCreateAlbum(self, albumName):
        if albumName not in self.__albumCollection:
            # Import Album to avoid circular dependency
            from Album import Album
            # Instantiate new album
            album = Album(albumName)
            self.__albumCollection[albumName] = album
            return album
        return self.__albumCollection[albumName]
    
    # Append track to corresponding album
    def addTrackToAlbum(self, track):
        albumName = track.getAlbum()
        album = self.getOrCreateAlbum(albumName)
        album.appendTrack(track)
        self.__persistAlbums()
    
    # Fetch album by name
    def getAlbum(self, name):
        return self.__albumCollection.get(name)
    
    # Retrieve all album names
    def getAlbumNames(self):
        return list(self.__albumCollection.keys())
    
    # Retrieve all album objects
    def getAllAlbums(self):
        return list(self.__albumCollection.values())
    
    # Show albums with pagination
    def showAlbums(self, pageNum=1):
        nameList = self.getAlbumNames()
        if not nameList:
            print("No albums found!")
            return 0
        
        albumsPerPage = 10
        totalPages = (len(nameList) + albumsPerPage - 1) // albumsPerPage
        
        startIdx = (pageNum - 1) * albumsPerPage
        endIdx = min(startIdx + albumsPerPage, len(nameList))
        
        print("\n<----- ALBUMS ----->")
        for i in range(startIdx, endIdx):
            album = self.__albumCollection[nameList[i]]
            print(f"({i + 1}) {nameList[i]} ({album.getTrackCount()} tracks)")
        
        if totalPages > 1:
            print(f"\n<Page {pageNum} of {totalPages}>")
        print()
        
        return totalPages
    
    # Fetch album by index
    def getAlbumByIndex(self, index):
        nameList = self.getAlbumNames()
        if 0 <= index < len(nameList):
            return self.__albumCollection[nameList[index]]
        return None
    
    # Persist albums to file
    def __persistAlbums(self):
        serializedData = []
        for album in self.__albumCollection.values():
            serializedData.append(album.toDict())
        
        os.makedirs(os.path.dirname(self.__albumFilePath), exist_ok=True)
        
        with open(self.__albumFilePath, 'w') as fileHandle:
            json.dump(serializedData, fileHandle, indent=4)
    
    # Load albums from file
    def loadFromFile(self, trackObjects):
        if not os.path.exists(self.__albumFilePath):
            return
        
        try:
            # Import Album to avoid circular dependency
            from Album import Album
            
            with open(self.__albumFilePath, 'r') as fileHandle:
                serializedData = json.load(fileHandle)
                for albumData in serializedData:
                    album = Album.fromDict(albumData, trackObjects)
                    self.__albumCollection[album.getName()] = album
        except:
            print("Error loading albums file")


# PlaylistManager handles playlist operations                                           
class PlaylistManager:
    """
    Manages all playlists in the system.
    
    This class creates, saves and loads playlists from files.
    Supports importing from JSON and CSV formats.
    
    Attributes:
        __playlistCollection: Dictionary mapping name to playlist
        __playlistFilePath: Path to playlists JSON file
        __libraryRef: Reference to library for auto-adding imported tracks
    """
    def __init__(self, library=None):
        self.__playlistCollection = {}  # Hash map: name -> Playlist
        self.__playlistFilePath = "storage/playlist_data.json"
        self.__libraryRef = library  # Reference to Library for auto-adding tracks
        self.__loadPlaylistsFromFile()
    
    # Instantiate new playlist
    def createPlaylist(self, name):
        if name in self.__playlistCollection:
            return None  # Playlist name conflict
        
        # Import Playlist to avoid circular dependency
        from Playlist import Playlist
        
        playlist = Playlist(name)
        self.__playlistCollection[name] = playlist
        self.__persistPlaylists()
        return playlist
    
    # Fetch playlist by name
    def getPlaylist(self, name):
        return self.__playlistCollection.get(name)
    
    # Retrieve all playlist names
    def getPlaylistNames(self):
        return list(self.__playlistCollection.keys())
    
    # Retrieve all playlist objects
    def getAllPlaylists(self):
        return list(self.__playlistCollection.values())
    
    # Arrange playlists by criteria
    def arrangePlaylists(self, sortCriteria="date_created"):
        """
        Sort playlists by specified criteria and return sorted list.
        sortCriteria: "date_created", "name", "duration"
        """
        playlistList = self.getAllPlaylists()
        
        if sortCriteria == "date_created":
            playlistList.sort(key=lambda pl: pl.getCreationTime())
        elif sortCriteria == "name":
            playlistList.sort(key=lambda pl: pl.getName().lower())
        elif sortCriteria == "duration":
            # Sort by cumulative duration
            def computeDurationSeconds(playlist):
                totalDur = 0
                for track in playlist.getTracks():
                    totalDur += track.convertDurationToSeconds()
                return totalDur
            playlistList.sort(key=computeDurationSeconds)
        
        return playlistList
    
    # Show playlists with pagination
    def showPlaylists(self, pageNum=1, sortedPlaylists=None):
        """
        Display playlists with pagination.
        If sortedPlaylists provided, use that arrangement.
        """
        if sortedPlaylists is not None:
            playlistList = sortedPlaylists
        else:
            playlistList = self.getAllPlaylists()
        
        if not playlistList:
            print("No playlists created yet!")
            return
        
        playlistsPerPage = 10
        totalPages = (len(playlistList) + playlistsPerPage - 1) // playlistsPerPage
        
        startIdx = (pageNum - 1) * playlistsPerPage
        endIdx = min(startIdx + playlistsPerPage, len(playlistList))
        
        print("\n<----- PLAYLISTS ----->")
        for i in range(startIdx, endIdx):
            print(f"({i + 1}) {playlistList[i].getName()}")
        
        if totalPages > 1:
            print(f"\n<Page {pageNum} of {totalPages}>")
        print()
        
        return totalPages
    
    # Fetch playlist by index position
    def getPlaylistByIndex(self, index, sortedPlaylists=None):
        """
        Get playlist by index.
        If sortedPlaylists provided, use that arrangement.
        """
        if sortedPlaylists is not None:
            playlistList = sortedPlaylists
        else:
            playlistList = self.getAllPlaylists()
        
        if 0 <= index < len(playlistList):
            return playlistList[index]
        return None
    
    # Append track to specified playlist
    def appendTrackToPlaylist(self, playlistName, track):
        playlist = self.getPlaylist(playlistName)
        if playlist:
            wasAdded = playlist.appendTrack(track)
            if wasAdded:
                self.__persistPlaylists()
            return wasAdded
        return False
    
    # Persist all playlists to file
    def __persistPlaylists(self):
        serializedData = []
        for playlist in self.__playlistCollection.values():
            serializedData.append(playlist.toDict())
        
        os.makedirs(os.path.dirname(self.__playlistFilePath), exist_ok=True)
        
        with open(self.__playlistFilePath, 'w') as fileHandle:
            json.dump(serializedData, fileHandle, indent=4)
    
    # Load playlists from file
    def __loadPlaylistsFromFile(self):
        if not os.path.exists(self.__playlistFilePath):
            return
        
        try:
            # Import Playlist to avoid circular dependency
            from Playlist import Playlist
            
            with open(self.__playlistFilePath, 'r') as fileHandle:
                serializedData = json.load(fileHandle)
                for playlistData in serializedData:
                    playlist = Playlist.fromDict(playlistData)
                    self.__playlistCollection[playlist.getName()] = playlist
        except:
            print("Error loading playlists file")
    
    # Import playlists from JSON file
    def importFromJson(self, filePath):
        try:
            # Import Track to avoid circular dependency
            from Track import Track
            from Playlist import Playlist
            
            with open(filePath, 'r') as fileHandle:
                jsonData = json.load(fileHandle)
                
                importedCount = 0
                duplicateCount = 0
                skippedCount = 0
                errorList = []
                
                for playlistEntry in jsonData:
                    try:
                        playlistName = playlistEntry["name"]
                        
                        # Verify playlist doesn't exist
                        if playlistName in self.__playlistCollection:
                            duplicateCount += 1
                            continue
                        
                        # Create new playlist
                        playlist = self.createPlaylist(playlistName)
                        if not playlist:
                            skippedCount += 1
                            continue
                        
                        # Add tracks to playlist
                        for trackEntry in playlistEntry["tracks"]:
                            track = Track.fromDict(trackEntry)
                            playlist.appendTrack(track)
                            # Auto-add track to library if reference exists
                            if self.__libraryRef:
                                self.__libraryRef.addTrack(track)
                        
                        importedCount += 1
                        
                    except Exception as e:
                        errorList.append(f"Error with playlist: {str(e)}")
                        skippedCount += 1
                
                self.__persistPlaylists()
                
                return {
                    "success": True,
                    "imported": importedCount,
                    "duplicates": duplicateCount,
                    "skipped": skippedCount,
                    "errors": errorList
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import playlists from CSV file
    def importFromCsv(self, filePath):
        try:
            # Import Track to avoid circular dependency
            from Track import Track
            
            with open(filePath, 'r') as fileHandle:
                csvReader = csv.DictReader(fileHandle)
                
                importedCount = 0
                duplicateCount = 0
                skippedCount = 0
                errorList = []
                # Cache stores playlists we're building (avoids creating duplicates)
                # Key = playlist name, Value = Playlist object or None if duplicate
                playlistCache = {}  # Track playlists being constructed
                
                # CSV files have multiple rows, possibly multiple rows per playlist
                for csvRow in csvReader:
                    try:
                        # Extract fields with None handling
                        playlistName = csvRow.get("name")
                        trackTitle = csvRow.get("title")
                        trackArtist = csvRow.get("artist")
                        trackAlbum = csvRow.get("album")
                        trackDuration = csvRow.get("duration")
                        
                        # Skip row if missing required fields
                        if not all([playlistName, trackTitle, trackArtist, trackAlbum, trackDuration]):
                            errorList.append(f"Missing required fields in row")
                            skippedCount += 1
                            continue
                        
                        # Clean whitespace
                        playlistName = playlistName.strip()
                        trackTitle = trackTitle.strip()
                        trackArtist = trackArtist.strip()
                        trackAlbum = trackAlbum.strip()
                        trackDuration = trackDuration.strip()
                        
                        # Handle multiple artists
                        if "," in trackArtist and not trackArtist.startswith('"'):
                            trackArtist = [art.strip() for art in trackArtist.split(",")]
                        
                        # Build track object
                        track = Track(trackTitle, trackArtist, trackAlbum, trackDuration)
                        
                        # Retrieve or create playlist
                        # First check cache to see if we've seen this playlist in this CSV already
                        if playlistName not in playlistCache:
                            # Not in cache yet, check if it exists globally
                            if playlistName in self.__playlistCollection:
                                # Playlist exists, mark as duplicate
                                playlistCache[playlistName] = None  # Duplicate marker
                                duplicateCount += 1
                                continue
                            else:
                                # Create new playlist and add to cache
                                playlist = self.createPlaylist(playlistName)
                                if playlist:
                                    playlistCache[playlistName] = playlist
                                    importedCount += 1
                                else:
                                    playlistCache[playlistName] = None
                                    skippedCount += 1
                                    continue
                        
                        # Append track to playlist (if valid)
                        if playlistCache[playlistName] is not None:
                            playlistCache[playlistName].appendTrack(track)
                            # Auto-add track to library if reference exists
                            if self.__libraryRef:
                                self.__libraryRef.addTrack(track)
                        
                    except Exception as e:
                        errorList.append(f"Error with row: {str(e)}")
                        skippedCount += 1
                
                self.__persistPlaylists()
                
                return {
                    "success": True,
                    "imported": importedCount,
                    "duplicates": duplicateCount,
                    "skipped": skippedCount,
                    "errors": errorList
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import playlists with format detection
    def importPlaylists(self, filePath):
        fileExtension = filePath.lower()
        if fileExtension.endswith('.json'):
            return self.importFromJson(filePath)
        elif fileExtension.endswith('.csv'):
            return self.importFromCsv(filePath)
        else:
            return {"success": False, "error": "Unsupported file format! Use .json or .csv"}
