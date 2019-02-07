from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from robot import Robot, RobotType
from copy import deepcopy


class CreateRobotPopup(Popup):
    def __init__(self, display, robot_representation=None, **kwargs):
        super(CreateRobotPopup, self).__init__(**kwargs)
        if robot_representation is None:
            self.robot = None
            self.is_editing = False
        else:
            self.robot_representation = robot_representation
            self.robot = deepcopy(robot_representation.robot)
            self.is_editing = True            
        
        self.display = display

        if not self.is_editing:
            suggestion_name_value = 1
            while any([str(suggestion_name_value) == robot.name for robot in self.display.objects if robot.obj_type is 'Robot']):
                suggestion_name_value += 1
            self.robot = Robot(str(suggestion_name_value), RobotType.a1, (0, 0))
        
        self.name_label = Label(text='Robot name:')
        self.name_input = TextInput(text=self.robot.name, multiline=False)
        self.name_input.bind(focus=self.name_label_on_focus)
        
        self.name_layout = BoxLayout()
        self.name_layout.add_widget(self.name_label)
        self.name_layout.add_widget(self.name_input)

        self.robot_position_label = Label(text="Robot's position (x,y):")
        
        self.robot_position_input_x = TextInput(text=str(round(self.robot.position[0],3)), multiline=False, size_hint=(0.2,1))
        self.robot_position_input_x.bind(focus=self.robot_position_input_x_on_focus)

        self.robot_position_input_y = TextInput(text=str(round(self.robot.position[1],3)), multiline=False, size_hint=(0.2,1))
        self.robot_position_input_y.bind(focus=self.robot_position_input_y_on_focus)
        self.robot_position_layout = BoxLayout()
        self.robot_position_layout.add_widget(self.robot_position_label)
        self.robot_position_layout.add_widget(self.robot_position_input_x)
        self.robot_position_layout.add_widget(self.robot_position_input_y)
        
        self.close_button = Button(text='Close')
        self.close_button.bind(on_press=self.popup_close_button_callback)
        if self.is_editing:
            self.create_button = Button(text='Edit')
        else:
            self.create_button = Button(text='Create')
        self.create_button.bind(on_press=self.popup_create_button_callback)
        self.end_layout = BoxLayout()
        self.end_layout.add_widget(self.close_button)
        self.end_layout.add_widget(self.create_button)

        self.box_layout = BoxLayout(orientation='vertical')
        self.box_layout.add_widget(self.name_layout)
        self.box_layout.add_widget(self.robot_position_layout)
        self.box_layout.add_widget(self.end_layout)

        self.content = self.box_layout

    def popup_close_button_callback(self, instance):
        self.dismiss()

    def popup_create_button_callback(self, instance):
        if self.is_editing:
            self.robot_representation.robot = self.robot
        else:
            self.display.add_robot(self.robot)
        self.dismiss()
    
    def name_label_on_focus(self, instance, value):
        if not value:
            if len(instance.text) > 2:
                instance.text = instance.text[0:2]
            self.robot.name = instance.text

    def robot_position_input_x_on_focus(self, instance, value):
        try:
            new_x_value = float(instance.text)
            if abs(new_x_value) <= abs(self.display.axis_max_value):
                self.robot.position = new_x_value, self.robot.position[1]
            else:
                instance.text = str(self.robot.position[0])
        except ValueError:
            instance.text = str(self.robot.position[0])
            
    def robot_position_input_y_on_focus(self, instance, value):
        try:
            new_y_value = float(instance.text)
            if abs(new_y_value) <= abs(self.display.axis_max_value):
                self.robot.position = self.robot.position[0], new_y_value
            else:
                instance.text = str(self.robot.position[1])
        except ValueError:
            instance.text = str(self.robot.position[1])