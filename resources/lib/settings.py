#!/usr/bin/python
# -*- coding: utf-8 -*-

import xbmc
import xbmcgui
import xbmcaddon
import json
import os

ADDON = xbmcaddon.Addon()
ADDON_ID = ADDON.getAddonInfo('id')
ADDON_DATA = xbmc.translatePath(f"special://profile/addon_data/{ADDON_ID}")
CONFIG_FILE = os.path.join(ADDON_DATA, "settings.json")

class SettingsDialog(xbmcgui.WindowXMLDialog):
    def __init__(self, *args, **kwargs):
        self.config = self.load_config()
        
    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            return {
                "auto_clean": False,
                "clean_interval": 24,
                "overclock_enabled": False,
                "overclock_settings": {
                    "arm_freq": 1500,
                    "gpu_freq": 500,
                    "core_freq": 500,
                    "sdram_freq": 500
                }
            }
        
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    
    def save_config(self):
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=4)
    
    def onInit(self):
        # Set up controls
        self.auto_clean = self.getControl(100)
        self.clean_interval = self.getControl(101)
        self.overclock_enabled = self.getControl(102)
        self.arm_freq = self.getControl(103)
        self.gpu_freq = self.getControl(104)
        self.core_freq = self.getControl(105)
        self.sdram_freq = self.getControl(106)
        
        # Set initial values
        self.auto_clean.setSelected(self.config["auto_clean"])
        self.clean_interval.setLabel(str(self.config["clean_interval"]))
        self.overclock_enabled.setSelected(self.config["overclock_enabled"])
        self.arm_freq.setLabel(str(self.config["overclock_settings"]["arm_freq"]))
        self.gpu_freq.setLabel(str(self.config["overclock_settings"]["gpu_freq"]))
        self.core_freq.setLabel(str(self.config["overclock_settings"]["core_freq"]))
        self.sdram_freq.setLabel(str(self.config["overclock_settings"]["sdram_freq"]))
    
    def onClick(self, controlId):
        if controlId == 200:  # Save button
            self.config["auto_clean"] = self.auto_clean.isSelected()
            self.config["clean_interval"] = int(self.clean_interval.getLabel())
            self.config["overclock_enabled"] = self.overclock_enabled.isSelected()
            self.config["overclock_settings"]["arm_freq"] = int(self.arm_freq.getLabel())
            self.config["overclock_settings"]["gpu_freq"] = int(self.gpu_freq.getLabel())
            self.config["overclock_settings"]["core_freq"] = int(self.core_freq.getLabel())
            self.config["overclock_settings"]["sdram_freq"] = int(self.sdram_freq.getLabel())
            
            self.save_config()
            self.close()
        
        elif controlId == 201:  # Cancel button
            self.close()
        
        elif controlId == 300:  # Clear Cache button
            xbmc.executebuiltin("RunScript(service.opti.core,clear_cache)")
            xbmcgui.Dialog().ok("OptiCore", "Cache cleared successfully!") 