from gigachat import GigaChat
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.clock import Clock

api_key = 'MDE5Y2Y5Y2EtODA1Zi03ZjJhLTlmM2YtYWIzNzM4MGI1MTZhOjAwM2E0YTA4LTQwNDktNGY1Ni04ZjlmLTk3YzQ1ODA1NmMzMg=='

class VasiaChatLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = 5
        self.padding = 10

        self.scroll_view = ScrollView(
            size_hint=(1, 0.8),
            do_scroll_x=False
        )

        self.chat_display = Label(
            markup=True,
            size_hint_y=None,
            halign='left',
            valign='top',
            text_size=(Window.width * 0.95, None)
        )
        self.chat_display.bind(texture_size=self.chat_display.setter('size'))

        self.scroll_view.add_widget(self.chat_display)

        self.input_field = TextInput(
            multiline=False,
            size_hint_y=None,
            height=40,
            hint_text='Введите сообщение и нажмите Enter...',
            font_size=14
        )
        self.input_field.bind(on_text_validate=self.send_message)
        self.add_widget(self.scroll_view)
        self.add_widget(self.input_field)
        self.giga = GigaChat(credentials=api_key, verify_ssl_certs=False)
        self.messages = []
        self.has_loading_indicator = False
        self.add_message('Вася', 'Привет!', is_assistant=True)

    def send_message(self, instance):
        user_input = instance.text.strip()
        if not user_input:
            return

        self.add_message('Вы', user_input, is_user=True)
        instance.text = ''

        self.show_loading_indicator()

        Clock.schedule_once(lambda dt: self.get_response(user_input), 0.1)

    def show_loading_indicator(self):
        if not self.has_loading_indicator:
            self.messages.append({
                'sender': 'Вася',
                'text': 'печатает...',
                'is_loading': True,
                'color': '#f39c12'
            })
            self.has_loading_indicator = True
            self.update_chat_display()

    def hide_loading_indicator(self):
        if self.has_loading_indicator:
            if self.messages and self.messages[-1].get('is_loading'):
                self.messages.pop()
                self.has_loading_indicator = False
                self.update_chat_display()

    def add_message(self, sender, text, is_user=False, is_assistant=False):
        color = '#2ecc71' if is_user else '#9b59b6'
        self.messages.append({
            'sender': sender,
            'text': text,
            'is_user': is_user,
            'is_assistant': is_assistant,
            'color': color
        })
        self.update_chat_display()

    def update_chat_display(self):
        lines = []
        for msg in self.messages:
            if msg.get('is_loading'):
                lines.append(f'[color={msg["color"]}]{msg["sender"]} {msg["text"]}[/color]\n')
            else:
                lines.append(f'[color={msg["color"]}]{msg["sender"]}: {msg["text"]}[/color]\n')
        self.chat_display.text = ''.join(lines)

    def get_response(self, user_input):
        try:
            response = self.giga.chat(user_input)
            assistant_reply = response.choices[0].message.content
            Clock.schedule_once(
                lambda dt: self.display_assistant_response(assistant_reply),
                0.5
            )
        except Exception as e:
            self.hide_loading_indicator()
            self.add_message('Система', 'Ошибка при получении ответа', is_assistant=True)

    def display_assistant_response(self, assistant_reply):
        self.hide_loading_indicator()
        self.add_message('Вася', assistant_reply, is_assistant=True)

    def append_to_chat(self, message):
        pass

    def scroll_to_bottom(self, *args):
        self.scroll_view.scroll_y = 0



class VasiaChatApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 1)
        return VasiaChatLayout()


if __name__ == '__main__':
    VasiaChatApp().run()
