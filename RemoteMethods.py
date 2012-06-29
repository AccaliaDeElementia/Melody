#!/usr/bin/python

Methods = [
    {
        "returns": None, 
        "params": [
            "method"
        ], 
        "method": "help", 
        "defaults": {
            "method": None
        }, 
        "help": None
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "type_", 
            "needle"
        ], 
        "method": "libraryFind", 
        "defaults": {}, 
        "help": "Return a list of songs where [needle] exactly matches metadata [type_]."
    }, 
    {
        "returns": "list_library", 
        "params": [
            "path"
        ], 
        "method": "libraryList", 
        "defaults": {
            "path": "/"
        }, 
        "help": "Return a list of the contents of a directory in the music library."
    }, 
    {
        "returns": "list_library", 
        "params": [], 
        "method": "libraryListAll", 
        "defaults": {}, 
        "help": "Return a list of all songs in the music library."
    }, 
    {
        "returns": "job_id", 
        "params": [
            "path"
        ], 
        "method": "libraryRescan", 
        "defaults": {
            "path": "/"
        }, 
        "help": "Rescan music library, starting at [path]."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "type_", 
            "needle"
        ], 
        "method": "librarySearch", 
        "defaults": {}, 
        "help": "Return a list of songs where metadata [type_] contains [needle]."
    }, 
    {
        "returns": "stats", 
        "params": [], 
        "method": "libraryStats", 
        "defaults": {}, 
        "help": "Return basic statistics about the music library."
    }, 
    {
        "returns": "job_id", 
        "params": [
            "path"
        ], 
        "method": "libraryUpdate", 
        "defaults": {
            "path": "/"
        }, 
        "help": "Look for changes in music library, starting at [path]."
    }, 
    {
        "returns": None, 
        "params": [
            "name", 
            "path"
        ], 
        "method": "playlistAdd", 
        "defaults": {}, 
        "help": "Add [path] to stored playlist [name] and return updated playlist."
    }, 
    {
        "returns": None, 
        "params": [
            "name"
        ], 
        "method": "playlistClear", 
        "defaults": {}, 
        "help": "Clear contents of stored playlist [name] and return updated playlist."
    }, 
    {
        "returns": None, 
        "params": [
            "name"
        ], 
        "method": "playlistDelete", 
        "defaults": {}, 
        "help": "Delete stored playlist [name]."
    }, 
    {
        "returns": None, 
        "params": [
            "name"
        ], 
        "method": "playlistInfo", 
        "defaults": {}, 
        "help": "Return a list of songs contained in stored playlist [name]."
    }, 
    {
        "returns": None, 
        "params": [], 
        "method": "playlistList", 
        "defaults": {}, 
        "help": "Return a list of stored playlist names."
    }, 
    {
        "returns": None, 
        "params": [
            "name", 
            "from_", 
            "to_"
        ], 
        "method": "playlistMove", 
        "defaults": {}, 
        "help": "Move position [from_] to position [to_] in stored playlist [name] and return updated playlist."
    }, 
    {
        "returns": None, 
        "params": [
            "name", 
            "songid"
        ], 
        "method": "playlistRemove", 
        "defaults": {}, 
        "help": "Remove [songid] from stored playlist [name] and return updated playlist."
    }, 
    {
        "returns": None, 
        "params": [
            "oldname", 
            "newname"
        ], 
        "method": "playlistRename", 
        "defaults": {}, 
        "help": "Rename stored playlist [oldname] to [newname]."
    }, 
    {
        "returns": None, 
        "params": [
            "name", 
            "path"
        ], 
        "method": "playlistReplace", 
        "defaults": {}, 
        "help": "Replace contents of stored playlist [name] with [path] and return updated playlist."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "path", 
            "position"
        ], 
        "method": "queueAdd", 
        "defaults": {
            "position": None
        }, 
        "help": "Add [path] to play queue, optionally starting at [position], and return new play queue."
    }, 
    {
        "returns": "list_songs", 
        "params": [], 
        "method": "queueClear", 
        "defaults": {}, 
        "help": "Clear play queue and return new play queue."
    }, 
    {
        "returns": "bool", 
        "params": [
            "mode"
        ], 
        "method": "queueConsume", 
        "defaults": {
            "mode": None
        }, 
        "help": "Set the play queue consume [mode], return updated value."
    }, 
    {
        "returns": "float", 
        "params": [
            "length"
        ], 
        "method": "queueCrossfade", 
        "defaults": {
            "length": None
        }, 
        "help": "Set the playback crossfade [length], return the updated value."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queueCurrent", 
        "defaults": {}, 
        "help": "Return the currently playing song."
    }, 
    {
        "returns": "list_songs", 
        "params": [], 
        "method": "queueList", 
        "defaults": {}, 
        "help": "Return a list of songs in the play queue."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "name"
        ], 
        "method": "queueLoad", 
        "defaults": {}, 
        "help": "Load play queue from playlist [name] and return new play queue."
    }, 
    {
        "returns": "float", 
        "params": [
            "delay"
        ], 
        "method": "queueMixrampDelay", 
        "defaults": {
            "delay": None
        }, 
        "help": "Set the playback mixramp [delay], return the updated value."
    }, 
    {
        "returns": "float", 
        "params": [
            "decibels"
        ], 
        "method": "queueMixrampdB", 
        "defaults": {
            "decibels": None
        }, 
        "help": "Set the playback mixramp [decibels] level, return the updated value."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "fromid", 
            "position"
        ], 
        "method": "queueMove", 
        "defaults": {}, 
        "help": "Move song [songid] to [position] and return new play queue."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queueNext", 
        "defaults": {}, 
        "help": "Advance the play queue by one song."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queuePause", 
        "defaults": {}, 
        "help": "Pause playback of play queue."
    }, 
    {
        "returns": "song", 
        "params": [
            "position"
        ], 
        "method": "queuePlay", 
        "defaults": {
            "position": None
        }, 
        "help": "Resume playback of play queue, optionally at [position]."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queuePrev", 
        "defaults": {}, 
        "help": "Rewind the play queue by one song."
    }, 
    {
        "returns": "bool", 
        "params": [
            "mode"
        ], 
        "method": "queueRandom", 
        "defaults": {
            "mode": None
        }, 
        "help": "Set the play queue randomize order [mode], return updated value."
    }, 
    {
        "returns": "list_songs", 
        "params": [], 
        "method": "queueRandomize", 
        "defaults": {}, 
        "help": "Randomize order of play queue and return new play queue."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "songid"
        ], 
        "method": "queueRemove", 
        "defaults": {}, 
        "help": "Remove song [songid] from the play queue and return new play queue."
    }, 
    {
        "returns": "bool", 
        "params": [
            "mode"
        ], 
        "method": "queueRepeat", 
        "defaults": {
            "mode": None
        }, 
        "help": "Set the play queue repeat [mode], return updated value."
    }, 
    {
        "returns": "list_songs", 
        "params": [
            "path"
        ], 
        "method": "queueReplace", 
        "defaults": {}, 
        "help": "Replace contents of play queue with [path] and return new play queue."
    }, 
    {
        "returns": None, 
        "params": [
            "name"
        ], 
        "method": "queueSave", 
        "defaults": {}, 
        "help": "Save play queue as playlist [name]."
    }, 
    {
        "returns": "bool", 
        "params": [
            "mode"
        ], 
        "method": "queueSingle", 
        "defaults": {
            "mode": None
        }, 
        "help": "Set the play queue single song [mode], return updated value."
    }, 
    {
        "returns": "status", 
        "params": [], 
        "method": "queueStatus", 
        "defaults": {}, 
        "help": "Return the genral playback status."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queueStop", 
        "defaults": {}, 
        "help": "Stop playback of play queue."
    }, 
    {
        "returns": "song", 
        "params": [], 
        "method": "queueToggle", 
        "defaults": {}, 
        "help": "Toggle play/pause of play queue."
    }, 
    {
        "returns": "int", 
        "params": [
            "volume"
        ], 
        "method": "queueVolume", 
        "defaults": {
            "volume": None
        }, 
        "help": "Set the playback [volume], return changed value."
    }
]
