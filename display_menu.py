from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty
from rv import RV

Builder.load_string('''
<DisplayMenu>:
    rv: rv
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
''')

class DisplayMenu(BoxLayout):
    rv = ObjectProperty(None)
    object_menu_selected = StringProperty('')
    def __init__(self, **kwargs):
        super(DisplayMenu, self).__init__(**kwargs)

    def display_objects_changed(self, instance, value):
        self.rv.data.append({'text':str(value[-1].obj_type)+':'+str(value[-1].name), 'display_object':value[-1]})

    def on_object_selected(self, instance, value):
        self.rv.select_view(str(value.obj_type)+':'+str(value.name))

    def on_is_object_selected(self, instance, value):
        if value is False:
            self.rv.deselect_view()

    def on_rv(self, instance, value):
        value.bind(selected_value=self.selection_happened)
    
    def selection_happened(self, instance, value):
        self.object_menu_selected =  value