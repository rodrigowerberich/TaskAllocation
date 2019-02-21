from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, ReferenceListProperty, ListProperty, ObjectProperty

class DisplayObject(Widget):
    name = StringProperty('')
    display_name = StringProperty('')
    x_pos = NumericProperty(0)
    y_pos = NumericProperty(0)
    local_pos = ReferenceListProperty(x_pos, y_pos)
    default_size = ListProperty([])
    z_pos = NumericProperty(0)
    display_info_widget = ObjectProperty(None)
    def __init__(self, obj_type, **kwargs):
        super(DisplayObject, self).__init__(**kwargs)
        self.obj_type = obj_type
        if 'x_pos'in kwargs and 'y_pos' in kwargs:
            self.x_pos = kwargs['x_pos']
            self.y_pos = kwargs['y_pos']
        elif 'local_pos' in kwargs:
            self.local_pos = kwargs['local_pos']
        else:
            raise AssertionError('Missing obrigatory local position parameter')
        if 'default_size' in kwargs:
            self.default_size = kwargs['default_size']
        else:
            raise AssertionError('Missing obrigatory default_size parameter')
        if 'name' in kwargs:
            self.name = kwargs['name']
        else:
            raise AssertionError('Missing obrigatory name parameter')
        if 'z_pos' in kwargs:
            self.z_pos = kwargs['z_pos']
        else:
            raise AssertionError('Missing obrigatory z_pos parameter')
        self.display_name = str(self.obj_type)+':'+self.name

    def calculate_canvas_position(self, canvas_center, canvas_size, axis_max_value):
        return canvas_center[0] + (self.x_pos)*(canvas_size[0]/2)/(axis_max_value)-self.default_size[0]/2\
            , canvas_center[1]+(self.y_pos)*(canvas_size[1]/2)/(axis_max_value)-self.default_size[1]/2

    def calculate_local_position(self, canvas_center, canvas_size, axis_max_value):
        return (self.pos[0]-canvas_center[0]+self.default_size[0]/2)*(axis_max_value)/(canvas_size[0]/2),\
            (self.pos[1]-canvas_center[1]+self.default_size[1]/2)*(axis_max_value)/(canvas_size[1]/2)

    def move_canvas(self, new_position):
        self.pos = new_position[0]-self.default_size[0]/2, new_position[1]-self.default_size[1]/2 

    def move_local(self, new_position, canvas_center, canvas_size, axis_max_value):
        self.local_pos = new_position
        self.pos = self.calculate_canvas_position(canvas_center, canvas_size, axis_max_value)

    def on_name(self, instance, value):
        try:
            self.display_name = str(self.obj_type)+':'+value
        except AttributeError:
            pass