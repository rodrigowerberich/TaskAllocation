from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
from menu import Menu
from display import Display
from display_menu import DisplayMenu

class TaskPlanningWindow(BoxLayout):
    menu = ObjectProperty(None)
    display = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(TaskPlanningWindow, self).__init__(**kwargs)
        self.display = Display()
        self.menu = Menu(self.display, orientation='vertical', size_hint=(0.2,1))
        self.display_menu = DisplayMenu(size_hint=(0.2,1))
        self.display.bind(objects=self.display_menu.display_objects_changed, 
                          selected_object=self.display_menu.on_object_selected,
                          is_object_selected=self.display_menu.on_is_object_selected)
        self.display_menu.bind(object_menu_selected=self.display.on_object_menu_selected)
        self.add_widget(self.menu)
        self.add_widget(self.display)
        self.add_widget(self.display_menu)