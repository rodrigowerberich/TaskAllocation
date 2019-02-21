from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, DictProperty
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from create_robot_popup import CreateRobotPopup
from configurations_popup import ConfigurationsPopup
from create_task_popup import CreateTaskPopup
from kivy.uix.popup import Popup
from task_domain_parser import TaskDomainParser
from task import Task

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
    Button:
        text:'Configurations'
        on_press: root.open_configurations_button_callback(*args)
''')

class Menu(BoxLayout):
    axis_resolution = NumericProperty(10)
    axis_max_value = NumericProperty(10)
    file_loaded = DictProperty({})
    def __init__(self, display=None, **kwargs):
        super(Menu, self).__init__(**kwargs)
        self.display = display
        self.configuration_popup = None
        try:
            self.file_loaded = TaskDomainParser.parse('tasks_definitions.json')
        except Exception:
            pass                

    def add_task_button_callback(self, instance):
        popup = CreateTaskPopup(title='Create task popup', 
                                auto_dismiss=False, 
                                size_hint=(0.5, 0.5),
                                task_types=self.file_loaded['task_types'],
                                unavailable_names=[task.name for task in self.display.tasks],
                                mu_tasks_unavailable_names=[mu_task.name for mu_task in self.display.mu_tasks],
                                creation_done=self.add_task_popup_complete)
        popup.open()

    def add_task_popup_complete(self, name, priority, deadline, mu_tasks):
        if len(mu_tasks) > 0:
            new_task = Task(name, mu_tasks, priority, deadline)
            self.display.add_task(new_task)

    def add_robot_button_callback(self, instance):
        if self.file_loaded != {}:
            self.robot_popup = CreateRobotPopup(self.display,
                self.file_loaded['robot_types'],
                title='Create Robot',
                size_hint=(0.5, 0.5),
                auto_dismiss=False)
            self.robot_popup.open()
        else:
            box_layout = BoxLayout(orientation='vertical')
            label = Label(text='Please load the task domain file in the configurations!')
            button = Button(text='Okay')
            box_layout.add_widget(label)
            box_layout.add_widget(button)
            popup = Popup(title='Missing robot types', content=box_layout, size_hint=(0.7, 0.3))
            button.on_release = popup.dismiss
            popup.open()

    def edit_robot_button_callback(self, instance):
        if self.display.is_object_selected:
            if self.display.selected_object.obj_type == 'Robot':
                self.robot_popup = CreateRobotPopup(self.display,
                    self.file_loaded['robot_types'],
                    title='Edit Robot',
                    size_hint=(0.5, 0.5),
                    auto_dismiss=False,
                    robot_representation=self.display.selected_object)
                self.robot_popup.open()

    def open_configurations_button_callback(self, instance):
        if self.configuration_popup is None:
            self.configuration_popup = ConfigurationsPopup(self.display,
                file_loaded = self.file_loaded,
                title='Configurations',
                size_hint=(0.5, 0.5),
                auto_dismiss=False)
        self.configuration_popup.bind(file_loaded=self.on_file_loaded)
        self.configuration_popup.open()

    def on_file_loaded(self, instance, value):
        self.file_loaded = value