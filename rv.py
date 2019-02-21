from kivy.lang import Builder
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty, ObjectProperty, StringProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

Builder.load_string('''
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
<RV>:
    viewclass: 'SelectableLabel'
    controller: controller
    SelectableRecycleBoxLayout:
        id: controller
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: False
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''


class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    display_object = ObjectProperty(None)
    old_display = None

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected

    def on_display_object(self, instance,  value):
        if self.old_display is not None:
            self.old_display.unbind(display_name=self.change_display_name)
            self.text = value.display_name
        
        self.display_object = value
        self.old_display = value
        self.display_object.bind(display_name=self.change_display_name)

    def change_display_name(self, instance,  value):
        self.text = value

    def on_text(self, instance, value):
        if self.parent is not None:
            self.parent.parent.data[self.index]['text'] = value

class RV(RecycleView):
    controller = ObjectProperty(None)
    selected_value = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)

    def select_view(self, key):
        for node in self.controller.children:
            if node.text == key:
                self.controller.select_node(node.index)

    def deselect_view(self):
        self.controller.clear_selection()

    def on_controller(self, instance,  value):
        value.bind(selected_nodes=self.selected_nodes_changed)

    def selected_nodes_changed(self, instance, value):
        if len(value) == 1:
            self.selected_value = instance.children[-value[0]+(len(instance.children)-1)].display_object 