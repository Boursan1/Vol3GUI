#
#   Christopher Place
#   CS498 Capstone
#   Filename: plugins.py
#
#   Overview:
#       Imports volatility framework to extract the plugin names prior the the program runs via CLI
#       Command ran by Updater.js in order to get dropdown options for Windows, Mac & Linux
#
import json
from typing import List,Dict
import sys
import os

vol_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'volatility3')
sys.path.insert(0, vol_dir)

from volatility.framework import constants, interfaces
from volatility import framework, plugins
import volatility


def get_plugins():
    volatility.plugins.__path__ = constants.PLUGINS_PATH
    volatility.framework.import_files(volatility.plugins, True)
    osJSON, commandJSON, nameJSON = [], [], []

    for plugin in volatility.framework.class_subclasses(interfaces.plugins.PluginInterface):
        pluginCommand = (plugin.__module__ + "." +
                         plugin.__name__).replace('volatility.plugins.', '')
        os = ['windows.', 'mac.', 'linux.']
        if any(string in pluginCommand for string in os):
            osJSON.append(pluginCommand.split('.', 1)[0])
            commandJSON.append(pluginCommand)
            nameJSON.append(pluginCommand.rsplit('.', 1)[1])
    pluginJSON = [{"OS": i, "Command": x, "Name": y}
                  for i, x, y in zip(osJSON, commandJSON, nameJSON)]

    outputPath = './plugins.json'
    with open(outputPath, 'w+') as json_file:
        json.dump(pluginJSON, json_file, indent=2)
    return 'Success'


print(get_plugins())
