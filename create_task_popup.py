from kivy.lang import Builder
from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, NumericProperty, StringProperty, DictProperty, ListProperty
from create_micro_task_popup import CreateMicroTaskPopup
from micro_task import MuTask
from functools import reduce

Builder.load_string('''
<MuTaskSelection>:
    Label:
        size_hint_x: 0.7
        text: root.text
    Button:
        text: 'Edit'
        size_hint_x: 0.15
        on_release: root.edit_press(root) if root.edit_press is not None else None
    Button:
        text: 'X'
        background_color: 1,0,0,1
        size_hint_x: 0.15
        on_release: root.delete_press(root) if root.delete_press is not None else None
<CreateTaskPopup>:
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
                id: priority_label
                size_hint: 0.35,0.12
                pos: 0, root.ids.name_text_input.pos[1]-self.height
                text:'Priority:'
            TextInput:
                id: priority_text_input
                size_hint: 0.15,0.12
                pos: root.ids.priority_label.pos[0]+root.ids.priority_label.width, root.ids.name_text_input.pos[1]-self.height
                text : str(root.priority)
                multiline: False
                on_focus: root.priority_on_focus(*args)
            Label: 
                id: deadline_label
                size_hint: 0.35,0.12
                pos: root.ids.priority_text_input.pos[0]+root.ids.priority_text_input.width, root.ids.name_text_input.pos[1]-self.height
                text:'Deadline:'
            TextInput:
                id: deadline_text_input
                size_hint: 0.15,0.12
                pos: root.ids.deadline_label.pos[0]+root.ids.deadline_label.width, root.ids.deadline_label.pos[1]
                text : str(root.deadline)
                multiline: False
                on_focus: root.deadline_on_focus(*args)
            Label:
                canvas:
                    Line:
                        points: [*self.pos, self.pos[0]+self.width, self.pos[1]]
                id: micro_tasks_label
                size_hint: 1 ,0.10
                pos: 0, root.ids.deadline_label.pos[1]-self.height
                text:'Micro tasks:'
            ScrollView:
                id: micro_tasks_scroll_view
                pos: 0, root.ids.micro_tasks_label.pos[1]-self.height
                size_hint: 1, 0.42
                do_scroll_y: True
                GridLayout:
                    id: micro_tasks_grid_layout
                    cols:1
                    spacing:2
                    size_hint_y:None
                    height: self.minimum_height
            Button:
                text:'Add micro task'
                size_hint: 1, 0.12
                pos: 0, root.ids.micro_tasks_scroll_view.pos[1]-self.height
                on_press: root.open_micro_task_creation()
            Button:
                size_hint: 0.35,0.12
                pos: 0, 0
                text: 'Cancel'
                on_press: root.dismiss()
            Button:
                size_hint: 0.35,0.12
                pos: self.parent.width-self.width, 0
                text: 'Done'
                on_press: root.done()
''')

class MuTaskSelection(BoxLayout):
    text = StringProperty('')
    delete_press = ObjectProperty(None)
    edit_press = ObjectProperty(None)

class CreateTaskPopup(Popup):
    unavailable_names = ListProperty([])
    mu_tasks_unavailable_names = ListProperty([])
    name = StringProperty('1')
    priority = NumericProperty(0)
    deadline = NumericProperty(0)
    mu_tasks = ListProperty([])
    task_types = ListProperty([])
    creation_done = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(CreateTaskPopup, self).__init__(**kwargs)
        value = 1
        while str(value) in self.unavailable_names:
            value += 1
        self.name = str(value)

    def name_on_focus(self, instance, value):
        if not value:
            instance.text = instance.text.strip()
            if len(instance.text) > 2:
                instance.text = instance.text[0:2]
                instance.text = instance.text.strip()
            if instance.text not in self.unavailable_names:
                self.name = instance.text
            else:
                instance.text = self.name

    def priority_on_focus(self, instance, value):
        if not value:
            try:
                self.priority = float(self.ids.priority_text_input.text)
            except ValueError:
                self.ids.priority_text_input.text = str(self.priority)

    def deadline_on_focus(self, instance, value):
        if not value:
            try:
                self.deadline = float(self.ids.deadline_text_input.text)
            except ValueError:
                self.ids.deadline_text_input.text = str(self.deadline)
    
    def open_micro_task_creation(self):
        name_value = 1
        names = [mu_task.name for mu_task in self.mu_tasks]
        while str(name_value) in names or str(name_value) in self.mu_tasks_unavailable_names:
            name_value+=1
        tasks_pre_requisites = reduce(lambda x,y: x+y, [ mu_task.get_all_pre_requisites() for mu_task in self.mu_tasks], [])
        non_pre_requisites = list(filter(lambda x: x not in tasks_pre_requisites, self.mu_tasks))
        non_pre_requisites_names = [mu_task.name for mu_task in non_pre_requisites]
        popup = CreateMicroTaskPopup(title='Create micro task', 
                                    task_types=self.task_types, 
                                    name=str(name_value), 
                                    previous_micro_tasks=non_pre_requisites_names,
                                    previous_micro_tasks_selected=[],
                                    size_hint=(0.5,0.5))
        popup.done = self.add_micro_task
        popup.open()

    def add_micro_task(self, name, mu_task_type, position, micro_tasks_previous_names):
        micro_tasks_previous = [mu_task for mu_task in self.mu_tasks if mu_task.name in micro_tasks_previous_names]
        if micro_tasks_previous == []:
            micro_tasks_previous = None
        new_mu_task = MuTask(name, mu_task_type, position, previous=micro_tasks_previous)
        mu_task_name = [mu_task.name for mu_task in self.mu_tasks if mu_task.name == new_mu_task.name]
        if len(mu_task_name) is 0 and new_mu_task.name not in self.mu_tasks_unavailable_names:
            self.mu_tasks.append(new_mu_task)
            self.ids.micro_tasks_grid_layout.add_widget(MuTaskSelection(text=name, size_hint_y=None, height=20, delete_press=self.remove_micro_task, edit_press=self.edit_micro_task))

    def edit_micro_task_done(self, name, old_name, mu_task_type, position, micro_tasks_previous_names):
        found_mu_task = [ mu_task for mu_task in self.mu_tasks if old_name == mu_task.name]
        if old_name != name:
            not_conflicting_name = len([ mu_task for mu_task in self.mu_tasks if name == mu_task.name]) == 0
        else:
            not_conflicting_name = len([ mu_task for mu_task in self.mu_tasks if name == mu_task.name]) == 1
        if len(found_mu_task) == 1 and not_conflicting_name and name not in self.mu_tasks_unavailable_names:
            self.mu_tasks.remove(found_mu_task[0])
            micro_tasks_previous = [mu_task for mu_task in self.mu_tasks if mu_task.name in micro_tasks_previous_names]
            if micro_tasks_previous == []:
                micro_tasks_previous = None
            new_mu_task = MuTask(name, mu_task_type, position, previous=micro_tasks_previous)
            for mu_task in self.mu_tasks:
                if mu_task.previous is not None:
                    before = len(mu_task.previous)
                    mu_task.previous = list(filter(lambda x: x is not found_mu_task[0], mu_task.previous))
                    after = len(mu_task.previous)
                    if after < before:
                        mu_task.previous.append(new_mu_task)
            for child in self.ids.micro_tasks_grid_layout.children:
                if child.text == old_name:
                    child.text = name
            self.mu_tasks.append(new_mu_task)

    def done(self):
        if self.creation_done is not None:
            self.creation_done(self.name, self.priority, self.deadline, self.mu_tasks)
        self.dismiss()

    def remove_micro_task(self, micro_task):
        for mu_task in self.mu_tasks:
            if mu_task.previous is not None:
                mu_task.previous = list(filter(lambda x: x.name is not micro_task.text, mu_task.previous))
        self.mu_tasks = list(filter(lambda x: x.name is not micro_task.text, self.mu_tasks))
        self.ids.micro_tasks_grid_layout.remove_widget(micro_task)

    def edit_micro_task(self, micro_task):
        found_mu_task = [ mu_task for mu_task in self.mu_tasks if mu_task.name == micro_task.text]
        if len(found_mu_task) == 1:
            tasks_pre_requisites = reduce(lambda x,y: x+y, [ mu_task.get_all_pre_requisites() for mu_task in self.mu_tasks], [])
            previous_to = [ mu_task for mu_task in self.mu_tasks if  found_mu_task[0] in mu_task.get_all_pre_requisites() ]
            non_pre_requisites = list(filter(lambda x: x not in tasks_pre_requisites and x is not found_mu_task[0] and x not in previous_to, self.mu_tasks))
            non_pre_requisites_names = [mu_task.name for mu_task in non_pre_requisites]
            previous_mu_tasks = found_mu_task[0].previous if found_mu_task[0].previous is not None else []
            previous_mu_tasks = list(map(lambda x: x.name, previous_mu_tasks))
            popup = CreateMicroTaskPopup(editing=True,
                                         title='Edit micro task',
                                         position=found_mu_task[0].position,
                                         task_type=found_mu_task[0].type,
                                         task_types=self.task_types, 
                                         name=found_mu_task[0].name, 
                                         previous_micro_tasks=non_pre_requisites_names,
                                         previous_micro_tasks_selected=previous_mu_tasks,
                                         size_hint=(0.5,0.5))
            popup.done = self.edit_micro_task_done
            popup.open()
