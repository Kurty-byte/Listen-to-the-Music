import json
import os
import random
from Track import Track

# LinkedListNode for doubly-linked queue structure
class LinkedListNode:
    """
    Represents a node in a doubly-linked list for the queue.
    
    Each node contains a track and maintains bidirectional links.
    
    Attributes:
        trackData: The track stored in this node
        nextNode: Reference to the subsequent node
        prevNode: Reference to the preceding node
    """
    def __init__(self, track: Track):
        self.trackData = track
        # nextNode points forward to the next track in queue
        self.nextNode: Track = None
        # prevNode points backward to the previous track in queue
        # This allows us to move both forward and backward easily
        self.prevNode: Track = None

class Queue:
    """
    Manages playback queue using a doubly-linked list structure.
    
    Queue supports playback control, shuffle, and repeat functionality.
    State persistence allows restoration after program termination.
    
    Attributes:
        __headNode: First node in the queue
        __tailNode: Last node in the queue
        __activeNode: Currently active/playing track node
        __queueSize: Count of tracks in queue
        __shuffleEnabled: Indicates if shuffle is active
        __repeatEnabled: Indicates if repeat is active
        __playbackActive: Indicates if playback is ongoing
        __originalSequence: Stores original track order pre-shuffle
        __stateFilePath: Path for persisting queue state
    """
    def __init__(self):
        self.__headNode = None
        self.__tailNode = None
        self.__activeNode = None  # Currently selected track
        self.__queueSize = 0
        self.__shuffleEnabled = False
        self.__repeatEnabled = False
        self.__playbackActive = False
        self.__originalSequence = []  # For restoring original order
        self.__stateFilePath = "storage/queue_state.json"
    
    # Append track to queue
    def addTrack(self, track: Track):
        # Walk through entire queue to check for duplicates
        currentNode = self.__headNode
        while currentNode is not None:
            if currentNode.trackData == track:
                print(f"Track '{track.getTitle()}' by '{track.getArtist()}' is already in the queue. Skipping addition.")
                return False  # Duplicate detected
            currentNode = currentNode.nextNode

        newNode = LinkedListNode(track)
        
        # If queue is empty, this track becomes the first node
        if self.__headNode is None:
            self.__headNode = newNode
            self.__tailNode = newNode
            self.__activeNode = newNode
        else:
            # Find the last node by walking to the end
            tailFinder = self.__headNode
            while tailFinder.nextNode is not None:
                tailFinder = tailFinder.nextNode
            # Link new node to the end: tailFinder <-> newNode
            tailFinder.nextNode = newNode
            newNode.prevNode = tailFinder
            self.__tailNode = newNode
        
        self.__queueSize = 0
        counter = self.__headNode
        while counter is not None:
            self.__queueSize += 1
            counter = counter.nextNode
        
        # Add to original sequence only if not shuffled
        if not self.__shuffleEnabled:
            self.__originalSequence.append(track)
        return True
    
    # Bulk load tracks from collection
    def loadTracks(self, trackCollection):
        for track in trackCollection:
            self.addTrack(track)
        self.saveQueueState()  # Persist after loading
    
    # Resume playback
    def startPlayback(self):
        if not self.__repeatEnabled and self.__activeNode == self.__tailNode:
            self.__activeNode = self.__headNode
        self.__playbackActive = True
        self.saveQueueState()
    
    # Halt playback
    def pausePlayback(self):
        self.__playbackActive = False
        self.saveQueueState()
    
    # Advance to next track - O(1) operation
    def advanceToNext(self):
        if not self.__activeNode:
            return None
        
        if self.__activeNode.nextNode:
            self.__activeNode = self.__activeNode.nextNode
        elif self.__repeatEnabled:
            # Repeat enabled: loop to first track
            self.__activeNode = self.__headNode
        else:
            # No repeat: stop at end
            self.__playbackActive = False
            self.saveQueueState()
            return None
        
        self.saveQueueState()
        return self.__activeNode.trackData
    
    # Rewind to previous track - O(1) operation
    def rewindToPrevious(self):
        if not self.__activeNode:
            return None
        
        if self.__activeNode.prevNode:
            self.__activeNode = self.__activeNode.prevNode
        elif self.__repeatEnabled:
            # Repeat enabled and at start: jump to end
            self.__activeNode = self.__tailNode
        
        self.saveQueueState()
        return self.__activeNode.trackData
    
    # Randomize queue order
    def shuffleQueue(self):
        if self.__shuffleEnabled:
            return
        if self.__queueSize <= 1:
            return
        
        # Store original order on first shuffle
        if len(self.__originalSequence) == 0:
            node = self.__headNode
            while node:
                self.__originalSequence.append(node.trackData)
                node = node.nextNode
        
        # Find where the active track is positioned
        activePosition = -1
        node = self.__headNode
        pos = 0
        while node:
            if node == self.__activeNode:
                activePosition = pos
                break
            pos += 1
            node = node.nextNode
        
        # Split queue into: tracks before active, and tracks after active
        precedingTracks = []
        followingTracks = []
        
        node = self.__headNode
        currentPos = 0
        while node:
            if currentPos < activePosition:
                # Already played tracks go here
                precedingTracks.append(node.trackData)
            elif currentPos > activePosition:
                # Not yet played tracks go here (these will be shuffled)
                followingTracks.append(node.trackData)
            currentPos += 1
            node = node.nextNode
        
        # Store active track reference
        activeTrack = self.__activeNode.trackData if self.__activeNode else None
        
        # Randomize only tracks following active (already played tracks stay in order)
        random.shuffle(followingTracks)
        
        # Clear the queue to rebuild it
        self.__headNode = None
        self.__tailNode = None
        self.__queueSize = 0
        
        # Rebuild preceding tracks (already played - keep original order)
        for track in precedingTracks:
            node = LinkedListNode(track)
            if self.__headNode is None:
                self.__headNode = node
                self.__tailNode = node
            else:
                current = self.__headNode
                while current.nextNode is not None:
                    current = current.nextNode
                current.nextNode = node
                node.prevNode = current
                self.__tailNode = node
            self.__queueSize += 1
        
        # Rebuild active track
        if activeTrack:
            node = LinkedListNode(activeTrack)
            if self.__headNode is None:
                self.__headNode = node
                self.__tailNode = node
                self.__activeNode = node
            else:
                current = self.__headNode
                while current.nextNode is not None:
                    current = current.nextNode
                current.nextNode = node
                node.prevNode = current
                self.__tailNode = node
                self.__activeNode = node
            self.__queueSize += 1
        
        # Rebuild shuffled following tracks
        for track in followingTracks:
            node = LinkedListNode(track)
            if self.__headNode is None:
                self.__headNode = node
                self.__tailNode = node
            else:
                current = self.__headNode
                while current.nextNode is not None:
                    current = current.nextNode
                current.nextNode = node
                node.prevNode = current
                self.__tailNode = node
            self.__queueSize += 1
        
        # Default to head if no active track
        if not self.__activeNode:
            self.__activeNode = self.__headNode
        
        self.__shuffleEnabled = True
        self.saveQueueState()
        if not self.__shuffleEnabled:
            self.__shuffleEnabled = True
    
    # Restore original order
    def restoreOriginalOrder(self):
        if not self.__shuffleEnabled:
            return
        
        # Preserve active track
        activeTrack = self.__activeNode.trackData if self.__activeNode else None
        
        newlyAddedTracks = []
        node = self.__headNode
        while node:
            found = False
            for origTrack in self.__originalSequence:
                if node.trackData == origTrack:
                    found = True
                    break
            if not found:
                newlyAddedTracks.append(node.trackData)
            node = node.nextNode
        
        allTracks = self.__originalSequence + newlyAddedTracks
        self.__headNode = None
        self.__tailNode = None
        self.__queueSize = 0
        
        for track in allTracks:
            node = LinkedListNode(track)
            if self.__headNode is None:
                self.__headNode = node
                self.__tailNode = node
            else:
                current = self.__headNode
                while current.nextNode is not None:
                    current = current.nextNode
                current.nextNode = node
                node.prevNode = current
                self.__tailNode = node
            self.__queueSize += 1
        
        # Update original sequence with newly added tracks
        for track in newlyAddedTracks:
            self.__originalSequence.append(track)
        
        self.__activeNode = None
        if activeTrack:
            node = self.__headNode
            position = 0
            while node:
                if node.trackData == activeTrack:
                    self.__activeNode = node
                    break
                position += 1
                node = node.nextNode
        
        # Fallback to head if active not found
        if not self.__activeNode:
            self.__activeNode = self.__headNode
        
        self.__shuffleEnabled = False
        self.saveQueueState()
    

    
    # Toggle repeat mode
    def toggleRepeat(self):
        self.__repeatEnabled = not self.__repeatEnabled
        self.saveQueueState()
        return self.__repeatEnabled
    
    # Empty the queue
    def clearQueue(self):
        self.__headNode = None
        self.__tailNode = None
        self.__activeNode = None
        self.__queueSize = 0
        self.__shuffleEnabled = False
        self.__repeatEnabled = False
        self.__playbackActive = False
        self.__originalSequence = []
        self.saveQueueState()
    
    # Retrieve current track
    def getCurrentTrack(self):
        return self.__activeNode.trackData if self.__activeNode else None
    
    # Calculate total duration
    def getTotalDuration(self):
        size = 0
        counter = self.__headNode
        while counter:
            size += 1
            counter = counter.nextNode
        
        totalSecs = 0
        node = self.__headNode
        while node:
            duration = node.trackData.getDuration()
            timeParts = duration.split(":")
            mins = int(timeParts[0])
            secs = int(timeParts[1])
            totalSecs += (mins * 60) + secs
            node = node.nextNode
        
        hrs = totalSecs // 3600
        mins = (totalSecs % 3600) // 60
        secs = totalSecs % 60
        
        return f"{hrs} hr {mins} min"
    
    # Determine current page number
    def getCurrentPageNumber(self):
        if not self.__activeNode:
            return 1
        
        totalSize = 0
        counter = self.__headNode
        while counter:
            totalSize += 1
            counter = counter.nextNode
        
        position = 0
        node = self.__headNode
        while node:
            if node == self.__activeNode:
                break
            position += 1
            node = node.nextNode
        
        page = (position // 10) + 1
        totalPages = (totalSize // 10) + 1
        if page > totalPages:
            page = totalPages
        
        return page
    
    # Show queue with pagination
    def showQueue(self, pageNum=1):
        if self.__queueSize == 0:
            print("Queue is empty!")
            return
        
        print("\n<----- TRACK QUEUE ----->")
        print(f"Total Duration: {self.getTotalDuration()}")
        print(f"Shuffled: {'Yes' if self.__shuffleEnabled else 'No'}")
        print(f"Repeat: {'Yes' if self.__repeatEnabled else 'No'}")
        print("Tracks:")
        
        # Display active track
        if self.__activeNode:
            playbackStatus = "Playing" if self.__playbackActive else "Paused"
            print(f"\nCurrently {playbackStatus}:")
            print(f"    {self.__activeNode.trackData.formatDisplay()}")
            print("\nUp Next:")
        else:
            print("\nQueue:")
        
        # Pagination setup
        tracksPerPage = 10
        totalPages = (self.__queueSize + tracksPerPage - 1) // tracksPerPage
        
        # Collect tracks for display
        nodeList = []
        if self.__activeNode:
            # Show tracks after active
            node = self.__activeNode.nextNode
            while node:
                nodeList.append(node)
                node = node.nextNode
            
            # If repeat is on and need more tracks, loop from start
            if self.__repeatEnabled and len(nodeList) < tracksPerPage:
                node = self.__headNode
                while node and node != self.__activeNode:
                    nodeList.append(node)
                    node = node.nextNode
        else:
            # No active track, show all
            node = self.__headNode
            while node:
                nodeList.append(node)
                node = node.nextNode
        
        # Render tracks
        if len(nodeList) == 0:
            print("    (No more tracks in queue)")
        else:
            startIdx = (pageNum - 1) * tracksPerPage
            endIdx = min(startIdx + tracksPerPage, len(nodeList))
            
            for i in range(startIdx, endIdx):
                currentNode = nodeList[i]
                print(f"    ({i + 1}) {currentNode.trackData.formatDisplay()}")
        
        # Recalculate total pages
        if len(nodeList) > 0:
            totalPages = (len(nodeList) + tracksPerPage - 1) // tracksPerPage
        
        print(f"\n<Page {pageNum} of {totalPages}>")
        print()
    
    # Persist queue state
    def saveQueueState(self):
        trackData = []
        node = self.__headNode
        activeIndex = -1
        position = 0
        
        while node:
            trackData.append(node.trackData.toDict())
            if node == self.__activeNode:
                activeIndex = position
            node = node.nextNode
            position += 1
        
        originalData = [track.toDict() for track in self.__originalSequence]
        
        stateData = {
            "tracks": trackData,
            "current_index": activeIndex,
            "is_shuffled": self.__shuffleEnabled,
            "is_repeat": self.__repeatEnabled,
            "is_playing": self.__playbackActive,
            "original_order": originalData
        }
        
        os.makedirs(os.path.dirname(self.__stateFilePath), exist_ok=True)
        
        with open(self.__stateFilePath, 'w') as fileHandle:
            json.dump(stateData, fileHandle, indent=4)
    
    # Restore queue state
    def loadQueueState(self):
        if not os.path.exists(self.__stateFilePath):
            return False
        
        try:
            with open(self.__stateFilePath, 'r') as fileHandle:
                stateData = json.load(fileHandle)
                
                # Clear existing queue
                self.__headNode = None
                self.__tailNode = None
                self.__queueSize = 0
                
                # Restore tracks
                for trackData in stateData["tracks"]:
                    track = Track.fromDict(trackData)
                    node = LinkedListNode(track)
                    if self.__headNode is None:
                        self.__headNode = node
                        self.__tailNode = node
                    else:
                        self.__tailNode.nextNode = node
                        node.prevNode = self.__tailNode
                        self.__tailNode = node
                    self.__queueSize += 1
                
                # Restore active track
                activeIndex = stateData["current_index"]
                if activeIndex >= 0:
                    node = self.__headNode
                    for i in range(activeIndex):
                        if node:
                            node = node.nextNode
                    self.__activeNode = node
                
                # Restore flags
                self.__shuffleEnabled = stateData["is_shuffled"]
                self.__repeatEnabled = stateData["is_repeat"]
                self.__playbackActive = stateData["is_playing"]
                
                # Restore original sequence
                self.__originalSequence = []
                for trackData in stateData["original_order"]:
                    track = Track.fromDict(trackData)
                    self.__originalSequence.append(track)
                
                return True
        except:
            return False
    
    # State accessor methods
    def isPlaying(self):
        return self.__playbackActive
    
    def isShuffled(self):
        return self.__shuffleEnabled
    
    def isRepeatOn(self):
        return self.__repeatEnabled
    
    def getSize(self):
        return self.__queueSize
