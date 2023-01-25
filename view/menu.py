import toga, os
from ..fileSystem.yaml import Yaml
from ..fileSystem.file import File

class Menu(object):
    def __init__(self, app):
        self.app = app
        self.config = app.config
        self.path_icon = os.path.dirname(self.app.icons[0])+self.app.icons[1] 
        self.path_menu = os.path.dirname(self.app.config[0])+self.app.config[1] 
    
    def generate(self, data=None):
        groups = {}
        cmd = {}
        group_order = 1
        toga.Group.APP.text = 'Home'
        if data is None:
            data = Yaml().load(self.path_menu+'/menu.yaml')

        for item in data:
            i = 0
            for key in data[item]: 
                cmd[item+'_cmd'] = toga.Command(
                    self.app.menu_click,
                    text = key['text'],
                    shortcut = key.get('shortcut'),
                    enabled = key.get('enabled') and key['enabled'],
                    section = i
                )

                i += 1
                if item == 'App':
                    cmd[item+'_cmd'].group = toga.Group.APP
                else:
                    if groups.get(item) is None:
                        groups[item] = toga.Group(item, order=group_order)
                        group_order += 1

                    cmd[item+'_cmd'].group = groups[item]
            
                self.app.commands.add(cmd[item+'_cmd'])

                if key.get('toolbar') and key['toolbar']:
                    if key.get('icon'):
                        icon = File().get_path(self.path_icon+'/'+key['icon'])
                        if icon:
                            cmd[item+'_cmd'].icon = icon
                    if key.get('tooltip'):
                        cmd[item+'_cmd'].tooltip = key['tooltip']
                    else: 
                        cmd[item+'_cmd'].tooltip = key['text']
                    self.app.main_window.toolbar.add(cmd[item+'_cmd'])

    def toggle(self, data):
        for item in self.app.commands:
            if item != None and type(item) == toga.command.Command:
                if item.text in data:
                    item.enabled = not item.enabled 
