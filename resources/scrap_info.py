#
# Advanced Emulator Launcher scraping engine
#

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# -----------------------------------------------------------------------------
# We support online an offline scrapers.
# Note that this module does not depend on Kodi stuff at all, and can be
# called externally from console Python scripts for testing of the scrapers.
# -----------------------------------------------------------------------------

# Load replacements for functions that depend on Kodi modules.
# This enables running this module in standard Python for testing scrapers.
try: import xbmc
except: from standalone import *
from disk_IO import *

# Python standard library
import xml.etree.ElementTree as ET 
import re

# -----------------------------------------------------------------------------
# Miscellaneous emulator and gamesys (platforms) supported.
# -----------------------------------------------------------------------------
def emudata_get_program_arguments( app ):
    # Based on the app. name, retrieve the default arguments for the app.
    app = app.lower()
    applications = {
        'mame'        : '"%rom%"',
        'mednafen'    : '-fs 1 "%rom%"',
        'mupen64plus' : '--nogui --noask --noosd --fullscreen "%rom%"',
        'nestopia'    : '"%rom%"',
        'xbmc'        : 'PlayMedia(%rom%)',
        'retroarch'   : '-L /path/to/core "%rom%"',
        'yabause'     : '-a -f -i "%rom%"',
    }
    for application, arguments in applications.iteritems():
        if app.find(application) >= 0:
            return arguments

    return '"%rom%"'

def emudata_get_program_extensions( app ):
    # Based on the app. name, retrieve the recognized extension of the app.
    app = app.lower()
    applications = {
        'mame'       : 'zip|7z',
        'mednafen'   : 'zip|cue|iso',
        'mupen64plus': 'z64|zip|n64',
        'nestopia'   : 'nes|zip',
        'retroarch'  : 'zip|cue|iso',
        'yabause'    : 'cue',
    }
    for application, extensions in applications.iteritems():
        if app.find(application) >= 0:
            return extensions

    return ""

#
# This dictionary has the AEL "official" game system list as key, and the XML file 
# with offline scraping information as value. File location is relative to
# this file location, CURRENT_ADDON_DIR/resources/.
#
offline_scrapers_dic = {
    'MAME'             : 'scraper_data/MAME.xml', 
    'Sega 32X'         : 'scraper_data/Sega 32x.xml',
    'Nintendo SNES'    : 'scraper_data/Super Nintendo Entertainment System.xml'
}

def emudata_game_system_list():
    game_list = []
    
    for key in sorted(offline_scrapers_dic):
        game_list.append(key)

    return game_list

# -----------------------------------------------------------------------------
# Translation of AEL oficial gamesys (platform) name to scraper particular name
# -----------------------------------------------------------------------------
AEL_gamesys_to_TheGamesDB = {
    'test' : 'test GamesDB'
}