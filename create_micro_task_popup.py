from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, DictProperty, ReferenceListProperty, ListProperty
from load_file_dialog import LoadDialog
from task_domain_parser import TaskDomainParser
from kivy.uix.dropdown import DropDown
import copy
import os
import json

Builder.load_string('''#:import Button kivy.uix.button.Button
<CreateMicroTaskPopup>:
    task_type_dropdown_button: task_type_dropdown_button
    previous_task_dropdown_button: previous_task_dropdown_button
    BoxLayout:
        RelativeLayout:
            Label:
                id: name_label
                size_hint: 0.35,0.12
                pos: 0, self.parent.height-self.height
                text:'Name:'
            TextInput:
                id: name_text_input
                size_hint: 0.65,0.12
                pos: root.ids.name_label.pos[0]+root.ids.name_label.width, root.ids.name_label.pos[1]
                text: root.name
                multiline: False
                on_focus: root.name_on_focus(*args)
            Label: 
                id: task_type_label
                size_hint: 0.35,0.12
                pos: 0, root.ids.name_text_input.pos[1]-self.height
                text:'Task type:'
            Button:
                id: task_type_dropdown_button
                size_hint: 0.65,0.12
                pos: root.ids.task_type_label.pos[0]+root.ids.task_type_label.width, root.ids.name_text_input.pos[1]-self.height
                text : root.task_types[0] if len(root.task_types) > 0 else 'Empty dropdown'
                on_release: root.robot_types_dropdown.open(self)
                on_text: root.task_type = args[1]
            #     multiline: False
            #     on_focus: root.priority_on_focus(*args)
            Label: 
                id: x_position_label
                size_hint: 0.25,0.12
                pos: 0, root.ids.task_type_label.pos[1]-self.height
                text:'X Pos:'
            TextInput:
                id: x_position_text_input
                size_hint: 0.25,0.12
                pos: root.ids.x_position_label.pos[0]+root.ids.x_position_label.width, root.ids.x_position_label.pos[1]
                text : str(root.x_pos)
                multiline: False
                on_focus: root.x_pos_on_focus(*args)
            Label: 
                id: y_position_label
                size_hint: 0.25,0.12
                pos: root.ids.x_position_text_input.pos[0]+root.ids.x_position_text_input.width, root.ids.task_type_label.pos[1]-self.height
                text:'Y Pos:'
            TextInput:
                id: y_position_text_input
                size_hint: 0.25,0.12
                pos: root.ids.y_position_label.pos[0]+root.ids.y_position_label.width, root.ids.y_position_label.pos[1]
                text : str(root.y_pos)
                multiline: False
                on_focus: root.y_pos_on_focus(*args)
            Label:
                canvas:
                    Line:
                        points: [*self.pos, self.pos[0]+self.width, self.pos[1]]
                id: previous_tasks_label
                size_hint: 1 ,0.10
                pos: 0, root.ids.y_position_label.pos[1]-self.height
                text:'Previous tasks:'
            ScrollView:
                id: previous_scroll_view
                pos: 0, root.ids.previous_tasks_label.pos[1]-self.height
                size_hint: 1, 0.30
                do_scroll_y: True
                GridLayout:
                    id: previous_tasks_grid_layout
                    cols:1
                    spacing:2
                    size_hint_y:None
                    height: self.minimum_height
            Button:
                id: previous_task_dropdown_button
                text:'Add previous task' if len(root.previous_micro_tasks) > 0 else 'No previous task to select from'
                size_hint: 1, 0.12
                pos: 0, root.ids.previous_scroll_view.pos[1]-self.height
                on_release: root.previous_tasks_dropdown.open(self) 
            Button:
                size_hint: 0.35,0.12
                pos: 0, 0
                text: 'Cancel'
                on_press: root.dismiss()
            Button:
                size_hint: 0.35,0.12
                pos: self.parent.width-self.width, 0
                text: 'Done'
                on_press: root.creation_complete()
''')

class CreateMicroTaskPopup(Popup):
    task_type_dropdown_button = ObjectProperty(None)
    previous_task_dropdown_button = ObjectProperty(None)
    name = StringProperty('1')
    task_type = StringProperty('')
    task_types = ListProperty([])
    x_pos = NumericProperty(0)
    y_pos = NumericProperty(0)
    position = ReferenceListProperty(x_pos, y_pos)
    previous_micro_tasks = ListProperty([])
    robot_types_dropdown = ObjectProperty(DropDown())
    previous_tasks_dropdown = ObjectProperty(DropDown())
    done = ObjectProperty(None)
    cancel = ObjectProperty(None)

    def __init__(self, name='', task_type='', editing=False, previous_micro_tasks_selected=[] , task_types=['a1', 'a2', 'a3'] ,previous_micro_tasks=['m1','m2','m3'], **kwargs):
        super(CreateMicroTaskPopup, self).__init__(**kwargs)
        self.task_types=task_types
        self.robot_types_dropdown.clear_widgets()
        if task_type == '':
            self.task_type = task_types[0]
        else:
            self.task_type = task_type
        self.task_type_dropdown_button.text = self.task_type
        for t_type in self.task_types:
            btn = Button(text=t_type, size_hint_y=None, height=40)
            btn.bind(on_release=lambda btn: self.robot_types_dropdown.select(btn.text))
            self.robot_types_dropdown.add_widget(btn)
        self.robot_types_dropdown.bind(on_select=lambda instance, x: setattr(self.task_type_dropdown_button, 'text', x))
        self.previous_micro_tasks = previous_micro_tasks
        self.previous_tasks_dropdown.bind(on_select=self.add_previous_task)
        self.previous_micro_tasks_selected = previous_micro_tasks_selected
        self.ids.previous_tasks_grid_layout.clear_widgets()
        for element in self.previous_micro_tasks_selected:
            btn = Button(text=element,
                     size_hint_y=None, 
                     height=20, 
                     background_color=(.5,.5,.5,.3),
                     on_release=self.remove_previous_task)
            self.ids.previous_tasks_grid_layout.add_widget(btn)
            self.previous_micro_tasks = list(filter(lambda x: x is not element, self.previous_micro_tasks))
        self.editing = editing
        self.name=name
        if self.editing:
            self.old_name=name

    def add_previous_task(self, instance, value):
        btn = Button(text=value,
                     size_hint_y=None, 
                     height=20, 
                     background_color=(.5,.5,.5,.3),
                     on_release=self.remove_previous_task)
        self.ids.previous_tasks_grid_layout.add_widget(btn)
        self.previous_micro_tasks_selected.append(value)
        self.previous_micro_tasks = list(filter(lambda x: x is not value, self.previous_micro_tasks))

    def remove_previous_task(self, instance):
        self.ids.previous_tasks_grid_layout.remove_widget(instance)
        self.previous_micro_tasks_selected = list(filter(lambda x: x is not instance.text, self.previous_micro_tasks_selected))
        self.previous_micro_tasks.append(instance.text)

    def name_on_focus(self, instance, value):
        if len(instance.text) > 2:
            instance.text = instance.text[0:2]
        self.name = instance.text

    def x_pos_on_focus(self, instance, value):
        if not value:
            try:
                self.x_pos = float(instance.text)
            except ValueError:
                instance.text = str(self.x_pos)

    def y_pos_on_focus(self, instance, value):
        if not value:
            try:
                self.y_pos = float(instance.text)
            except ValueError:
                instance.text = str(self.y_pos)

    def creation_complete(self):
        if self.done is not None:
            if self.editing:
                self.done(self.name, self.old_name, self.task_type, self.position, self.previous_micro_tasks_selected)
            else:
                self.done(self.name, self.task_type, self.position, self.previous_micro_tasks_selected)
        self.dismiss()

    def on_previous_micro_tasks(self, instance, previous_micro_tasks):
        self.previous_tasks_dropdown.clear_widgets()
        for previous_task in previous_micro_tasks:
            btn = Button(text=previous_task, size_hint_y=None, height=20)
            btn.bind(on_release=lambda btn: self.previous_tasks_dropdown.select(btn.text))
            self.previous_tasks_dropdown.add_widget(btn)
        if len(previous_micro_tasks) is 0:
            self.previous_task_dropdown_button.text = 'No previous task to select from'
        else:
            self.previous_task_dropdown_button.text = 'Add previous task'