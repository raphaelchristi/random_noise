from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from bs4 import BeautifulSoup
import random
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class RandomSongApp(App):
    def build(self):
        # Layout principal
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Elementos da interface
        label_boas_vindas = Label(
            text="Bem-vindo ao Random Song!",
            font_size=20, bold=True, color=(0.2, 0.6, 0.9, 1)
        )
        label_instrucao = Label(
            text="Clique no botão 'Run' para obter um gênero de música aleatório.",
            color=(0.4, 0.4, 0.4, 1)
        )
        self.resultado_texto = TextInput(
            text="",
            multiline=True,
            readonly=True,
            font_size=14,
            background_color=(0.9, 0.9, 0.9, 1),
            foreground_color=(0, 0, 0, 1)
        )

        # Botão "Run"
        botao_run = Button(
            text="Run",
            on_press=self.obter_genero_aleatorio,
            font_size=16,
            background_color=(0.2, 0.6, 0.9, 1),
            color=(1, 1, 1, 1)
        )

        # Adicionando elementos ao layout
        layout.add_widget(label_boas_vindas)
        layout.add_widget(label_instrucao)
        layout.add_widget(botao_run)
        layout.add_widget(ScrollView(size=(400, 300), size_hint=(None, None), do_scroll_x=False))
        layout.add_widget(self.resultado_texto)

        return layout

    def obter_genero_aleatorio(self, instance):
        url = 'https://everynoise.com/everynoise1d.cgi?scope=all'
        response = requests.get(url, verify=False)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            td_tags = soup.find_all('td', class_='note')
            dados = []

            for td in td_tags:
                a_tag = td.find('a')
                if a_tag:
                    genero = a_tag.text.strip().lower()
                    link = a_tag['href']
                    dados.append({'genero': genero, 'link': link})

            item_aleatorio = random.choice(dados)
            self.resultado_texto.text = f"Genero aleatorio recomendado: {item_aleatorio['genero']}\n" \
                                         f"Link associado: https://everynoise.com/everynoise1d.cgi{item_aleatorio['link']}"
        else:
            self.resultado_texto.text = f"Erro ao acessar a página. Código de status: {response.status_code}"

# Executar o aplicativo
if __name__ == '__main__':
    RandomSongApp().run()
