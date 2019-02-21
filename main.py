from kivy.config import Config
Config.set('graphics', 'minimum_width', 800)
Config.set('graphics', 'minimum_height', 600)
from kivy.app import App
from task_planning_window import TaskPlanningWindow

class TaskPlanningApp(App):
    def build(self):
        return TaskPlanningWindow()

if __name__ == '__main__':
    TaskPlanningApp().run()