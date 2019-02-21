from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, DictProperty
from menu import Menu
from display import Display
from display_menu import DisplayMenu

Builder.load_string('''
<TaskPlanningWindow>:
    display: display
    menu: menu
    Menu:
        display: root.ids.display
        id: menu
        size_hint: 0.20, 1
        on_file_loaded: root.task_domain = args[1]
    Display:
        id: display
        on_objects: root.ids.display_menu.display_objects_changed(*args)
        on_selected_object: root.ids.display_menu.on_object_selected(*args)
        on_is_object_selected: root.ids.display_menu.on_is_object_selected(*args)
    DisplayMenu:
        id: display_menu
        size_hint: 0.25, 1
        on_object_menu_selected: root.ids.display.on_object_menu_selected(*args)
''')

class TaskPlanningWindow(BoxLayout):
    menu = ObjectProperty(None)
    display = ObjectProperty(None)
    task_domain = DictProperty({})

    def file_loaded(self, parsed_file):
        pass