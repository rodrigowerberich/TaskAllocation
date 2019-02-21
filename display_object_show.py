from display_object import DisplayObject
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_string('''
<DisplayObjectShow>:
    orientation: 'vertical'
    pos_label: pos_label
    type_label: type_label
    name_label: name_label
    box_layout: rest_layout
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (1, 1, 1, 1)
        Line:
            points: [0, self.height, self.width, self.height]
    Label:
        id: title_label
        canvas.before:
            Color:
                rgba: (1, 1, 1, 1)
            Line:
                points: [0, root.height-self.height, root.width, root.height-self.height]
        text: 'Object details'
        pos: 0, root.height-self.height
        size_hint: 1, 0.1
    Label: 
        id: name_label_title
        text: 'Name:'
        halign: 'left'
        pos: 0, root.ids.title_label.pos[1]-self.height
        size_hint: 0.41, 0.1
    Label:
        id: name_label
        text: str(root.display_object.name)
        halign: 'left'
        pos:  root.ids.name_label_title.pos[0]+root.ids.name_label_title.width,  root.ids.title_label.pos[1]-self.height
        size_hint: 0.59, 0.1
    Label: 
        id: type_label_title
        text: 'Type:'
        halign: 'left'
        pos: 0, root.ids.name_label_title.pos[1]-self.height
        size_hint: 0.31, 0.1
    Label:
        id: type_label
        text: str(root.display_object.obj_type)
        halign: 'left'
        pos:  root.ids.type_label_title.pos[0]+root.ids.type_label_title.width,  root.ids.name_label_title.pos[1]-self.height
        size_hint: 0.69, 0.1
    Label: 
        id: pos_label_title
        text: 'Pos:'
        halign: 'left'
        pos: 0, root.ids.type_label_title.pos[1]-self.height
        size_hint: 0.31, 0.1
    Label:
        id: pos_label
        text: str(root.display_object.local_pos)
        halign: 'left'
        pos:  root.ids.pos_label_title.pos[0]+root.ids.pos_label_title.width,  root.ids.type_label_title.pos[1]-self.height
        size_hint: 0.69, 0.1
    BoxLayout:
        id: rest_layout
        pos: 0, root.ids.pos_label_title.pos[1]-self.height
        size_hint: 1, 0.7
''')

class DisplayObjectShow(RelativeLayout):
    dummy = DisplayObject('Unselected', local_pos = (0,0), default_size=(0,0), name='Unselected', z_pos=-1)
    display_object = ObjectProperty(dummy)
    old_display_object = None
    pos_label = ObjectProperty(None)
    name_label = ObjectProperty(None)
    type_label = ObjectProperty(None)
    box_layout = ObjectProperty(None)
    
    def on_display_object(self, instance, value):
        local_pos = value.local_pos
        local_pos = list(map(lambda x: round(x,2), local_pos))
        self.pos_label.text = str(local_pos)
        self.type_label.text = str(value.obj_type)
        self.name_label.text = str(value.name)
        if self.old_display_object is not None:
            self.old_display_object.unbind(local_pos=self.location_update, name=self.name_update)
            if self.old_display_object.display_info_widget is not None:
                self.box_layout.remove_widget(self.old_display_object.display_info_widget)
        value.bind(local_pos=self.location_update, name=self.name_update)
        self.old_display_object = value
        if self.display_object.display_info_widget is not None:
            self.box_layout.add_widget(self.display_object.display_info_widget)
        

    def location_update(self, instance, value):
        local_pos = value
        local_pos = list(map(lambda x: round(x,2), local_pos))
        self.pos_label.text = str(local_pos)

    def name_update(self, instance, value):
        self.name_label.text = str(value)