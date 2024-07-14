from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from app.screens.menu_screen import MenuScreen
from app.screens.word_list_screen import WordListScreen
from app.utils.database import Base, engine

Base.metadata.create_all(engine)

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(WordListScreen(name='word_list'))
        return sm

if __name__ == '__main__':
    MainApp().run()
