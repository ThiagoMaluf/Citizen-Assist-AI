import json
import re
import unicodedata
from orientacao import Orientacao


STOPWORDS = {"de", "do", "da", "dos", "das", "no", "na", "nos", "nas", "em", "o", "a", "os", "as", "um", "uma", "para", "pra", "com", "que", "como", "onde", "qual"}


def normalizar(texto):
    texto = unicodedata.normalize("NFD", texto.lower().strip())
    texto = "".join(letra for letra in texto if unicodedata.category(letra) != "Mn")
    texto = re.sub(r"[^a-z0-9 ]", " ", texto)
    return " " + " ".join(texto.split()) + " "


def radical(palavra):
    if len(palavra) > 4 and palavra.endswith("s"):
        return palavra[:-1]
    return palavra


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
        tokens_pergunta = [radical(p) for p in pergunta_n.split() if p not in STOPWORDS]
        set_pergunta = set(tokens_pergunta)
        pontos = 0

        for palavra in orientacao.palavras_chave:
            chave_n = normalizar(palavra).strip()
            if not chave_n:
                continue

            if (" " + chave_n + " ") in pergunta_n:
                pontos += 3
            else:
                tokens_chave = [radical(p) for p in chave_n.split() if p not in STOPWORDS]
                if tokens_chave and all(tk in set_pergunta for tk in tokens_chave):
                    pontos += 3

        palavras_titulo = {radical(p) for p in titulo_n.split() if len(p) >= 4 and p not in STOPWORDS}
        for palavra in set_pergunta:
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