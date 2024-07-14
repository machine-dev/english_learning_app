from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.properties import StringProperty

class WordBox(BoxLayout):
    word = StringProperty()
    definition = StringProperty()
    example = StringProperty()
    date_added = StringProperty()
    
    def __init__(self, word, definition, example, date_added, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.definition = definition
        self.example = example
        self.date_added = date_added
        self.add_widget(Label(text=f"登録日: {self.date_added}"))
        self.add_widget(Label(text=self.word))
        self.add_widget(Label(text=self.definition))
        self.add_widget(Label(text=self.example))
        speak_button = Button(text="読み上げ")
        speak_button.bind(on_press=self.speak_word)
        self.add_widget(speak_button)

    def speak_word(self, instance):
        from app.utils.api import speak_word
        speak_word(self.word)
