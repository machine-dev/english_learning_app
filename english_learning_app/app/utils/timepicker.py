from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from datetime import datetime

class TimePicker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.time_label = Label(text=datetime.now().strftime('%H:%M'))
        self.add_widget(self.time_label)
        self.select_button = Button(text="時刻を選択")
        self.select_button.bind(on_press=self.show_time_picker)
        self.add_widget(self.select_button)

    def show_time_picker(self, instance):
        content = GridLayout(cols=6, padding=10)
        for hour in range(24):
            for minute in [0, 10, 20, 30, 40, 50]:
                time_str = f"{hour:02}:{minute:02}"
                button = Button(text=time_str)
                button.bind(on_press=self.set_time)
                content.add_widget(button)
        self.popup = Popup(title='時刻を選択', content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def set_time(self, instance):
        self.time_label.text = instance.text
        self.popup.dismiss()

    @property
    def time(self):
        return datetime.strptime(self.time_label.text, '%H:%M').time()
