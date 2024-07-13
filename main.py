import os
from models import Base, engine, session, Word, Reminder

# データベースファイルを削除して新しいスキーマで再作成
if os.path.exists('words.db'):
    os.remove('words.db')

Base.metadata.create_all(engine)

from kivy.config import Config
Config.read('config.ini')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
from api import fetch_definition
from utils import speak_word
from reminders import check_reminders
from datepicker import DatePicker
from timepicker import TimePicker

FONT_PATH = "/Users/sn/Desktop/for_dev_me/english_learning_app/NotoSansJP-VariableFont_wght.ttf"  # フォントファイルのパス

class WordBox(BoxLayout):
    word = ''
    definition = ''
    example = ''
    date_added = ''
    
    def __init__(self, word, definition, example, date_added, **kwargs):
        super().__init__(**kwargs)
        self.word = word
        self.definition = definition
        self.example = example
        self.date_added = date_added

        self.add_widget(Label(text=f"登録日: {self.date_added}", font_name=FONT_PATH, size_hint_y=None, height=40))
        self.add_widget(Label(text=self.word, font_name=FONT_PATH, size_hint_y=None, height=40))
        self.add_widget(Label(text=self.definition, font_name=FONT_PATH, size_hint_y=None, height=40))
        self.add_widget(Label(text=self.example, font_name=FONT_PATH, size_hint_y=None, height=40))

    def speak_word(self):
        speak_word(self.word)

class MenuScreen(Screen):
    pass

class WordListScreen(Screen):
    pass

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(WordListScreen(name='word_list'))
        return sm

    def on_start(self):
        check_reminders(0)

    def add_word(self):
        word_input = self.root.get_screen('menu').ids.word_input
        definition_input = self.root.get_screen('menu').ids.definition_input
        example_input = self.root.get_screen('menu').ids.example_input
        word = word_input.text
        definition = definition_input.text or fetch_definition(word)
        example = example_input.text
        if word and definition:
            new_word = Word(word=word, definition=definition, example=example)
            session.add(new_word)
            session.commit()
            word_input.text = ''
            definition_input.text = ''
            example_input.text = ''

    def show_word_list(self):
        self.root.current = 'word_list'
        self.load_words()

    def show_menu(self):
        self.root.current = 'menu'

    def load_words(self):
        word_list_layout = self.root.get_screen('word_list').ids.word_list_layout
        word_list_layout.clear_widgets()
        words = session.query(Word).all()
        for word in words:
            word_box = WordBox(word.word, word.definition, word.example, word.date_added.strftime('%Y-%m-%d'))
            word_list_layout.add_widget(word_box)

    def show_reminder_popup(self):
        self.reminder_popup = Popup(title='リマインダー設定', size_hint=(0.8, 0.8))
        popup_layout = BoxLayout(orientation='vertical', padding=10)

        self.reminder_message_input = TextInput(hint_text="リマインダーのメッセージ", font_name=FONT_PATH, size_hint_y=None, height=40)
        popup_layout.add_widget(self.reminder_message_input)

        self.date_picker = DatePicker(size_hint_y=None, height=40)
        popup_layout.add_widget(self.date_picker)

        self.time_picker = TimePicker(size_hint_y=None, height=40)
        popup_layout.add_widget(self.time_picker)

        set_button = Button(text="設定", font_name=FONT_PATH, size_hint_y=None, height=40)
        set_button.bind(on_press=self.set_reminder)
        popup_layout.add_widget(set_button)

        self.reminder_popup.add_widget(popup_layout)
        self.reminder_popup.open()

    def set_reminder(self, instance):
        message = self.reminder_message_input.text
        reminder_date = self.date_picker.date
        reminder_time = self.time_picker.time
        reminder_datetime = datetime.combine(reminder_date, reminder_time)

        if message and reminder_datetime:
            new_reminder = Reminder(message=message, time=reminder_datetime)
            session.add(new_reminder)
            session.commit()
            self.reminder_popup.dismiss()

if __name__ == '__main__':
    MainApp().run()
