from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from datetime import datetime

class DatePicker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.date_label = Label(text=datetime.now().strftime('%Y-%m-%d'))
        self.add_widget(self.date_label)
        self.select_button = Button(text="日付を選択")
        self.select_button.bind(on_press=self.show_date_picker)
        self.add_widget(self.select_button)

    def show_date_picker(self, instance):
        content = GridLayout(cols=7, padding=10)
        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for day in days:
            content.add_widget(Label(text=day))
        for day in range(1, 32):
            button = Button(text=str(day))
            button.bind(on_press=self.set_date)
            content.add_widget(button)
        self.popup = Popup(title='日付を選択', content=content, size_hint=(0.8, 0.8))
        self.popup.open()

    def set_date(self, instance):
        self.date_label.text = f"{datetime.now().strftime('%Y-%m')}-{instance.text}"
        self.popup.dismiss()

    @property
    def date(self):
        return datetime.strptime(self.date_label.text, '%Y-%m-%d').date()
