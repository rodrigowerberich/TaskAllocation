from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty, ListProperty, NumericProperty
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color, Ellipse
from display_object import DisplayObject
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
<MuTaskRepresentationExtraInfo>:
    GridLayout:
        cols: 2
        row_force_default:True 
        row_default_height:40
        Label:
            size_hint: 0.65,0.12
            text:'Task:'
        Label:
            id: task_name_label
            size_hint: 0.35,0.12
            text: root.task_name
        Label:
            size_hint: 0.65,0.12
            text:'Micro Task:'
        Label:
            id: mu_task_name_label
            size_hint: 0.35,0.12
            text: root.mu_task_name
        Label:
            size_hint: 0.65,0.12
            text:'Previous:'
        ScrollView:
            size_hint: 0.35, 0.12
            do_scroll_x: True
            GridLayout:
                cols:1
                size_hint_x:None
                height: self.minimum_height
                Label:
                    id: previous_label
                    size: self.texture_size
                    text: str(root.previous)
        Label:
            size_hint: 0.65,0.12
            text:'Priority:'
        Label:
            id: priority_label
            size_hint: 0.35,0.12
            text: str(root.priority)
<MuTaskRepresentation>:
    size: self.default_width, self.default_height
    Label:
        text: 'T'+root.task.name
        size: root.width, root.height
        pos: root.pos[0], root.pos[1]+root.height/4
        font_size: 12
    Label:
        text: 'Mu'+root.mu_task.name
        size: root.width, root.height
        pos: root.pos[0], root.pos[1]-root.height/4
        font_size: 12
''')

class MuTaskRepresentationExtraInfo(BoxLayout):
    task_name = StringProperty('')
    mu_task_name = StringProperty('')
    previous = ListProperty([])
    priority = NumericProperty(0)

class MuTaskRepresentation(DisplayObject):
    task = ObjectProperty()
    mu_task = ObjectProperty(None)
    default_width = 40
    default_height = 40
    def __init__(self, **kwargs):
        super(MuTaskRepresentation, self).__init__('MuTask', **kwargs)
        with self.canvas.before:
            Color(0,0,1)
            self.circle = Ellipse(pos=self.pos, size=self.size)
        self.bind(pos=self._update_position)
        self.display_info_widget = MuTaskRepresentationExtraInfo(
            task_name=self.task.name, 
            mu_task_name=self.mu_task.name, 
            previous=[mu_task.name for mu_task in self.mu_task.previous] if self.mu_task.previous is not None else [],
            priority=self.task.priority)

    def _update_position(self, instance, value):
        self.circle.pos = instance.pos
        self.mu_task.position = self.calculate_local_position(self.parent.center, self.parent.size, self.parent.axis_max_value)
        self.local_pos = self.mu_task.position