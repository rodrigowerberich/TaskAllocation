from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Color
from display_object import DisplayObject
from kivy.uix.boxlayout import BoxLayout


Builder.load_string('''
<RobotRepresentationExtraInfo>:
    RelativeLayout:
        Label:
            id: robot_type_desc_label
            size_hint: 0.65,0.12
            pos: 0, self.parent.height-self.height
            text:'Robot Type:'
        Label:
            id: robot_type_label
            size_hint: 0.35,0.12
            pos: root.ids.robot_type_desc_label.pos[0]+root.ids.robot_type_desc_label.width, self.parent.height-self.height
            text: root.robot_type
''')

class RobotRepresentationExtraInfo(BoxLayout):
    robot_type = StringProperty('')

class RobotRepresentation(DisplayObject):
    robot = ObjectProperty(None)
    default_width = 40
    default_height = 40
    def __init__(self, robot, **kwargs):
        super(RobotRepresentation, self).__init__('Robot', **kwargs)
        self.size = self.default_width, self.default_height
        with self.canvas.before:
            Color(0,1,0)
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.label = Label(pos=self.pos, text=str(robot), size=self.size, color=(0,0,0,1))
        self.robot = robot
        self.add_widget(self.label)
        self.bind(pos=self._update_position, robot=self.on_robot)
        self.display_info_widget = RobotRepresentationExtraInfo(robot_type=robot.type)

    def _update_position(self, instance, value):
        self.label.pos = instance.pos
        self.rect.pos = instance.pos
        self.robot.position = self.calculate_local_position(self.parent.center, self.parent.size, self.parent.axis_max_value)
        self.local_pos = self.robot.position

    def on_robot(self, instance, value):
        self.label.text = str(value)
        self.name = value.name
        if self.display_info_widget is not None:
            self.display_info_widget.robot_type = value.type
        if self.parent is not None:
            self.move_local(value.position, self.parent.center, self.parent.size, self.parent.axis_max_value)
        
        