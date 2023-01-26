# beeTito (a module for beware-toga)
---
### name        : beeTito
### Description : module for beeware-Toga
### author      : Harjito
---

### Directory Structure
```
|- src
|   |- app_name
|   |   |- app.py
|   |   |- __init__.py
|   |   |- __main__.py
|   |   |- titoBee
|   |   |   |- __init__.py
|   |   |   |- auth
|   |   |   |   |- **/*.py
|   |   |   |- config
|   |   |   |   |- **/*.yaml
|   |   |   |- fileSystem
|   |   |   |   |- *.py
|   |   |   |- view
|   |   |   |   |- **/*.py
```

### User Guide

#### Create Menu

- open app_name/app.py
- import package Form, for example app_name is myApp
```
from myapp.modules import  Form
```
- create yaml in config directory for example config/menu.yaml
```
# config/menu/yaml

App :
-   text: Login
    shortcut : L
    enabled : False
    toolbar: True
    icon: gauth.png 
-   text: Logout
    shortcut : O
    enabled : False
Edit :
-   text: Data 1
    enabled : True
-   text: Data 2
    enabled : False
```

- in startup method
```
    def startup(self):
        ...
        ...
        self.main_window = toga.MainWindow(id="main", title=self.formal_name, size=(screen.width, screen.height), minimizable=False)
        self.menu = Menu(self)
        self.menu.generate()

        self.main_window.show()
```
        
#### Change Status Menu
For change status menu from disabled to enabled vise versa, use method toggle
```
  self.menu.toggle(['Login','Data 1'])
```

#### Create Form
- open app_name/app.py
- import package Form, for example app_name is myApp
```
from myapp.modules import  Form
```
- create yaml in config directory for example config/form/login.yaml
```
# config/form/login/yaml

title: Form Login
inputs:
  - id: username
    label: Username
    type: text
    placeholder: type your username 
  - id: password
    type: password
    label: Password
    placehoder: type your password 
buttons:
  - id: login_clasic
    caption: Login
    enabled: True
  - id: login_google_oauth
    caption: Login with google 
    enabled: True
```
- in startup method
```
    def startup(self):
        ...
        ...
        self.main_box = toga.Box(style=Pack(direction=COLUMN))
        self.main_window.content = self.main_box
        self.main_window.show()
        self.form_open()
```

- create method form open
  - Menu in main box (main window)
    
  ```
    def form_open(self):
      self.form = Form(self,self.main_box)
      # set default value for username
      self.form.generate('form/login',{'username':'titounnes'})
      
      # Or without defaul value
      # set default value for username
      self.form.generate('form/login')
      
  ```
        
  - Menu in new window
    
  ```
    def form_open(self):
      self.form = Form(self)
      # set default value for username
      self.form.generate('form/login',{'username':'titounnes'})
      
      # Or without defaul value
      # set default value for username
      self.form.generate('form/login')
      
  ```

## Tutorial
  Playlist video tutorial can accessed in [Playlist](https://www.youtube.com/playlist?list=PLB5fg4ce35kM_U2z-0Lj7XFuwt-_7IFwW) 
