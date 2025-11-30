import json
import os
import csv
from Track import Track
from Managers import AlbumManager

# TreeNode for binary search tree structure
class TreeNode:
    """
    Represents a node within a Binary Search Tree for the library.
    
    Each node contains a track and references to left and right children.
    
    Attributes:
        trackData: The track contained in this node
        leftChild: Reference to left subtree (smaller values)
        rightChild: Reference to right subtree (larger values)
    """
    def __init__(self, track):
        self.trackData = track
        # Left child holds tracks that come before this one alphabetically
        self.leftChild = None
        # Right child holds tracks that come after this one alphabetically
        self.rightChild = None

class Library:
    """
    Manages the music library using a Binary Search Tree structure.
    
    This class maintains all tracks in sorted order and provides search capabilities.
    Supports importing tracks from JSON and CSV file formats.
    
    Attributes:
        __rootNode: Root node of BST for storing tracks
        __libraryFilePath: Path to library JSON file
        __albumMgr: Manager for organizing tracks by albums
    """
    def __init__(self):
        self.__rootNode = None  # BST root
        self.__libraryFilePath = "storage/library_data.json"
        self.__albumMgr = AlbumManager()  # Album manager
        self.__loadLibraryFromFile()
    
    # Compare tracks using hierarchical comparison
    # Returns: negative if t1 < t2, 0 if equal, positive if t1 > t2
    def __compareTrackObjects(self, t1, t2):
        # Primary comparison: title
        title1Lower = t1.getTitle().lower()
        title2Lower = t2.getTitle().lower()
        if title1Lower != title2Lower:
            return -1 if title1Lower < title2Lower else 1
        
        # Secondary comparison: artist
        artist1 = t1.getPrimaryArtist()
        artist2 = t2.getPrimaryArtist()
        artist1Lower = artist1.lower()
        artist2Lower = artist2.lower()
        if artist1Lower != artist2Lower:
            return -1 if artist1Lower < artist2Lower else 1
        
        # Tertiary comparison: album
        album1Lower = t1.getAlbum().lower()
        album2Lower = t2.getAlbum().lower()
        if album1Lower != album2Lower:
            return -1 if album1Lower < album2Lower else 1
        
        # Final comparison: duration
        dur1 = t1.convertDurationToSeconds()
        dur2 = t2.convertDurationToSeconds()
        if dur1 != dur2:
            return -1 if dur1 < dur2 else 1
        
        return 0  # Tracks are equal
    
    # Recursively insert track into BST
    def __insertTrackRecursive(self, currentNode, newTrack, wasInserted):
        # Base case: found empty spot, create new node here
        if currentNode is None:
            wasInserted[0] = True  # Flag successful insertion
            return TreeNode(newTrack)
        
        # Compare new track with current node's track
        comparisonResult = self.__compareTrackObjects(newTrack, currentNode.trackData)
        
        # Recursive case: go left if new track is smaller
        if comparisonResult < 0:
            currentNode.leftChild = self.__insertTrackRecursive(currentNode.leftChild, newTrack, wasInserted)
        # Recursive case: go right if new track is larger
        elif comparisonResult > 0:
            currentNode.rightChild = self.__insertTrackRecursive(currentNode.rightChild, newTrack, wasInserted)
        # If comparisonResult == 0, duplicate exists (skip insertion)
        # wasInserted stays False
        
        return currentNode
    
    # Append track to library
    def addTrack(self, track):
        wasInserted = [False]  # Use list for mutable reference
        self.__rootNode = self.__insertTrackRecursive(self.__rootNode, track, wasInserted)
        
        # Process only if track was successfully inserted
        if wasInserted[0]:
            # Auto-add track to its album
            self.__albumMgr.addTrackToAlbum(track)
            self.__saveLibraryToFile()
        
        return wasInserted[0]  # True if inserted, False if duplicate
    
    # Retrieve album manager
    def getAlbumManager(self):
        return self.__albumMgr
    
    # Traverse BST in order (left-root-right)
    def __traverseInOrder(self, currentNode, trackList):
        if currentNode:
            # First, visit all tracks in left subtree (smaller values)
            self.__traverseInOrder(currentNode.leftChild, trackList)
            # Then, add current track to list
            trackList.append(currentNode.trackData)
            # Finally, visit all tracks in right subtree (larger values)
            self.__traverseInOrder(currentNode.rightChild, trackList)
        # This gives us tracks in alphabetical order
    
    def getAllTracks(self):
        trackCollection = []
        self.__traverseInOrder(self.__rootNode, trackCollection)
        return trackCollection
    
    # Find tracks matching title query
    def searchTracksByTitle(self, searchQuery):
        allTracks = self.getAllTracks()
        matchingTracks = []
        searchLower = searchQuery.lower()
        for track in allTracks:
            if searchLower in track.getTitle().lower():
                matchingTracks.append(track)
        return matchingTracks
    
    # Show library with pagination
    def displayLibrary(self, pageNum=1):
        trackList = self.getAllTracks()
        if not trackList:
            print("Library is empty!")
            return 0
        
        tracksPerPage = 10
        totalPages = (len(trackList) + tracksPerPage - 1) // tracksPerPage
        
        startIndex = (pageNum - 1) * tracksPerPage
        endIndex = min(startIndex + tracksPerPage, len(trackList))
        
        print("\n<----- TRACK LIBRARY ----->")
        for i in range(startIndex, endIndex):
            print(f"({i + 1}) {trackList[i].formatDisplay()}")
        
        if totalPages > 1:
            print(f"\n<Page {pageNum} of {totalPages}>")
        print()
        
        return totalPages
    
    # Persist library to JSON file
    def __saveLibraryToFile(self):
        trackList = self.getAllTracks()
        serializedData = [track.toDict() for track in trackList]
        
        # Ensure storage directory exists
        os.makedirs(os.path.dirname(self.__libraryFilePath), exist_ok=True)
        
        with open(self.__libraryFilePath, 'w') as fileHandle:
            json.dump(serializedData, fileHandle, indent=4)
    
    # Load library from JSON file
    def __loadLibraryFromFile(self):
        if not os.path.exists(self.__libraryFilePath):
            return
        
        try:
            with open(self.__libraryFilePath, 'r') as fileHandle:
                serializedData = json.load(fileHandle)
                for trackData in serializedData:
                    track = Track.fromDict(trackData)
                    wasInserted = [False]
                    self.__rootNode = self.__insertTrackRecursive(self.__rootNode, track, wasInserted)
            
            # Load album data after tracks
            allTracks = self.getAllTracks()
            self.__albumMgr.loadFromFile(allTracks)
        except:
            print("Error loading library file")
    
    # Retrieve track by index position
    def getTrackByIndex(self, index):
        trackList = self.getAllTracks()
        if 0 <= index < len(trackList):
            return trackList[index]
        return None
    
    # Import tracks from JSON file
    def importFromJson(self, filePath):
        if not os.path.exists(filePath):
            return {"success": False, "error": "File not found!"}
        
        try:
            with open(filePath, 'r') as fileHandle:
                jsonData = json.load(fileHandle)
            
            importedCount = 0
            skippedCount = 0
            duplicateCount = 0
            errorList = []
            
            for trackEntry in jsonData:
                try:
                    # Validate required fields exist
                    requiredFields = ['title', 'artist', 'album', 'duration']
                    if not all(field in trackEntry for field in requiredFields):
                        errorList.append(f"Missing required fields in track")
                        skippedCount += 1
                        continue
                    
                    # Extract artist data
                    artistData = trackEntry['artist']
                    
                    # Build track object
                    track = Track(
                        trackEntry['title'],
                        artistData,
                        trackEntry['album'],
                        trackEntry['duration']
                    )
                    
                    # Attempt to add to library
                    wasAdded = self.addTrack(track)
                    if wasAdded:
                        importedCount += 1
                    else:
                        duplicateCount += 1
                    
                except Exception as e:
                    errorList.append(f"Error with track: {str(e)}")
                    skippedCount += 1
            
            return {
                "success": True,
                "imported": importedCount,
                "duplicates": duplicateCount,
                "skipped": skippedCount,
                "errors": errorList
            }
            
        except json.JSONDecodeError:
            return {"success": False, "error": "Invalid JSON format!"}
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import tracks from CSV file
    def importFromCsv(self, filePath):
        if not os.path.exists(filePath):
            return {"success": False, "error": "File not found!"}
        
        try:
            with open(filePath, 'r', encoding='utf-8') as fileHandle:
                csvReader = csv.DictReader(fileHandle)
                
                importedCount = 0
                skippedCount = 0
                duplicateCount = 0
                errorList = []
                
                for csvRow in csvReader:
                    try:
                        # Validate required fields exist
                        requiredFields = ['title', 'artist', 'album', 'duration']
                        if not all(field in csvRow for field in requiredFields):
                            errorList.append(f"Missing required fields in row")
                            skippedCount += 1
                            continue
                        
                        # Process artist field (handle multiple artists)
                        artistData = csvRow['artist']
                        if ',' in artistData:
                            # Parse comma-separated artists
                            artistData = [art.strip() for art in artistData.split(',')]
                        
                        # Build track object
                        track = Track(
                            csvRow['title'].strip(),
                            artistData,
                            csvRow['album'].strip(),
                            csvRow['duration'].strip()
                        )
                        
                        # Attempt to add to library
                        wasAdded = self.addTrack(track)
                        if wasAdded:
                            importedCount += 1
                        else:
                            duplicateCount += 1
                        
                    except Exception as e:
                        errorList.append(f"Error with row: {str(e)}")
                        skippedCount += 1
                
                return {
                    "success": True,
                    "imported": importedCount,
                    "duplicates": duplicateCount,
                    "skipped": skippedCount,
                    "errors": errorList
                }
                
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    # Import tracks with format auto-detection
    def importTracks(self, filePath):
        fileExtension = filePath.lower()
        if fileExtension.endswith('.json'):
            return self.importFromJson(filePath)
        elif fileExtension.endswith('.csv'):
            return self.importFromCsv(filePath)
        else:
            return {"success": False, "error": "Unsupported file format! Use .json or .csv"}
