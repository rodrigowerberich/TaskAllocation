from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from rv import RV
from display_object_show import DisplayObjectShow

Builder.load_string('''
<DisplayMenu>:
    rv: rv
    display_object_show: display_object_show
    orientation: 'vertical'
    canvas:
        Line:
            points: [self.center_x-self.width/2, self.center_y-self.height/2, self.center_x-self.width/2, self.center_y+self.height/2]
    Label:
        canvas:
            Line:
                points: [self.center_x-self.width/2, self.center_y-self.height/2, self.center_x+self.width/2, self.center_y-self.height/2]
        text: 'Object selection'
        size_hint: 1, 0.05
    RV:
        id: rv
    DisplayObjectShow:
        id: display_object_show
''')

class DisplayMenu(BoxLayout):
    rv = ObjectProperty(None)
    object_menu_selected = ObjectProperty(None)
    display_object_show = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(DisplayMenu, self).__init__(**kwargs)

    def display_objects_changed(self, instance, value):
        print('value 1', value[-1], value)
        self.rv.data.append({'text':str(value[-1].obj_type)+':'+str(value[-1].name), 'display_object':value[-1]})
        print(self.rv.data)

    def on_object_selected(self, instance, value):
        print('value 2', value)
        self.rv.select_view(str(value.obj_type)+':'+str(value.name))
        if value.obj_type != 'Dummy':
            self.display_object_show.display_object = value

    def on_is_object_selected(self, instance, value):
        print('value 3', value)
        if value is False:
            self.rv.deselect_view()
            self.display_object_show.display_object = self.display_object_show.dummy

    def on_rv(self, instance, value):
        print('value 4', value)
        value.bind(selected_value=self.selection_happened)
    
    def selection_happened(self, instance, value):
        print('value 5', value)
        self.object_menu_selected =  value
        self.display_object_show.display_object = value