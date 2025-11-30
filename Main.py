from Library import Library
from Managers import PlaylistManager
from Queue import Queue
from Track import Track

# Initialize components
musicLibrary = Library()
playlistMgr = PlaylistManager(musicLibrary)
playbackQueue = Queue()

# [MENU DEFINITIONS - DICTIONARY BASED]
MENUS = {
    'main': {
        'title': 'LISTEN TO THE MUSIC',
        'header_style': '=',
        'options': {
            '1': 'Browse Tracks',
            '2': 'Music Player',
            '0': 'Exit'
        }
    },
    'browse_tracks': {
        'title': 'BROWSE TRACKS',
        'header_style': '_',
        'options': {
            '1': 'Track Library',
            '2': 'Track Albums',
            '3': 'Track Playlists',
            'b': 'Back'
        }
    },
    'library': {
        'title': 'TRACK LIBRARY',
        'header_style': '_',
        'options': {
            '1': 'Create Track',
            '2': 'View Library',
            '3': 'Search Track',
            '4': 'Import',
            'b': 'Back'
        }
    },
    'playlist': {
        'title': 'PLAYLISTS',
        'header_style': '_',
        'options': {
            '1': 'Create Playlist',
            '2': 'View Playlists',
            '3': 'Add Track to Playlist',
            '4': 'Queue Playlist',
            '5': 'Import',
            'b': 'Back'
        }
    }
}

def displayMenu(menuKey, **kwargs):
    """
    [UNIVERSAL MENU DISPLAY FUNCTION]
    
    Displays any menu from MENUS dictionary
    Supports dynamic options based on state (for queue menu)
    
    PARAMETERS:
    - menuKey: key to lookup in MENUS dictionary
    - **kwargs: additional state for dynamic menus (playbackActive, etc.)
    """
    menu = MENUS.get(menuKey)
    
    if not menu:
        # Handle dynamic queue menu
        if menuKey == 'queue':
            displayQueueMenu(
                kwargs.get('playbackActive', False),
                kwargs.get('repeatActive', False),
                kwargs.get('shuffleActive', False)
            )
            return
        return
    
    # Display menu header
    title = menu['title']
    style = menu['header_style']
    
    if style == '=':
        print("\n" + "="*35)
        print(f"======= {title} =======")
        print("="*35)
    else:
        print(f"\n{style*5}{title}{style*5}")
    
    # Display options
    for key, label in menu['options'].items():
        print(f"{key}: {label}")
    
    if style == '=':
        print("="*35)

def displayQueueMenu(playbackActive, repeatActive, shuffleActive):
    """Dynamic queue menu based on playback state"""
    if playbackActive:
        print("1: Pause")
    else:
        print("1: Play")
    
    print("2: Next")
    print("3: Previous")
    
    if repeatActive:
        print("4: Turn off repeat")
    else:
        print("4: Turn on repeat")
    
    if shuffleActive:
        print("5: Turn off shuffle")
    else:
        print("5: Turn on shuffle")
    
    print("6: Clear queue")
    print("x: Exit queue")

# [ACTION HANDLERS - DICTIONARY MAPPING]
# These dictionaries will map user input (like '1', '2') to the actual function to call
# This is cleaner than using many if-elif statements
LIBRARY_ACTIONS = {}
PLAYLIST_ACTIONS = {}
BROWSE_ACTIONS = {}
QUEUE_ACTIONS = {}

def handleCreateTrack():
    """Handler for creating a new track"""
    print("\n_____Add New Track_____")
    trackTitle = input("Title: ")
    artistInput = input("Artist (separate multiple with comma): ")
    
    # Handle multiple artists
    if "," in artistInput:
        artistData = [a.strip() for a in artistInput.split(",")]
    else:
        artistData = artistInput.strip()
    
    albumName = input("Album: ")
    trackDuration = input("Duration (mm:ss): ")
    if ":" not in trackDuration or len(trackDuration.split(":")) != 2:
        print("Invalid duration format! Use mm:ss")
        return
    
    newTrack = Track(trackTitle, artistData, albumName, trackDuration)
    musicLibrary.addTrack(newTrack)
    print("Track added successfully!")

def handleViewLibrary():
    """Handler for viewing library with pagination"""
    currentPage = 1
    while True:
        totalPageCount = musicLibrary.displayLibrary(currentPage)
        if not totalPageCount:
            input("Press Enter to continue...")
            break
        elif totalPageCount == 1:
            print("-" * 35)
            print("a: Add to queue")
            print("b: Back")
            print("-" * 35)
            navChoice = input(">> ")
            if navChoice.lower() == 'a':
                handleAddTrackToQueue()
            elif navChoice.lower() == 'b':
                break
            continue
        
        print("-" * 35)
        print("n: Next")
        print("p: Previous")
        print("a: Add to queue")
        print("b: Back")
        print("-" * 35)
        navChoice = input(">> ")
        if navChoice.lower() == 'n' and currentPage < totalPageCount:
            currentPage += 1
        elif navChoice.lower() == 'p' and currentPage > 1:
            currentPage -= 1
        elif navChoice.lower() == 'a':
            handleAddTrackToQueue()
        elif navChoice.lower() == 'b':
            break

def handleAddTrackToQueue():
    """Helper to add track to queue"""
    try:
        trackNumber = int(input("Enter track number to add to queue: "))
        selectedTrack = musicLibrary.getTrackByIndex(trackNumber - 1)
        if selectedTrack:
            wasAdded = playbackQueue.addTrack(selectedTrack)
            if wasAdded:
                playbackQueue.saveQueueState()
                print(f"Added '{selectedTrack.getTitle()}' to queue!")
            input("Press Enter to continue...")
        else:
            print("Invalid track number!")
    except:
        print("Invalid input!")

def handleSearchTrack():
    """Handler for searching tracks"""
    searchQuery = input("Enter track title to search: ")
    searchResults = musicLibrary.searchTracksByTitle(searchQuery)
    
    if searchResults:
        print("\n_____Search Results_____")
        for idx, track in enumerate(searchResults, 1):
            print(f"({idx}) {track.formatDisplay()}")
    else:
        print("No tracks found!")

def handleImportTracks():
    """Handler for importing tracks"""
    print("\n_____Import Tracks_____")
    print("Available files: tracks.json, tracks.csv")
    fileName = input("Enter filename (tracks.json or tracks.csv): ")
    
    importPath = fileName
    
    print(f"\nImporting from {importPath}...")
    importResult = musicLibrary.importTracks(importPath)
    
    if importResult["success"]:
        print(f"\nImport successful!")
    else:
        print(f"\nImport failed!")
    
    input("\nPress Enter to continue...")

# Map library actions
LIBRARY_ACTIONS = {
    '1': handleCreateTrack,
    '2': handleViewLibrary,
    '3': handleSearchTrack,
    '4': handleImportTracks
}

def processLibrary():
    """Main library processing loop using dictionary dispatch"""
    while True:
        displayMenu('library')
        print("-" * 35)
        userChoice = input(">> ")
        
        # Dictionary-based action dispatch
        # Instead of if userChoice == '1': handleCreateTrack()
        # We look up the function in the dictionary and call it
        action = LIBRARY_ACTIONS.get(userChoice)
        if action:
            action()  # Call the function we found
        elif userChoice.lower() == "b":
            break
        else:
            print("Invalid choice!")

def handleCreatePlaylist():
    """Handler for creating playlist"""
    playlistName = input("Enter playlist name: ")
    result = playlistMgr.createPlaylist(playlistName)
    if result:
        print(f"Playlist '{playlistName}' created!")
    else:
        print("Playlist name already exists!")

def handleViewPlaylists():
    """Handler for viewing playlists with pagination and options"""
    currentPage = 1
    sortedPlaylistList = None
    
    while True:
                totalPageCount = playlistMgr.showPlaylists(currentPage, sortedPlaylistList)
                if not totalPageCount:
                    # Empty playlists
                    break
                
                if totalPageCount > 1:
                    print("-" * 35)
                    print("n: Next")
                    print("p: Previous")
                    print("v: View")
                    print("q: Queue")
                    print("s: Sort")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                else:
                    print("-" * 35)
                    print("v: View")
                    print("q: Queue")
                    print("s: Sort")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                
                if navChoice.lower() == 'n' and currentPage < totalPageCount:
                    currentPage += 1
                elif navChoice.lower() == 'p' and currentPage > 1:
                    currentPage -= 1
                elif navChoice.lower() == 's':
                    # Sort playlists
                    print("\n_____Sort Playlists By_____")
                    print("1: Date Created")
                    print("2: Name")
                    print("3: Duration")
                    print("4: Back to original order")
                    print("-" * 35)
                    
                    sortChoice = input(">> ")
                    
                    if sortChoice == "1":
                        sortedPlaylistList = playlistMgr.arrangePlaylists("date_created")
                        print("\nPlaylists sorted by date created!")
                        currentPage = 1
                    elif sortChoice == "2":
                        sortedPlaylistList = playlistMgr.arrangePlaylists("name")
                        print("\nPlaylists sorted by name!")
                        currentPage = 1
                    elif sortChoice == "3":
                        sortedPlaylistList = playlistMgr.arrangePlaylists("duration")
                        print("\nPlaylists sorted by duration!")
                        currentPage = 1
                    elif sortChoice == "4":
                        sortedPlaylistList = None
                        print("\nBack to original order!")
                        currentPage = 1
                elif navChoice.lower() == 'q':
                    # Queue playlist directly
                    try:
                        playlistNum = int(input("Enter playlist number: "))
                        selectedPlaylist = playlistMgr.getPlaylistByIndex(playlistNum - 1, sortedPlaylistList)
                        
                        if selectedPlaylist:
                            playbackQueue.clearQueue()
                            playbackQueue.loadTracks(selectedPlaylist.getTracks())
                            print(f"Queue created from playlist '{selectedPlaylist.getName()}'!")
                            input("Press Enter to continue...")
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif navChoice.lower() == 'v':
                    # View playlist details
                    try:
                        playlistNum = int(input("Enter playlist number: "))
                        selectedPlaylist = playlistMgr.getPlaylistByIndex(playlistNum - 1, sortedPlaylistList)
                        
                        if selectedPlaylist:
                            # View playlist loop with sorting
                            while True:
                                # Display the playlist
                                selectedPlaylist.showPlaylist()
                                
                                # Show playlist options
                                print("-" * 35)
                                print("s: Sort")
                                print("q: Queue")
                                print("b: Back")
                                print("-" * 35)
                                action = input(">> ")
                                
                                if action.lower() == 's':
                                    # Sort tracks in playlist
                                    print("\n_____Sort Tracks By_____")
                                    print("1: Date added")
                                    print("2: Title")
                                    print("3: Artist")
                                    print("4: Duration")
                                    print("5: Back")
                                    print("-" * 35)
                                    
                                    sortChoice = input(">> ")
                                    
                                    if sortChoice == "1":
                                        selectedPlaylist.sortTracks("date_added")
                                        print("\nTracks sorted by date added!")
                                    elif sortChoice == "2":
                                        selectedPlaylist.sortTracks("title")
                                        print("\nTracks sorted by title!")
                                    elif sortChoice == "3":
                                        selectedPlaylist.sortTracks("artist")
                                        print("\nTracks sorted by artist!")
                                    elif sortChoice == "4":
                                        selectedPlaylist.sortTracks("duration")
                                        print("\nTracks sorted by duration!")
                                    
                                elif action.lower() == 'q':
                                    # Queue playlist in current sort order
                                    playbackQueue.clearQueue()
                                    playbackQueue.loadTracks(selectedPlaylist.getTracks())
                                    print(f"Queue created from playlist '{selectedPlaylist.getName()}'!")
                                    input("Press Enter to continue...")
                                    break
                                elif action.lower() == 'b':
                                    break
                        else:
                            print("Invalid playlist number!")
                    except:
                        print("Invalid input!")
                elif navChoice.lower() == 'b':
                    break

def handleAddTrackToPlaylist():
    """Handler for adding track to playlist"""
    currentPage = 1
    selectedPlaylistName = None
    
    # Browse playlists with pagination
    while True:
                totalPageCount = playlistMgr.showPlaylists(currentPage)
                if not totalPageCount:
                    break
                
                # Show options
                if totalPageCount > 1:
                    print("-" * 35)
                    print("n: Next")
                    print("p: Previous")
                    print("s: Select playlist")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                else:
                    print("-" * 35)
                    print("s: Select playlist")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                
                if navChoice.lower() == 'n' and currentPage < totalPageCount:
                    currentPage += 1
                elif navChoice.lower() == 'p' and currentPage > 1:
                    currentPage -= 1
                elif navChoice.lower() == 's':
                    # Select playlist
                    try:
                        playlistNum = int(input("Enter playlist number: "))
                        selectedPlaylist = playlistMgr.getPlaylistByIndex(playlistNum - 1)
                        
                        if not selectedPlaylist:
                            print("Invalid playlist number!")
                            continue
                        else:
                            selectedPlaylistName = selectedPlaylist.getName()
                            break
                    except:
                        print("Invalid input!")
                elif navChoice.lower() == 'b':
                    break
    
    # If no playlist selected, return
    if not selectedPlaylistName:
        return
    
    # Browse library with pagination
    currentPage = 1
    while True:
                totalPageCount = musicLibrary.displayLibrary(currentPage)
                if not totalPageCount:
                    break
                
                # Show navigation
                if totalPageCount > 1:
                    print("-" * 35)
                    print("n: Next")
                    print("p: Previous")
                    print("x: Add track")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                else:
                    print("-" * 35)
                    print("x: Add track")
                    print("b: Back")
                    print("-" * 35)
                    navChoice = input(">> ")
                
                if navChoice.lower() == 'n' and currentPage < totalPageCount:
                    currentPage += 1
                elif navChoice.lower() == 'p' and currentPage > 1:
                    currentPage -= 1
                elif navChoice.lower() == 'x':
                    # Add track
                    try:
                        trackNum = int(input("Enter track number to add: "))
                        selectedTrack = musicLibrary.getTrackByIndex(trackNum - 1)
                        
                        if selectedTrack:
                            if playlistMgr.appendTrackToPlaylist(selectedPlaylistName, selectedTrack):
                                print("Track added to playlist!")
                            else:
                                print("Track already in playlist!")
                        else:
                            print("Invalid track number!")
                    except:
                        print("Invalid input!")
                elif navChoice.lower() == 'b':
                    break

def handleQueuePlaylist():
    """Handler for queuing a playlist"""
    currentPage = 1
    
    # Browse playlists
    while True:
        totalPageCount = playlistMgr.showPlaylists(currentPage)
        if not totalPageCount:
            break
        
        # Show options
        if totalPageCount > 1:
            print("-" * 35)
            print("n: Next")
            print("p: Previous")
            print("c: Create queue")
            print("b: Back")
            print("-" * 35)
            navChoice = input(">> ")
        else:
            print("-" * 35)
            print("c: Create queue")
            print("b: Back")
            print("-" * 35)
            navChoice = input(">> ")
        
        if navChoice.lower() == 'n' and currentPage < totalPageCount:
            currentPage += 1
        elif navChoice.lower() == 'p' and currentPage > 1:
            currentPage -= 1
        elif navChoice.lower() == 'c':
            # Select playlist
            try:
                playlistNum = int(input("Enter playlist number: "))
                selectedPlaylist = playlistMgr.getPlaylistByIndex(playlistNum - 1)
                
                if selectedPlaylist:
                    playbackQueue.clearQueue()
                    playbackQueue.loadTracks(selectedPlaylist.getTracks())
                    print("Queue created from playlist!")
                    input("Press Enter to continue...")
                    break
                else:
                    print("Invalid playlist number!")
            except:
                print("Invalid input!")
        elif navChoice.lower() == 'b':
            break

def handleImportPlaylists():
    """Handler for importing playlists"""
    print("\n_____Import Playlists_____")
    print("Available files: playlists.json, playlists.csv")
    fileName = input("Enter filename (playlists.json or playlists.csv): ")
    
    importPath = fileName
    
    print(f"\nImporting from {importPath}...")
    importResult = playlistMgr.importPlaylists(importPath)
    
    if importResult["success"]:
        print(f"\nImport successful!")
    else:
        print(f"\nImport failed!")
    
    input("\nPress Enter to continue...")

# Map playlist actions
PLAYLIST_ACTIONS = {
    '1': handleCreatePlaylist,
    '2': handleViewPlaylists,
    '3': handleAddTrackToPlaylist,
    '4': handleQueuePlaylist,
    '5': handleImportPlaylists
}

def processPlaylists():
    """Main playlist processing loop using dictionary dispatch"""
    while True:
        displayMenu('playlist')
        print("-" * 35)
        userChoice = input(">> ")
        
        # Dictionary-based action dispatch
        action = PLAYLIST_ACTIONS.get(userChoice)
        if action:
            action()
        elif userChoice.lower() == "b":
            break
        else:
            print("Invalid choice!")

def processAlbums():
    """Handle album browsing"""
    albumMgr = musicLibrary.getAlbumManager()
    currentPage = 1
    
    while True:
        totalPageCount = albumMgr.showAlbums(currentPage)
        if not totalPageCount:
            # Empty albums
            input("Press Enter to continue...")
            break
        
        # Show options
        if totalPageCount > 1:
            print("-" * 35)
            print("n: Next")
            print("p: Previous")
            print("v: View")
            print("q: Queue")
            print("b: Back")
            print("-" * 35)
            navChoice = input(">> ")
        else:
            print("-" * 35)
            print("v: View")
            print("q: Queue")
            print("b: Back")
            print("-" * 35)
            navChoice = input(">> ")
        
        if navChoice.lower() == 'n' and currentPage < totalPageCount:
            currentPage += 1
        elif navChoice.lower() == 'p' and currentPage > 1:
            currentPage -= 1
        elif navChoice.lower() == 'q':
            # Queue album directly
            try:
                albumNum = int(input("Enter album number: "))
                selectedAlbum = albumMgr.getAlbumByIndex(albumNum - 1)
                
                if selectedAlbum:
                    playbackQueue.clearQueue()
                    playbackQueue.loadTracks(selectedAlbum.getTracks())
                    print(f"Queue created from album '{selectedAlbum.getName()}'!")
                    input("Press Enter to continue...")
                else:
                    print("Invalid album number!")
            except:
                print("Invalid input!")
        elif navChoice.lower() == 'v':
            # View album details
            try:
                albumNum = int(input("Enter album number: "))
                selectedAlbum = albumMgr.getAlbumByIndex(albumNum - 1)
                
                if selectedAlbum:
                    selectedAlbum.showAlbum()
                    
                    # Show album options
                    print("-" * 35)
                    print("q: Queue")
                    print("b: Back")
                    print("-" * 35)
                    action = input(">> ")
                    
                    if action.lower() == 'q':
                        # Queue album
                        playbackQueue.clearQueue()
                        playbackQueue.loadTracks(selectedAlbum.getTracks())
                        print(f"Queue created from album '{selectedAlbum.getName()}'!")
                        input("Press Enter to continue...")
                else:
                    print("Invalid album number!")
            except:
                print("Invalid input!")
        elif navChoice.lower() == 'b':
            break

# Map browse actions
BROWSE_ACTIONS = {
    '1': processLibrary,
    '2': processAlbums,
    '3': processPlaylists
}

def processBrowseTracks():
    """Handle browse tracks submenu using dictionary dispatch"""
    while True:
        displayMenu('browse_tracks')
        print("-" * 35)
        userChoice = input(">> ")
        
        # Dictionary-based action dispatch
        action = BROWSE_ACTIONS.get(userChoice)
        if action:
            action()
        elif userChoice.lower() == "b":
            break
        else:
            print("Invalid choice!")

def handlePlayPause():
    """Handler for play/pause toggle"""
    if playbackQueue.isPlaying():
        playbackQueue.pausePlayback()
        print("Paused.")
    else:
        playbackQueue.startPlayback()
        print("Playing...")

def handleNext():
    """Handler for next track"""
    nextTrack = playbackQueue.advanceToNext()
    if nextTrack:
        print(f"Now playing: {nextTrack.formatDisplay()}")
    else:
        print("End of queue!")

def handlePrevious():
    """Handler for previous track"""
    prevTrack = playbackQueue.rewindToPrevious()
    if prevTrack:
        print(f"Now playing: {prevTrack.formatDisplay()}")

def handleToggleRepeat():
    """Handler for repeat toggle"""
    repeatState = playbackQueue.toggleRepeat()
    print(f"Repeat: {'ON' if repeatState else 'OFF'}")

def handleToggleShuffle():
    """Handler for shuffle toggle"""
    if playbackQueue.isShuffled():
        playbackQueue.restoreOriginalOrder()
        print("Shuffle turned OFF")
    else:
        playbackQueue.shuffleQueue()
        print("Shuffle turned ON")

def handleClearQueue():
    """Handler for clearing queue"""
    confirm = input("Clear queue? (y/n): ")
    if confirm.lower() == 'y':
        playbackQueue.clearQueue()
        print("Queue cleared!")

# Map queue actions
QUEUE_ACTIONS = {
    '1': handlePlayPause,
    '2': handleNext,
    '3': handlePrevious,
    '4': handleToggleRepeat,
    '5': handleToggleShuffle,
    '6': handleClearQueue
}

def processQueue():
    """Main queue processing loop using dictionary dispatch"""
    playbackQueue.loadQueueState()
    
    currentPage = 1
    
    while True:
        playbackQueue.showQueue(currentPage)
        displayMenu('queue', 
                   playbackActive=playbackQueue.isPlaying(),
                   repeatActive=playbackQueue.isRepeatOn(),
                   shuffleActive=playbackQueue.isShuffled())
        print("-" * 35)
        userChoice = input(">> ")
        
        # Dictionary-based action dispatch
        action = QUEUE_ACTIONS.get(userChoice)
        if action:
            action()
        elif userChoice.lower() == "x":
            break
        else:
            print("Invalid choice!")

# Map main menu actions
MAIN_ACTIONS = {
    '1': processBrowseTracks,
    '2': processQueue
}

def executeMain():
    """Main entry point using dictionary dispatch"""
    print("Welcome to Listen to the Music!")
    
    while True:
        displayMenu('main')
        userChoice = input(">> ")
        
        # Dictionary-based action dispatch
        action = MAIN_ACTIONS.get(userChoice)
        if action:
            action()
        elif userChoice == "0":
            print("Thanks for using Listen to the Music!")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    executeMain()
