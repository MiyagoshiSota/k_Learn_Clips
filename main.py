import os
from dotenv import load_dotenv, set_key, get_key

from services import main

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.uix.floatlayout import FloatLayout
from kivy.config import Config
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.button import Button

# ウィンドウサイズを固定する設定
Config.set('graphics', 'width', '300')  # 幅を固定
Config.set('graphics', 'height', '300')  # 高さを固定

# 日本語フォントを登録
LabelBase.register(name='JapaneseFont', fn_regular='./fonts/ヒラギノ角ゴシック W3.ttc')

# .envファイルをロード
load_dotenv()

# kivy言語で記述
Layout = Builder.load_string('''
<Root_Layout>:
    font_name: 'JapaneseFont'

    TextInput:
        id: text_A
        size_hint_y: None
        height: '200dp'
        font_name: 'JapaneseFont'
        multiline: False 
        size_hint: 0.92,0.1
        pos_hint: {"x":0, "top":1}
        hint_text: "API key"
        text: "" if root.check_API_key_null() else root.get_API_key()
        
    TextInput:
        id: text_B
        size_hint_y: None
        height: '200dp'
        font_name: 'JapaneseFont'
        multiline: False 
        size_hint: 0.92,0.1
        pos_hint: {"x":0, "top":0.9}
        hint_text: "キーワード"

    TextInput:
        id: text_C
        size_hint_y: None
        height: '200dp'
        font_name: 'JapaneseFont'
        multiline: False 
        size_hint: 0.92,0.1
        input_filter: 'int'
        pos_hint: {"x":0, "top":0.8}
        hint_text: "単語数"

    Button:
        id: apikeyset
        background_color: (0, 1, 0, 1)
        text: 'API keyを設定する'
        font_name: 'JapaneseFont'
        on_press: root.set_API_key()
        pos_hint: {"x":0, "top":0.7}
        size_hint: 1,0.3

    Button:
        id: make
        background_color: (0, 1, 0, 1)
        text: '作成する'
        font_name: 'JapaneseFont'
        on_press: root.open_filechooser()
        pos_hint: {"x":0, "top":0.4}
        size_hint: 1,0.4
        
    Button:
        id: clear_1
        background_color: (1, 1, 1, 1)
        font_size: 15
        text: 'クリア'
        font_name: 'JapaneseFont'
        on_press: root.clear_API_text()
        pos_hint: {"x":0.92, "top":1}
        size_hint: 0.08,0.1
        
    Button:
        id: clear_2
        background_color: (1, 1, 1, 1)
        font_size: 15
        text: 'クリア'
        font_name: 'JapaneseFont'
        on_press: root.clear_keyword_text()
        pos_hint: {"x":0.92, "top":0.9}
        size_hint: 0.08,0.1
        
    Button:
        id: clear_3
        background_color: (1, 1, 1, 1)
        font_size: 15
        text: 'クリア'
        font_name: 'JapaneseFont'
        on_press: root.clear_num_text()
        pos_hint: {"x":0.92, "top":0.8}
        size_hint: 0.08,0.1

<FileChooserPopup>:
    BoxLayout:
        orientation: 'vertical'
        FileChooserListView:
            id: filechooser
            dirselect: True
        BoxLayout:
            size_hint_y: None
            height: '50dp'
            Button:
                text: "Select"
                on_release: root.select(filechooser.path)
            Button:
                text: "Cancel"
                on_release: root.dismiss()
''')


class FileChooserPopup(Popup):

    def select(self, selected_path):
        if selected_path:
            self.dismiss()
            App.get_running_app().root.make(selected_path)
        else:
            popup = Popup(title="Error",
                          content=Label(text="No directory selected."),
                          size_hint=(None, None),
                          size=(300, 200))
            popup.open()


class Root_Layout(FloatLayout):

    def check_API_key_null(self):
        env_file = ".env"
        return '' == get_key(env_file, "OPENAI_API_KEY")

    def get_API_key(self):
        env_file = ".env"
        return get_key(env_file, "OPENAI_API_KEY")

    def set_API_key(self):
        api_key = self.ids.text_A.text
        env_file = ".env"
        set_key(env_file, "OPENAI_API_KEY", api_key)

        popup = Popup(title="Save completed",
                      content=Label(text="API key saved", ),
                      size_hint=(None, None),
                      size=(300, 200))
        popup.open()

    def open_filechooser(self):
        popup = FileChooserPopup(title="Select Directory")
        popup.open()

    def make(self, directory):
        if not os.path.isdir(directory):
            popup = Popup(title="Error",
                          content=Label(text="Invalid directory."),
                          size_hint=(None, None),
                          size=(300, 200))
            popup.open()
            return

        if self.ids.text_A.text == '':
            popup = Popup(title="Error",
                          content=Label(text="API key not entered."),
                          size_hint=(None, None),
                          size=(300, 200))
            popup.open()
        elif self.ids.text_B.text == '':
            popup = Popup(title="Error",
                          content=Label(text="Keyword not entered."),
                          size_hint=(None, None),
                          size=(300, 200))
            popup.open()
        elif self.ids.text_C.text == '':
            popup = Popup(title="Error",
                          content=Label(text="Number not entered."),
                          size_hint=(None, None),
                          size=(300, 200))
            popup.open()
        else:
            main.make(self.ids.text_A.text, self.ids.text_B.text,
                      self.ids.text_C.text)
            mp4_file_path = "./services/outputs/output.mp4"

            if mp4_file_path and os.path.isfile(mp4_file_path):
                destination_path = os.path.join(
                    directory, os.path.basename(mp4_file_path))
                os.rename(mp4_file_path, destination_path)

                popup = Popup(
                    title="Success",
                    content=Label(text=f"File saved to: {destination_path}"),
                    size_hint=(None, None),
                    size=(300, 200))
                popup.open()
            else:
                popup = Popup(title="Error",
                              content=Label(text="File generation failed."),
                              size_hint=(None, None),
                              size=(300, 200))
                popup.open()

    def clear_API_text(self):
        self.ids.text_A.text = ''

    def clear_keyword_text(self):
        self.ids.text_B.text = ''

    def clear_num_text(self):
        self.ids.text_C.text = ''


class KrStvideoGeneratorApp(App):

    def build(self):
        return Root_Layout()


if __name__ == '__main__':
    KrStvideoGeneratorApp().run()
