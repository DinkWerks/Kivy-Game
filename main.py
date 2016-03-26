# Kivy Imports
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.properties import ObjectProperty, StringProperty
from kivy.app import App
# Utility Imports
import yaml
# Game Imports
from scripts.events import Event

# File Loads
loc_file = file('data/location.yml')
loc_dat = yaml.load(loc_file)

# Binding Classes
event = Event()


class EventWindow(BoxLayout):
    ct = ObjectProperty()

    def __init__(self, **kwargs):
        super(EventWindow, self).__init__(**kwargs)
        self.ct = event.current_text

ew = EventWindow()

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

        # Below section handles the location drop down
        self.dropdown = DropDown()
        self.dd_updater()
        self.ids.mb.bind(on_release=self.dropdown.open)  # opens the existing dropdown with added buttons
        self.dropdown.bind(on_select=lambda instance, x: self.location(x))

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
            # if child.id == 'pb':
            self.ids.mapspace.remove_widget(child)
        # self.ids.mapspace.remove_widget(EventWindow)
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
        # ew.changer()
        self.dd_updater()
        self.place_locale()


class Test(App):
    def build(self):
        return Foo()


Test().run()
