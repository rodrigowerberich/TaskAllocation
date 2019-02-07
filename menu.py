from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from create_robot_popup import CreateRobotPopup

class Menu(BoxLayout):
    display = ObjectProperty(None)
    def __init__(self, display, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.display = display
        self.add_task_button = Button(text='Add Task')
        self.add_task_button.bind(on_press=self.add_task_button_callback)
        self.add_robot_button = Button(text='Add Robot')
        self.add_robot_button.bind(on_press=self.add_robot_button_callback)
        self.edit_robot_button = Button(text='Edit Robot')
        self.edit_robot_button.bind(on_press=self.edit_robot_button_callback)
        self.axis_resolution_layout = BoxLayout()
        self.axis_max_value_layout = BoxLayout()
        self.add_widget(self.add_task_button)
        self.add_widget(self.add_robot_button)
        self.add_widget(self.edit_robot_button)
        self.add_widget(self.axis_resolution_layout)
        self.add_widget(self.axis_max_value_layout)

        self.axis_resolution_label = Label(text='Axis\nresolution')
        self.axis_resolution_value = TextInput(text = str(self.display.axis_resolution), multiline=False)
        self.axis_resolution_value.bind(focus=self.axis_resolution_on_focus)
        self.axis_resolution_layout.add_widget(self.axis_resolution_label)
        self.axis_resolution_layout.add_widget(self.axis_resolution_value)

        self.axis_max_value_label = Label(text='Axis\nmax\nvalue')
        self.axis_max_value_value = TextInput(text = str(self.display.axis_max_value), multiline=False)
        self.axis_max_value_value.bind(focus=self.axis_max_value_on_focus)
        self.axis_max_value_layout.add_widget(self.axis_max_value_label)
        self.axis_max_value_layout.add_widget(self.axis_max_value_value)

    def axis_resolution_on_focus(self, instance, value):
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