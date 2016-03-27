# Kivy Imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
# Utility Imports
import yaml
# Game Imports
from scripts.events import Event

# File Loads
loc_file = file('data/location.yml')
loc_dat = yaml.load(loc_file)

# Bind Classes
event = Event()

class EventWindow(BoxLayout):
    ct = StringProperty('')

    def __init__(self, **kwargs):
        super(EventWindow, self).__init__(**kwargs)
        self.ct = event.current_text
        # Error occurs below. Comment out too see semi-functional app.
        Event.bind(current_text=self.setter('ct'))


class Foo(BoxLayout):
    current_map = ObjectProperty('maps/Havana.jpg')
    current_location = StringProperty()
    containers = ObjectProperty(loc_dat['Havana']['container'], allownone=True)

    def __init__(self, **kwargs):
        super(Foo, self).__init__(**kwargs)
        self.current_map = 'maps/Havana.jpg'
        self.current_location = 'Havana'
        self.containers = loc_dat['Havana']['container']
        self.locale = loc_dat['Havana']['connections']
        self.first_run = False

        # Drop Down code
        self.dropdown = DropDown()  # Binds Class
        self.dd_updater()  # Calls method to determine location containers
        self.ids.mb.bind(on_release=self.dropdown.open)  # Connects generated locations to
        self.dropdown.bind(on_select=lambda instance, x: self.location(x))  # Binds button's location changing behavior

        # Handles the placement of buttons on the map
        self.place_locale()

    def place_locale(self):
        if self.first_run is True:
            self.cleanup()
        if self.locale is None:
            pass
        else:
            for place in self.locale:
                place_button = Button(text=place,
                                      id='pb',
                                      size_hint=(.05, .05),
                                      pos_hint={'x': loc_dat[self.current_location]['connections'][place][0],
                                                'y': loc_dat[self.current_location]['connections'][place][1]},
                                      on_release=lambda destination: self.location(destination.text))
                self.ids.mapspace.add_widget(place_button)
        self.first_run = True

    def cleanup(self):
        for child in [child for child in self.ids.mapspace.children]:
            self.ids.mapspace.remove_widget(child)
        self.ids.mapspace.add_widget(self.ids.event)

    def dd_updater(self):
        self.dropdown.clear_widgets()
        if self.containers is None:
            pass
        else:
            for note in self.containers:  # Adds widgets to the existing dropdown
                btn = Button(text=note,
                             color=(0, 0, 0, 1),
                             background_normal='images/Button.png',
                             background_down='images/Button.png',
                             border=(0, 60, 0, 120),
                             size_hint_y=None,
                             height=30)
                btn.bind(on_release=lambda b: self.dropdown.select(b.text))
                self.dropdown.add_widget(btn)

    def location(self, new_loc):
        self.current_location = new_loc
        self.current_map = loc_dat[new_loc]['image']
        self.locale = loc_dat[new_loc]['connections']
        self.containers = loc_dat[new_loc]['container']
        event.event_name()
        event.parse()
        print event.current_text
        self.dd_updater()
        self.place_locale()


class Test(App):
    def build(self):
        return Foo()


Test().run()
