# Listen to the Music 🎵

A comprehensive music library management system built with Python, demonstrating advanced data structures and object-oriented programming principles.

## Table of Contents
- [Project Overview](#project-overview)
- [Data Structures](#data-structures)
- [Object-Oriented Programming Principles](#object-oriented-programming-principles)
- [Core Features](#core-features)
- [File Structure](#file-structure)
- [Installation & Usage](#installation--usage)
- [Technical Deep Dive](#technical-deep-dive)

---

## Project Overview

**Listen to the Music** is a terminal-based music library management system that allows users to:
- Organize and manage music tracks
- Create and manage playlists
- Browse albums
- Queue tracks for playback with shuffle and repeat functionality
- Import music data from JSON and CSV files

The project showcases practical implementations of fundamental computer science concepts including binary search trees, linked lists, hash maps, and comprehensive OOP design patterns.

---

## Data Structures

### 1. **Binary Search Tree (BST)** - `Library.py`

The music library uses a **Binary Search Tree** for efficient track storage and retrieval.

#### Implementation Details:
```python
class TreeNode:
    def __init__(self, track):
        self.trackData = track
        self.leftChild = None   # Smaller values
        self.rightChild = None  # Larger values
```

#### Key Characteristics:
- **Time Complexity:**
  - Search: O(log n) average, O(n) worst case
  - Insert: O(log n) average, O(n) worst case
  - In-order traversal: O(n)

- **Hierarchical Comparison:**
  1. Primary: Track title (alphabetically)
  2. Secondary: Artist name
  3. Tertiary: Album name
  4. Quaternary: Duration

- **Advantages:**
  - Maintains tracks in sorted order automatically
  - Efficient searching by title
  - No duplicate prevention built-in
  - In-order traversal yields alphabetically sorted tracks

#### Operations:
```python
# Insert track (recursive)
def __insertTrackRecursive(self, currentNode, newTrack, wasInserted)

# In-order traversal (returns sorted tracks)
def __traverseInOrder(self, currentNode, trackList)

# Search by title
def searchTracksByTitle(self, searchQuery)
```

---

### 2. **Doubly-Linked List** - `Queue.py`

The playback queue uses a **Doubly-Linked List** for bidirectional navigation.

#### Implementation Details:
```python
class LinkedListNode:
    def __init__(self, track):
        self.trackData = track
        self.nextNode = None  # Forward link
        self.prevNode = None  # Backward link
```

#### Key Characteristics:
- **Time Complexity:**
  - Add to end: O(1)
  - Next/Previous track: O(1)
  - Search: O(n)

- **Advantages:**
  - Efficient forward and backward navigation
  - O(1) insertion at head/tail
  - Perfect for queue operations (play, pause, next, previous)
  - Supports repeat mode by looping from tail to head

#### Operations:
```python
# Add track to queue
def addTrack(self, track)

# Navigate to next track (O(1))
def advanceToNext(self)

# Navigate to previous track (O(1))
def rewindToPrevious(self)

# Shuffle queue (maintains active track position)
def shuffleQueue(self)
```

#### Shuffle Algorithm:
The shuffle implementation preserves the currently playing track:
1. Split queue into: played tracks, current track, unplayed tracks
2. Shuffle only the unplayed tracks
3. Rebuild: played (original order) → current → shuffled unplayed

---

### 3. **Hash Map (Dictionary)** - Multiple Classes

Hash maps are used extensively for O(1) lookups.

#### In `AlbumManager`:
```python
self.__albumCollection = {}  # album_name -> Album object
```
- **Purpose:** Fast album lookup by name
- **Time Complexity:** O(1) average for get/set

#### In `PlaylistManager`:
```python
self.__playlistCollection = {}  # playlist_name -> Playlist object
```
- **Purpose:** Fast playlist lookup by name
- **Prevents:** Duplicate playlist names

#### In `Playlist`:
```python
self.__trackIdentifiers = set()  # {track_identifier1, track_identifier2, ...}
```
- **Purpose:** O(1) duplicate detection
- **Identifier Format:** `title.lower() + str(artist).lower()`

---

### 4. **Dynamic List** - `Playlist.py`

Playlists use Python lists with tuple entries for track management.

#### Implementation Details:
```python
self.__trackList = []  # List of (track, timestamp) tuples
```

#### Key Characteristics:
- **Stores:** Tuples of `(Track object, datetime)`
- **Maintains:** Insertion order chronologically
- **Supports:** Multi-level sorting with tie-breaking

#### Sorting Implementation:
```python
def sortTracks(self, sortCriteria="date_added"):
    # 5-level tie-breaking
    def getSortKey(entry):
        trackObj, addedTimestamp = entry
        
        if sortCriteria == "title":
            return (
                trackObj.getTitle().lower(),           # 1st priority
                trackObj.getPrimaryArtist().lower(),   # 2nd priority
                trackObj.getAlbum().lower(),            # 3rd priority
                trackObj.convertDurationToSeconds(),    # 4th priority
                addedTimestamp                          # 5th priority (tie-breaker)
            )
```

---

### 5. **Menu Dictionary Pattern** - `Main.py`

The interface uses dictionary-based menu systems for clean code architecture.

#### Implementation:
```python
MENUS = {
    'main': {
        'title': 'LISTEN TO THE MUSIC',
        'options': {'1': 'Browse Tracks', '2': 'Music Player', '0': 'Exit'}
    }
}

# Action dispatching
LIBRARY_ACTIONS = {
    '1': handleCreateTrack,
    '2': handleViewLibrary,
    '3': handleSearchTrack,
    '4': handleImportTracks
}
```

#### Advantages:
- Eliminates long if-elif chains
- Easy to maintain and extend
- Cleaner code structure
- O(1) action lookup

---

## Object-Oriented Programming Principles

### 1. **Encapsulation** 🔒

All classes use private attributes (name mangling with `__`) to protect data integrity.

#### Example in `Track.py`:
```python
class Track:
    def __init__(self, title, artist, album, duration):
        self.__trackTitle = title      # Private attribute
        self.__trackArtist = artist    # Private attribute
        self.__trackAlbum = album      # Private attribute
        self.__trackDuration = duration # Private attribute
    
    # Public accessor methods
    def getTitle(self):
        return self.__trackTitle
    
    def setTitle(self, title):
        self.__trackTitle = title
```

**Benefits:**
- Data cannot be modified directly from outside the class
- Validation can be added to setter methods
- Internal implementation can change without affecting external code

---

### 2. **Abstraction** 🎭

Complex operations are hidden behind simple interfaces.

#### Example in `Library.py`:
```python
# Public interface (simple)
def addTrack(self, track):
    wasInserted = [False]
    self.__rootNode = self.__insertTrackRecursive(self.__rootNode, track, wasInserted)
    if wasInserted[0]:
        self.__albumMgr.addTrackToAlbum(track)
        self.__saveLibraryToFile()
    return wasInserted[0]

# Private implementation (complex BST logic)
def __insertTrackRecursive(self, currentNode, newTrack, wasInserted):
    # Complex recursive BST insertion logic
    ...
```

**Benefits:**
- Users don't need to understand BST mechanics
- Implementation can be optimized without changing the public API
- Reduces cognitive load for developers using the class

---

### 3. **Composition** 🧩

Classes are built from other classes to create complex functionality.

#### Example in `Main.py`:
```python
# Composition relationships
musicLibrary = Library()                          # Contains AlbumManager
playlistMgr = PlaylistManager(musicLibrary)       # Contains reference to Library
playbackQueue = Queue()                            # Contains LinkedListNodes
```

#### Relationships:
- `Library` **has-a** `AlbumManager`
- `Library` **has-a** BST of `TreeNode` objects
- `Queue` **has-a** doubly-linked list of `LinkedListNode` objects
- `Playlist` **has-a** list of `Track` objects with timestamps
- `PlaylistManager` **has-a** dictionary of `Playlist` objects

---

### 4. **Static Methods** 📌

Factory methods for object deserialization.

#### Example in `Track.py`:
```python
@staticmethod
def fromDict(data):
    return Track(data["title"], data["artist"], data["album"], data["duration"])
```

**Use Cases:**
- JSON deserialization
- Creating objects from file data
- Alternative constructors

---

### 5. **Magic Methods (Dunder Methods)** ✨

Special methods for Python integration.

#### Example in `Track.py`:
```python
def __eq__(self, other):
    if not isinstance(other, Track):
        return False
    return (self.__trackTitle == other.__trackTitle and 
            str(self.__trackArtist) == str(other.__trackArtist) and
            self.__trackAlbum == other.__trackAlbum and
            self.__trackDuration == other.__trackDuration)

def __str__(self):
    return self.formatDisplay()
```

**Implemented Methods:**
- `__eq__`: Enables track comparison with `==`
- `__str__`: String representation for `print(track)`
- `__init__`: Constructor

---

### 6. **Single Responsibility Principle** 📋

Each class has one clear purpose.

| Class | Responsibility |
|-------|---------------|
| `Track` | Represent a single music track |
| `Album` | Group tracks by album |
| `Playlist` | User-created track collections |
| `Library` | Manage all tracks in BST |
| `Queue` | Playback queue management |
| `AlbumManager` | Organize and access albums |
| `PlaylistManager` | Manage all playlists |

---

### 7. **Method Organization**

Methods are logically grouped:

#### Accessor Methods (Getters):
```python
def getTitle(self)
def getArtist(self)
def getAlbum(self)
```

#### Mutator Methods (Setters):
```python
def setTitle(self, title)
def setArtist(self, artist)
```

#### Business Logic Methods:
```python
def convertDurationToSeconds(self)
def calculateTotalDuration(self)
def sortTracks(self, criteria)
```

#### Serialization Methods:
```python
def toDict(self)
@staticmethod
def fromDict(data)
```

---

## Core Features

### 📚 Library Management
- Add tracks to library
- View library with pagination (10 tracks per page)
- Search tracks by title
- Import tracks from JSON/CSV files
- Automatic album organization
- Binary Search Tree for efficient storage

### 🎵 Playlist Management
- Create custom playlists
- View all playlists with pagination
- Add tracks to playlists
- Sort playlists by:
  - Date created
  - Name (alphabetically)
  - Duration
- Sort tracks within playlist by:
  - Date added
  - Title
  - Artist
  - Duration
- Queue entire playlists
- Import playlists from JSON/CSV

### 💿 Album Browsing
- Automatic album detection
- View all albums with track counts
- Browse tracks within albums
- Queue entire albums
- Calculated album duration

### 🎧 Playback Queue
- Add individual tracks to queue
- Load playlists/albums into queue
- Play/Pause controls
- Next/Previous track navigation
- Shuffle mode (preserves current track)
- Repeat mode
- Queue persistence (restored on restart)
- Duplicate prevention

---

## File Structure

```
LTTM/
│
├── Track.py              # Track class (data model)
├── Album.py              # Album class (track grouping)
├── Playlist.py           # Playlist class (user collections)
├── Library.py            # Library class (BST management)
├── Queue.py              # Queue class (doubly-linked list)
├── Managers.py           # AlbumManager & PlaylistManager
├── Main.py               # Entry point and UI logic
│
├── storage/              # Persistent data storage
│   ├── library_data.json
│   ├── album_data.json
│   ├── playlist_data.json
│   └── queue_state.json
│
├── tracks.json           # Sample track import file
├── tracks.csv            # Sample track import file
├── playlists.json        # Sample playlist import file
├── playlists.csv         # Sample playlist import file
│
└── README.md             # This file
```

---

## Installation & Usage

### Prerequisites
- Python 3.7 or higher
- No external dependencies required (uses standard library)

### Running the Application

```bash
# Navigate to project directory
cd d:\Code\LTTM

# Run the application
python Main.py
```

### Import File Formats

#### JSON Format (`tracks.json`):
```json
[
    {
        "title": "Shake It Off",
        "artist": "Taylor Swift",
        "album": "1989",
        "duration": "3:39"
    },
    {
        "title": "Bad Blood",
        "artist": ["Taylor Swift", "Kendrick Lamar"],
        "album": "1989",
        "duration": "3:31"
    }
]
```

#### CSV Format (`tracks.csv`):
```csv
title,artist,album,duration
Shake It Off,Taylor Swift,1989,3:39
Bad Blood,"Taylor Swift, Kendrick Lamar",1989,3:31
```

---

## Technical Deep Dive

### Algorithm Complexity Analysis

| Operation | Data Structure | Time Complexity | Space Complexity |
|-----------|---------------|-----------------|------------------|
| Add track to library | BST | O(log n) avg, O(n) worst | O(1) |
| Search track by title | BST | O(n) | O(k) where k = results |
| Get all tracks sorted | BST in-order | O(n) | O(n) |
| Add to queue | Doubly-linked list | O(1) | O(1) |
| Next/Prev track | Doubly-linked list | O(1) | O(1) |
| Find album by name | Hash map | O(1) avg | O(1) |
| Add track to playlist | Hash set check + List append | O(1) | O(1) |
| Sort playlist | Python Timsort | O(n log n) | O(n) |
| Shuffle queue | List shuffle + rebuild | O(n) | O(n) |

### Memory Management

- **BST**: Sparse tree structure, minimal overhead per node
- **Doubly-linked list**: 2 pointers per node (next, prev)
- **Hash maps**: Load factor ~0.67, automatic resizing
- **Persistence**: JSON serialization for human-readable storage

### Design Patterns Used

1. **Factory Pattern**: Static `fromDict()` methods
2. **Strategy Pattern**: Sorting with different criteria
3. **Command Pattern**: Dictionary-based action dispatching
4. **Singleton-like**: Single instances of Library, Queue, Managers
5. **Facade Pattern**: Main.py simplifies interaction with subsystems

---

## Key Design Decisions

### Why BST for Library?
- Maintains sorted order automatically
- Efficient searching
- No external sorting needed
- Good for range queries (though not implemented)

### Why Doubly-Linked List for Queue?
- O(1) navigation in both directions
- Perfect for player controls (next/previous)
- Easy insertion/deletion
- Natural fit for sequential playback

### Why Hash Maps for Albums/Playlists?
- O(1) lookup by name
- Prevent duplicate names
- Fast access for user operations

### Why Tuples in Playlist Tracks?
- Immutable pairing of track and timestamp
- Memory efficient
- Clear semantic meaning
- Easy to sort with Python's built-in sort

---

## Future Enhancements

### Potential Data Structure Upgrades:
1. **AVL Tree or Red-Black Tree**: Self-balancing BST for guaranteed O(log n)
2. **Trie**: Prefix-based track search
3. **Priority Queue**: Most played tracks, favorites
4. **Graph**: Track relationships, recommendations
5. **Bloom Filter**: Quick duplicate checks before BST insertion

### Feature Ideas:
- Track ratings and favorites
- Recently played history (circular buffer)
- Smart playlists (auto-generated based on criteria)
- Genre categorization
- Play count statistics
- Duration-based playlist generation
- Export functionality

---

## Learning Outcomes

This project demonstrates:

✅ **Data Structures:**
- Binary Search Trees (recursive operations)
- Doubly-Linked Lists (bidirectional traversal)
- Hash Maps (O(1) lookups)
- Dynamic Arrays (Python lists)
- Sets (duplicate prevention)

✅ **Algorithms:**
- Tree traversal (in-order)
- Recursive insertion
- Multi-level sorting with tie-breaking
- Shuffle with constraints
- Binary search tree comparison

✅ **OOP Principles:**
- Encapsulation (private attributes)
- Abstraction (hiding complexity)
- Composition (has-a relationships)
- Single Responsibility Principle
- Method organization and naming

✅ **Software Engineering:**
- File I/O and persistence
- JSON/CSV parsing
- Error handling
- State management
- Menu-driven interfaces
- Dictionary-based dispatching

---

## Code Statistics

- **Classes**: 9 (Track, Album, Playlist, Library, Queue, TreeNode, LinkedListNode, AlbumManager, PlaylistManager)
- **Lines of Code**: ~2,000+
- **Data Structures**: 5 major types (BST, Doubly-Linked List, Hash Map, Dynamic List, Set)
- **Design Patterns**: 5+ patterns implemented
- **Time Complexity**: O(1) to O(n log n) depending on operation

---

## Author Notes

This project was designed as a comprehensive demonstration of fundamental computer science concepts in a practical, real-world application. Each design decision balances performance, maintainability, and educational value.

The code prioritizes:
- **Clarity**: Descriptive variable names, extensive comments
- **Correctness**: Proper data structure implementations
- **Efficiency**: Optimal time/space complexity where practical
- **Maintainability**: Modular design, single responsibility

---

## License

This project is for educational purposes.

---

**Enjoy the music! 🎵🎧**
