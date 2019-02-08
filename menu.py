from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from create_robot_popup import CreateRobotPopup

Builder.load_string('''
<Menu>:
    orientation: 'vertical'
    Button:
        text: 'Add Task'
        on_press: root.add_task_button_callback(*args)
    Button:
        text: 'Add Robot'
        on_press: root.add_robot_button_callback(*args)
    Button:
        text:'Edit Robot'
        on_press: root.edit_robot_button_callback(*args)
    BoxLayout:
        Label: 
            text:'Axis resolution'
        TextInput:
            text : str(root.axis_resolution)
            multiline: False
            on_focus: root.axis_resolution_on_focus(*args)
    BoxLayout:
        Label: 
            text:'Axis max value'
        TextInput:
            text : str(root.axis_max_value)
            multiline: False
            on_focus: root.axis_max_value_on_focus(*args)
''')

class Menu(BoxLayout):
    axis_resolution = NumericProperty(10)
    axis_max_value = NumericProperty(10)
    def __init__(self, display=None, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.display = display

    def axis_resolution_on_focus(self, instance, value):
        print(value)
        if not value:
            try:
                new_resolution = int(instance.text)
                if new_resolution > 0:
                    self.display.axis_resolution = int(instance.text)
                else:
                    instance.text = str(self.display.axis_resolution)
            except ValueError:
                instance.text = str(self.display.axis_resolution)

    def axis_max_value_on_focus(self, instance, value):
        if not value:
            try:
                new_max_value = int(instance.text)
                if new_max_value > 0:
                    self.display.axis_max_value = int(instance.text)
                else:
                    instance.text = str(self.display.axis_max_value)
            except ValueError:
                instance.text = str(self.display.axis_max_value)

    def add_task_button_callback(self, instance):
        print('The button <%s> is being pressed' % instance.text)

    def add_robot_button_callback(self, instance):
        self.robot_popup = CreateRobotPopup(self.display,
            title='Create Robot',
            size_hint=(0.5, 0.5),
            auto_dismiss=False)
        self.robot_popup.open()

    def edit_robot_button_callback(self, instance):
        if self.display.is_object_selected:
            if self.display.selected_object.obj_type == 'Robot':
                self.robot_popup = CreateRobotPopup(self.display,
                    title='Edit Robot',
                    size_hint=(0.5, 0.5),
                    auto_dismiss=False,
                    robot_representation=self.display.selected_object)
                self.robot_popup.open()