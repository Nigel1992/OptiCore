#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui
import time
import json
import subprocess
import shutil
from datetime import datetime

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_PATH = ADDON.getAddonInfo('path')
ADDON_DATA = xbmc.translatePath(f"special://profile/addon_data/{ADDON_ID}")

# Cache directories
KODI_CACHE = xbmc.translatePath("special://temp")
YOUTUBE_CACHE = os.path.join(KODI_CACHE, "youtube")
SYSTEM_CACHE = "/storage/.cache"

# Config file path
CONFIG_FILE = os.path.join(ADDON_DATA, "settings.json")

def log(message):
    xbmc.log(f"{ADDON_NAME}: {message}", xbmc.LOGINFO)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "auto_clean": False,
            "clean_interval": 24,  # hours
            "overclock_enabled": False,
            "overclock_settings": {
                "arm_freq": 1500,
                "gpu_freq": 500,
                "core_freq": 500,
                "sdram_freq": 500
            }
        }
        os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f, indent=4)
        return default_config
    
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def clear_cache():
    try:
        # Clear Kodi cache
        for item in os.listdir(KODI_CACHE):
            path = os.path.join(KODI_CACHE, item)
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
        
        # Clear YouTube cache
        if os.path.exists(YOUTUBE_CACHE):
            shutil.rmtree(YOUTUBE_CACHE)
        
        # Clear system cache
        if os.path.exists(SYSTEM_CACHE):
            for item in os.listdir(SYSTEM_CACHE):
                path = os.path.join(SYSTEM_CACHE, item)
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
        
        log("Cache cleared successfully")
        return True
    except Exception as e:
        log(f"Error clearing cache: {str(e)}")
        return False

def apply_overclock(config):
    if not config["overclock_enabled"]:
        return
    
    try:
        # Create config.txt backup if it doesn't exist
        config_path = "/flash/config.txt"
        backup_path = "/flash/config.txt.bak"
        
        if not os.path.exists(backup_path):
            shutil.copy2(config_path, backup_path)
        
        # Read current config
        with open(config_path, 'r') as f:
            lines = f.readlines()
        
        # Update overclock settings
        overclock_settings = config["overclock_settings"]
        new_settings = [
            f"arm_freq={overclock_settings['arm_freq']}\n",
            f"gpu_freq={overclock_settings['gpu_freq']}\n",
            f"core_freq={overclock_settings['core_freq']}\n",
            f"sdram_freq={overclock_settings['sdram_freq']}\n"
        ]
        
        # Write new config
        with open(config_path, 'w') as f:
            f.writelines(lines)
            f.write("\n# OptiCore overclock settings\n")
            f.writelines(new_settings)
        
        log("Overclock settings applied successfully")
        return True
    except Exception as e:
        log(f"Error applying overclock settings: {str(e)}")
        return False

def monitor():
    config = load_config()
    last_clean = datetime.now()
    
    while not xbmc.Monitor().abortRequested():
        if config["auto_clean"]:
            current_time = datetime.now()
            hours_since_last_clean = (current_time - last_clean).total_seconds() / 3600
            
            if hours_since_last_clean >= config["clean_interval"]:
                if clear_cache():
                    last_clean = current_time
        
        # Sleep for 1 minute before next check
        xbmc.Monitor().waitForAbort(60)

if __name__ == "__main__":
    log("Service started")
    monitor() 