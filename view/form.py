import toga, os
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, CENTER
from screeninfo import get_monitors
screen = get_monitors()[0]
from ..fileSystem.yaml import Yaml
    
class Form(object):
    def __init__(self, app, container, popup=False):
        self.app = app
        self.popup = popup
        if popup:
            height = 480
            width = 640
            self.container = toga.Box(style=Pack(direction=COLUMN))
            self.app.modal_window = toga.Window(id="modal", title='Second window', closeable=False, resizeable=False, position=((screen.width-width)/2, (screen.height-height)/2))
            self.app.windows.add(self.app.modal_window)
            
            self.app.modal_window.content = self.container
            self.app.modal_window.minimizable=True
            self.app.modal_window.show()
            self.app.modal_window.on_close = self.window_close

        else:
            self.container = container
        self.path_form = os.path.dirname(self.app.config[0])+self.app.config[1]
         

    def show_modal(self):
        self.app.modal_window.show()
    
    async def close_modal(self, widget):
        if await self.app.modal_window.confirm_dialog('Confirmation', 'Are you sure?'):            
            self.app.menu.toggle([self.app.menu_active])
            self.app.menu_active = None
            self.app.popup = False
            self.app.modal_window.close()
            return True

        return False
        
        
    async def window_close(self):
        print('aaa')
        if await self.app.main_window.confirm_dialog('Confirmation', 'Are you sure?'):            
            self.app.menu.toggle([self.app.menu_active])
            self.app.menu_active = None
            self.app.popup = False
            return True

        return False

    def generate(self, form_config):
        if type(form_config)==str :
            config = Yaml().load(self.path_form+'/'+form_config+'.yaml')
        else:
            config = form_config
        
        children = self.container.children
        length = len(children) 
        for i in range(length):
            self.container.remove(children[length-1-i]) 
    
        if config.get('title'):
            if self.popup:
                self.app.modal_window.title = config.get('title')
            else:
                self.container.add(toga.Label(config.get('title'), id='title', style=Pack(padding=(0,0,10,10), text_align=CENTER)))

        if config.get('inputs'):
            boxInput = toga.Box(id="box_input", style = Pack( direction=COLUMN , padding=(0,30,0,30)))
            self.container.add(boxInput)
            labels = {}
            inputs = {}
            for input in config['inputs']:
                id = input.get('id')
                if input.get('label'):
                    labels[id] = toga.Label(input.get('label'))
                    boxInput.add(labels[id])

                if input['type'] == 'text':
                    inputs[id] = toga.TextInput(id = input.get('id'))

                elif input['type'] == 'textarea':
                    inputs[id] = toga.MultilineTextInput(id = input.get('id'), 
                        style=Pack(height=input['height'] if input.get('height') else 40) 
                    ) 
                elif input['type'] == 'password':
                    inputs[id] = toga.PasswordInput(id = input.get('id'))
            
                elif input['type'] == 'dropdown':
                    inputs[id] = toga.Selection(
                        items = input.get('options'),
                        id = input.get('id'), 
                    )
                    if input.get('on_select'):
                        inputs[id].on_select = input.get('on_select')
                    else:
                        inputs[id].on_select = self.app.selection_select


                if input.get('value'):
                    inputs[id].value = input.get('value')

                if input.get('readonly')==True:
                    inputs[id].readonly = True,

                if input.get('on_change'):
                    inputs[id].on_change = input.get('on_change')
                else:
                    inputs[id].on_change = self.app.input_change
                 

                inputs[id].placeholder = input['placeholder'] if input.get('placeholder')  else input.get('label')
                boxInput.add(inputs[id])
        
        if config.get('buttons'):
            boxButton = toga.Box(id="box_button", style = Pack( direction=ROW , padding=(0,30,0,30)))
            self.container.add(boxButton)
            buttons = {}
            for button in config['buttons']:
                id = button.get('id')
                buttons[id] = toga.Button(
                    text = button.get('caption'),
                    id = button.get('id'),
                    on_press = button.get('on_press'),
                    enabled = button.get('enabled')
                )
                if button.get('on_press') :
                    buttons[id].on_press = button.get('on_press')
                else:
                    buttons[id].on_press = self.app.button_press
                
                boxButton.add(buttons[id])
            
            if config.get('close'):
                boxButton.add(toga.Button(
                    text='Close',
                    on_press=self.close_modal
                ))

