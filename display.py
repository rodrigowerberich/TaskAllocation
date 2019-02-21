import math
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import NumericProperty, BooleanProperty, ListProperty, ObjectProperty
from kivy.graphics import Rectangle, Color, InstructionGroup
from kivy.core.window import Window
from robot_representation import RobotRepresentation
from micro_task_representation import MuTaskRepresentation
from display_object import DisplayObject


class Display(Widget):
    axis_resolution = NumericProperty(10)
    axis_max_value = NumericProperty(10)
    axis_x_marker_size = (4, 8)
    axis_y_marker_size = (8, 4)
    last_inside = BooleanProperty(False)
    objects = ListProperty([])
    robots = ListProperty([])
    tasks = ListProperty([])
    mu_tasks = ListProperty([])
    selected_object = ObjectProperty(None)
    is_object_selected = BooleanProperty(False)
    dummy_object = DisplayObject('Dummy',name='Dummy',local_pos=(math.inf, math.inf), \
                                                        z_pos = -1,\
                                                        default_size=(0, 0))
    def __init__(self, **kwargs):
        super(Display, self).__init__(**kwargs)
        self.rect_x_ig = InstructionGroup()
        self.rect_x_ig.add(Color(1,1,1))
        self.rect_x = Rectangle(size=(self.width,2), pos=(self.center_x - self.width/2, self.center_y-1))
        self.rect_x_ig.add(self.rect_x)
        self.canvas.add(self.rect_x_ig)

        self.rect_y_ig = InstructionGroup()
        self.rect_y_ig.add(Color(1,1,1))
        self.rect_y = Rectangle(size=(2,self.height), pos=(self.center_x - 1, self.center_y-self.height/2))
        self.rect_y_ig.add(self.rect_y)
        self.canvas.add(self.rect_y_ig)

        values = range(2*self.axis_resolution+1)
        values_x = list(map(lambda x: self._calculate_axis_value(x, self.axis_resolution, self.width), values))
        values_y = list(map(lambda x: self._calculate_axis_value(x, self.axis_resolution, self.height), values))
        self.rects_x = []
        self.rects_y = []
        self.rects_x_ig = []
        self.rects_y_ig = []
        for value_x in values_x:
                self.rects_x += [Rectangle(size=self.axis_x_marker_size, pos=self._calculate_axis_x_marker_pos(value_x, self))]
                self.rects_x_ig += [self.rects_x[-1]]
                self.canvas.add(self.rects_x_ig[-1])
        for value_y in values_y:
                self.rects_y += [Rectangle(size=self.axis_y_marker_size, pos=self._calculate_axis_y_marker_pos(value_y, self))]
                self.rects_y_ig += [self.rects_y[-1]]
                self.canvas.add(self.rects_y_ig[-1])
        self.bind(size=self._update_rect, pos=self._update_rect, axis_resolution=self._update_rect, axis_max_value=self._update_rect)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.coordinate_label = Label(text='0,0')

    
    def add_robot(self, new_robot):
        name_exists = any([new_robot.name == robot.name for robot in self.objects if robot.obj_type is 'Robot'])
        if not name_exists:
            self.robots.append(new_robot)
            robot_representation = RobotRepresentation(new_robot, \
                                                        name=new_robot.name, \
                                                        local_pos=new_robot.position, \
                                                        z_pos = len(self.objects),\
                                                        default_size=(RobotRepresentation.default_width, RobotRepresentation.default_height))
            self.add_display_object(robot_representation)

    def add_task(self, new_task):
        name_exists = any([new_task.name == task.name for task in self.objects if task.obj_type is 'Task'])
        if not name_exists:
            self.tasks.append(new_task)
            for mu_task in new_task.mu_tasks:
                self.mu_tasks.append(mu_task)
                mu_task_representation = MuTaskRepresentation(name=new_task.name+','+mu_task.name, 
                    task=new_task,
                    mu_task=mu_task,
                    local_pos=mu_task.position,
                    z_pos = len(self.objects),
                    default_size=(MuTaskRepresentation.default_width, MuTaskRepresentation.default_height))
                self.add_display_object(mu_task_representation)
            
    def clear_display(self):
        for obj in self.objects:
            self.remove_widget(obj)
        self.objects = []
        self.robots.clear()
        self.mu_tasks.clear()
        self.tasks.clear()

    def add_display_object(self, new_object):
        self.objects.append(new_object)
        self.add_widget(new_object)
        new_object.pos = new_object.calculate_canvas_position(self.center, self.size, self.axis_max_value)
    
    @staticmethod
    def _calculate_axis_value(original_value, axis_resolution, axis_total_size):
        return ((original_value-axis_resolution)/axis_resolution)*(axis_total_size/2)
    
    def _calculate_axis_x_marker_pos(self, marker_value, reference):
        return reference.center_x+marker_value-(self.axis_x_marker_size[0])/2, reference.center_y-(self.axis_x_marker_size[1])/2

    def _calculate_axis_y_marker_pos(self, marker_value, reference):
        return reference.center_x-(self.axis_y_marker_size[0])/2, reference.center_y+marker_value-(self.axis_y_marker_size[1])/2

    def _update_rect(self, instance, value):
        values = range(2*self.axis_resolution+1)
        values_x = list(map(lambda x: self._calculate_axis_value(x, self.axis_resolution, self.width), values))
        values_y = list(map(lambda x: self._calculate_axis_value(x, self.axis_resolution, self.height), values))
        self.rect_x.size = instance.width, 2
        self.rect_x.pos = instance.center_x - instance.width/2, instance.center_y-1
        self.rect_y.size = 2, self.height
        self.rect_y.pos = self.center_x - 1, self.center_y-self.height/2
        for value_x, rect  in zip(values_x, self.rects_x):
            rect.pos = self._calculate_axis_x_marker_pos(value_x, instance)
            rect.size = self.axis_x_marker_size
        for value_y,rect  in zip(values_y, self.rects_y):
            rect.pos = self._calculate_axis_y_marker_pos(value_y, instance)
            rect.size = self.axis_y_marker_size
        
        if len(self.rects_x) > len(values_x):
            for i in range(len(self.rects_x), len(values_x), -1):
                self.canvas.remove(self.rects_x_ig[i-1])
                self.rects_x.pop()
                self.rects_x_ig.pop()
        elif len(self.rects_x) < len(values_x):
                for i in range(len(self.rects_x), len(values_x)):
                    self.rects_x += [Rectangle(size=self.axis_x_marker_size, pos=self._calculate_axis_x_marker_pos(values_x[i], self))]
                    self.rects_x_ig += [self.rects_x[-1]]
                    self.canvas.add(self.rects_x_ig[-1])
        
        if len(self.rects_y) > len(values_y):
            for i in range(len(self.rects_y), len(values_y), -1):
                self.canvas.remove(self.rects_y_ig[i-1])
                self.rects_y.pop()
                self.rects_y_ig.pop()
        elif len(self.rects_y) < len(values_y):
                for i in range(len(self.rects_y), len(values_y)):
                    self.rects_y += [Rectangle(size=self.axis_y_marker_size, pos=self._calculate_axis_y_marker_pos(values_y[i], self))]
                    self.rects_y_ig += [self.rects_y[-1]]
                    self.canvas.add(self.rects_y_ig[-1])
        for obj in self.objects:
            obj.pos = obj.calculate_canvas_position(instance.center, instance.size, self.axis_max_value)
    
    def on_touch_down(self, value):
        pos = value.pos
        if not self.collide_point(*self.to_widget(*pos)):
            return
        candidates = [ candidate for candidate in self.objects if candidate.collide_point(*self.to_widget(*pos))]
        top_candidate = max(candidates, key=lambda x: x.z_pos, default=None)
        if top_candidate is not None:
            # if not self.is_object_selected or (self.is_object_selected and not top_candidate.collide_widget(self.selected_object)):
            if not self.is_object_selected or (self.is_object_selected and self.selected_object not in candidates):
                self.selected_object = top_candidate
                self.is_object_selected = True
        else:
            if self.is_object_selected:
                self.is_object_selected = False
                self.selected_object = self.dummy_object
        
    def on_touch_move(self, value):
        pos = value.pos
        if not self.collide_point(*self.to_widget(*pos)):
            return
        if self.is_object_selected:
            self.selected_object.move_canvas(value.pos)

    def on_object_menu_selected(self, instance, value):
        if self.is_object_selected:
            if self.selected_object == value:
                return
            else:   
                options = [ obj for obj in self.objects if obj == value]
                if len(options) == 1:
                    self.selected_object = options[0]
                else:
                    self.selected_object = self.dummy_object
                    self.is_object_selected = False
        else:
            options = [ obj for obj in self.objects if obj == value]
            if len(options) == 1:
                self.selected_object = options[0]
                self.is_object_selected = True
            else:
                self.selected_object = self.dummy_object
                self.is_object_selected = False

    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if inside:
            self.coordinate_label.pos = pos
            local_pos = self._calculate_axis_x_marker_pos(0, self)
            local_pos = round((pos[0] - self.center_x)*(self.axis_max_value)/(self.width/2),2), round((pos[1] - self.center_y)*(self.axis_max_value)/(self.height/2), 2)
            self.coordinate_label.text = str(local_pos)
            self.coordinate_label.size = self.coordinate_label.texture_size
        if self.last_inside != inside:
            if inside:
                self.add_widget(self.coordinate_label)
            else:
                self.remove_widget(self.coordinate_label)
            self.last_inside = inside