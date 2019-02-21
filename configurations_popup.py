from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, DictProperty
from load_file_dialog import LoadDialog
from task_domain_parser import TaskDomainParser, TaskProblemParser
import copy
import os
import json

Builder.load_string('''
<ConfigurationsPopup>:
    load_error_label: choose_task_domain_file_error_label
    BoxLayout:
        RelativeLayout:
            Label:
                id: axis_resolution_label
                size_hint: 0.35,0.12
                pos: 0, self.parent.height-self.height
                text:'Axis resolution:'
            TextInput:
                id: axis_resolution_text_input
                size_hint: 0.15,0.12
                pos: root.ids.axis_resolution_label.pos[0]+root.ids.axis_resolution_label.width, root.ids.axis_resolution_label.pos[1]
                text : str(root.axis_resolution)
                multiline: False
                on_focus: root.axis_resolution_on_focus(*args)
            Label: 
                id: axis_max_value_label
                size_hint: 0.35,0.12
                pos: root.ids.axis_resolution_text_input.pos[0]+root.ids.axis_resolution_text_input.width, root.ids.axis_resolution_text_input.pos[1]
                text:'Axis max value:'
            TextInput:
                id: axis_max_value_text_input
                size_hint: 0.15,0.12
                pos: root.ids.axis_max_value_label.pos[0]+root.ids.axis_max_value_label.width, root.ids.axis_max_value_label.pos[1]
                text : str(root.axis_max_value)
                multiline: False
                on_focus: root.axis_max_value_on_focus(*args)
            Label:
                id: choose_task_domain_file_label
                size_hint: 0.35,0.12
                pos: 0, self.parent.height-root.ids.axis_resolution_label.height-self.height
                text: 'Task domain file:'
            TextInput:
                id: choose_task_domain_file_text_input
                size_hint: 0.50,0.12
                pos: root.ids.choose_task_domain_file_label.pos[0]+root.ids.choose_task_domain_file_label.width, root.ids.choose_task_domain_file_label.pos[1]
                text : root.task_domain_file_name
                multiline: False
            Button:
                id: choose_task_domain_file_button
                size_hint: 0.15,0.12
                pos: root.ids.choose_task_domain_file_text_input.pos[0]+root.ids.choose_task_domain_file_text_input.width, root.ids.choose_task_domain_file_text_input.pos[1]
                text : 'Open...'
                on_release: root.show_load_domain_file()
            Label:
                id: choose_task_domain_file_error_label
                size_hint: 1,0
                pos: 0, self.parent.height-root.ids.axis_resolution_label.height-root.ids.choose_task_domain_file_label.height-self.height
                color: 1,0,0,1
                text: ''
            Label:
                id: save_problem_file_label
                size_hint: 0.17,0.12
                pos: 0, root.ids.choose_task_domain_file_error_label.pos[1]-self.height
                text: 'Problem:'
            TextInput:
                id: save_problem_file_text_input
                size_hint: 0.42,0.12
                pos: root.ids.save_problem_file_label.width, root.ids.choose_task_domain_file_error_label.pos[1]-self.height
                text : root.save_problem_file_name
                multiline: False
                on_text: root.save_problem_file_name = args[1]
            Button:
                id: choose_save_problem_file_button
                size_hint: 0.15,0.12
                pos: root.ids.save_problem_file_text_input.pos[0]+root.ids.save_problem_file_text_input.width, root.ids.choose_task_domain_file_error_label.pos[1]-self.height
                text : 'Choose'
                on_release: root.show_choose_save_problem_file()
            Button:
                id: save_problem_button
                size_hint: 0.13,0.12
                pos: root.ids.choose_save_problem_file_button.pos[0]+root.ids.choose_save_problem_file_button.width, root.ids.choose_task_domain_file_error_label.pos[1]-self.height
                text : 'Save'
                on_release: root.save_problem_file()
            Button:
                id: load_problem_button
                size_hint: 0.13,0.12
                pos: root.ids.save_problem_button.pos[0]+root.ids.save_problem_button.width, root.ids.choose_task_domain_file_error_label.pos[1]-self.height
                text : 'Load'
                on_release: root.load_problem_file()
            Label:
                id: problem_file_error_label
                size_hint: 1,0
                pos: 0, save_problem_file_label.pos[1]-self.height
                color: 1,0,0,1
                text: ''
            Button:
                size_hint: 0.35,0.12
                pos: self.parent.width-self.width, 0
                text: 'Done'
                on_press: root.dismiss()
''')

class ConfigurationsPopup(Popup):
    axis_resolution = NumericProperty(10)
    axis_max_value = NumericProperty(10)
    task_domain_file_name = StringProperty('...')
    save_problem_file_name = StringProperty('...')
    load_error_label = ObjectProperty(None)
    file_loaded = DictProperty(None)
    def __init__(self, display, **kwargs):
        super(ConfigurationsPopup, self).__init__(**kwargs)
        self.display = display
        self.axis_resolution = self.display.axis_resolution 
        self.axis_max_value = self.display.axis_max_value
        
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

    def show_load_domain_file(self):
        content = LoadDialog(load=self.load_domain_file, cancel=self.dismiss_popup_domain_file)
        self._popup_domain_file = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
        self._popup_domain_file.open()

    def show_choose_save_problem_file(self):
        content = LoadDialog(load=self.choose_problem_file, cancel=self.dismiss_popup_problem_file)
        self._popup_problem_file = Popup(title="Choose problem file", content=content)
        self._popup_problem_file.open()

    def load_domain_file(self, path, filename):
        if(len(filename) > 0):
            self.task_domain_file_name = os.path.join(path, filename[0])
            self.ids.choose_task_domain_file_text_input.do_cursor_movement('cursor_end')
            try:
                parsed_file = TaskDomainParser.parse(os.path.join(path, filename[0]))
                self.load_error_label.size_hint = 1, 0
                self.load_error_label.text = ''
                self.file_loaded = parsed_file
            except json.decoder.JSONDecodeError as identifier:
                self.load_error_label.size_hint = 1, 0.12
                self.load_error_label.text = 'File must be a JSON file'
            except Exception as identifier:
                self.load_error_label.size_hint = 1, 0.12
                self.load_error_label.text = str(identifier)
        self.dismiss_popup_domain_file()

    def choose_problem_file(self, path, filename):
        if(len(filename) > 0):
            self.save_problem_file_name = os.path.join(path, filename[0])
            self.ids.save_problem_file_text_input.do_cursor_movement('cursor_end')
        self.dismiss_popup_problem_file()

    def dismiss_popup_domain_file(self):
        self._popup_domain_file.dismiss()

    def dismiss_popup_problem_file(self):
        self._popup_problem_file.dismiss()

    def save_problem_file(self):
        if self.save_problem_file_name.endswith('.json'):
            self.ids.problem_file_error_label.size_hint_y = 0
            self.ids.problem_file_error_label.text=''
            TaskProblemParser.save_problem(self.save_problem_file_name, self.display.robots, self.display.tasks, self.display.mu_tasks)
        else:
            self.ids.problem_file_error_label.text = 'File must end with .json'
            self.ids.problem_file_error_label.size_hint_y = 0.12
            

    def load_problem_file(self):
        if self.save_problem_file_name.endswith('.json'):
            self.ids.problem_file_error_label.size_hint_y = 0
            self.ids.problem_file_error_label.text=''
            try:
                robots, mu_tasks, tasks = TaskProblemParser.load(self.save_problem_file_name)
                self.display.clear_display()
                for robot in robots:
                    self.display.add_robot(robot)
                for task in tasks:
                    self.display.add_task(task)
            except Exception as exception:
                self.ids.problem_file_error_label.text = str(exception)
                self.ids.problem_file_error_label.size_hint_y = 0.12        
        else:
            self.ids.problem_file_error_label.text = 'File must end with .json'
            self.ids.problem_file_error_label.size_hint_y = 0.12
            