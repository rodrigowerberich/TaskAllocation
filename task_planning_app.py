from kivy.app import App
from task_planning_window import TaskPlanningWindow

class TaskPlanningApp(App):
    def build(self):
        return TaskPlanningWindow()

if __name__ == '__main__':
    TaskPlanningApp().run()