import toga, os, math
from toga.style import Pack
from toga.style.pack import ROW, COLUMN, CENTER

from ..fileSystem.yaml import Yaml
from ..fileSystem.file import File
from ..view.form import Form

class DataTable(object):
    def __init__(self, app, container):
        self.container = container
        self.app = app
        self.path_datatable = os.path.dirname(self.app.config[0])+self.app.config[1] 

    def generate(self, datatable_config, data=[], page=1, per_page=20):
        if type(datatable_config)==str :
            config = Yaml().load(self.path_datatable+'/'+datatable_config+'.yaml')
        else:
            config = datatable_config

        children = self.container.children
        length = len(children) 
        for i in range(length):
            self.container.remove(children[length-1-i]) 

        if config.get('title'):
            title = toga.Label(config['title'], style=Pack(text_align=CENTER))
            self.container.add(title)    

        if  config.get('form'):
            box_form = toga.Box(style=Pack(direction=COLUMN, alignment=CENTER))
            self.container.add(box_form)
            Form(self.app, box_form).generate(config['form'])

        scroll = toga.ScrollContainer(vertical=True, horizontal=True, style = Pack( padding=(10, 30, 10, 30), height=per_page*40 ))
        table = toga.Table(config.get('header'), missing_value="")
        scroll.content = table
        self.container.add(scroll)

        table.data = []
        total = math.ceil(len(data)/per_page) 
        data = sorted(data, key=lambda x: x[1], reverse=False)
        if total > 1:
            tmp = []
            for i in range(per_page):
                if (page-1)*per_page+i < len(data):
                    tmp.append(data[(page-1)*per_page+i])
                else: 
                    break

            table.data = tmp

            box_nav = toga.Box(style=Pack(direction=ROW, alignment=CENTER, height=60) )
            self.container.add(box_nav)
            form = Form(self.app, box_nav).generate({
                'buttons' : [
                    {
                        'id' : 'nav:'+config['paginate']+':first',
                        'caption' : '<< First',
                        'enabled' : page > 1,
                    },
                    {
                        'id' : 'nav:'+config['paginate']+':back',
                        'caption' : '< Back',
                        'enabled' : page > 1,
                    },
                    {
                        'id' : 'nav:'+config['paginate']+':next',
                        'caption' : 'Next >',
                        'enabled' : page < total,
                    },
                    {
                        'id' : 'nav:'+config['paginate']+':last',
                        'caption' : 'Last >>',
                        'enabled' : page < total,
                    }
                ]
            })
        else:
            table.data = data

    
