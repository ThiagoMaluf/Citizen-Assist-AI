import json
import re
import unicodedata
from orientacao import Orientacao


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")
    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    return " " + " ".join(texto.split()) + " "


class BaseConhecimento:
    def __init__(self, caminho):
        self.caminho = caminho
        self.orientacoes = []

    def carregar(self):
        try:
            with open(self.caminho, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if not isinstance(dados, list):
                raise ValueError("A base precisa ser uma lista.")
            self.orientacoes = [Orientacao(item) for item in dados]
            return True
        except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError, ValueError) as erro:
            print("Não foi possível carregar a base de conhecimento:", erro)
            self.orientacoes = []
            return False

    def categorias(self):
        return sorted(set(item.categoria for item in self.orientacoes))

    def por_categoria(self, categoria):
        return [item for item in self.orientacoes if item.categoria == categoria]

    def pontuar(self, pergunta, orientacao):
        pergunta_n = normalizar(pergunta)
        titulo_n = normalizar(orientacao.titulo)
        pontos = 0

        for palavra in orientacao.palavras_chave:
            chave_n = normalizar(palavra).strip()
            if chave_n and (" " + chave_n + " ") in pergunta_n:
                pontos += 3

        palavras_pergunta = set(pergunta_n.split())
        palavras_titulo = set(titulo_n.split())
        for palavra in palavras_pergunta:
            if len(palavra) >= 4 and palavra in palavras_titulo:
                pontos += 1

        return pontos

    def buscar(self, pergunta):
        resultados = []
        for orientacao in self.orientacoes:
            pontos = self.pontuar(pergunta, orientacao)
            if pontos > 0:
                resultados.append((pontos, orientacao))
        return sorted(resultados, key=lambda item: item[0], reverse=True)
