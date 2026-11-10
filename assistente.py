import csv
import json
import os
import re
import time
from datetime import datetime
from base_conhecimento import normalizar


class Assistente:
    def __init__(self, nome, base):
        self.nome = nome
        self.base = base
        self.historico = []
        self.arquivo_historico = "data/historico.json"

    def carregar_historico(self):
        try:
            with open(self.arquivo_historico, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
            if isinstance(dados, list):
                self.historico = dados
        except (FileNotFoundError, json.JSONDecodeError):
            self.historico = []

    def dado_pessoal(self, texto):
        return "@" in texto or bool(re.search(r"\\d{8,}", texto))

    def perguntar(self):
        inicio = time.time()
        tentativas = 1
        pergunta = input("\nDigite sua dúvida (0 para voltar): ").strip()

        if pergunta == "0":
            return
        if not pergunta:
            print("Digite uma pergunta para continuar.")
            return
        if self.dado_pessoal(pergunta):
            print("Atenção: não digite CPF, telefone, e-mail ou outros dados pessoais. Reescreva.")
            return

        resultados = self.base.buscar(pergunta)
        encontrados = [item for item in resultados if item[0] >= 3]

        ajudou = None
        id_orientacao = None
        encontrou = bool(encontrados)

        if encontrou:
            pontos, orientacao = encontrados[0]
            id_orientacao = orientacao.id
            confianca = "ALTA" if pontos >= 6 else "MÉDIA"
            print(f"\nConfiança da resposta: {confianca} ({pontos} pontos)")
            orientacao.exibir()

            for pontos_alt, alternativa in encontrados[1:3]:
                print(f"Alternativa: {alternativa.titulo} ({pontos_alt} pontos)")

            while True:
                resposta = input("\nEssa orientação respondeu sua dúvida? (s/n): ").strip().lower()
                if resposta in ("s", "n"):
                    ajudou = resposta == "s"
                    break
                print("Entrada inválida. Digite apenas s ou n.")
        else:
            print("\nNão encontrei uma orientação com confiança suficiente.")
            print("Tente outras palavras ou navegue pelas categorias.")
            while True:
                resposta = input("Essa busca ajudou? (s/n): ").strip().lower()
                if resposta in ("s", "n"):
                    ajudou = resposta == "s"
                    break
                print("Entrada inválida. Digite apenas s ou n.")

        registro = {
            "data": datetime.now().isoformat(timespec="seconds"),
            "origem": "pergunta",
            "pergunta": pergunta,
            "id_orientacao": id_orientacao,
            "encontrou": encontrou,
            "ajudou": ajudou,
            "tentativas": tentativas,
            "tempo_segundos": round(time.time() - inicio, 1)
        }
        self.registrar(registro)

    def navegar(self):
        categorias = self.base.categorias()
        if not categorias:
            print("Não há categorias disponíveis.")
            return

        while True:
            print("\n--- CATEGORIAS ---")
            for i, categoria in enumerate(categorias, 1):
                print(f"{i}. {categoria}")
            print("0. Voltar")
            escolha = input("Escolha uma categoria: ").strip()

            if escolha == "0":
                return
            if not escolha.isdigit() or not 1 <= int(escolha) <= len(categorias):
                print("Opção inválida. Tente novamente.")
                continue

            categoria = categorias[int(escolha) - 1]
            orientacoes = self.base.por_categoria(categoria)
            while True:
                print(f"\n--- {categoria.upper()} ---")
                for i, orientacao in enumerate(orientacoes, 1):
                    print(f"{i}. {orientacao.titulo}")
                print("0. Voltar")
                item = input("Escolha uma orientação: ").strip()

                if item == "0":
                    break
                if not item.isdigit() or not 1 <= int(item) <= len(orientacoes):
                    print("Opção inválida. Tente novamente.")
                    continue

                inicio = time.time()
                orientacao = orientacoes[int(item) - 1]
                orientacao.exibir()
                while True:
                    resposta = input("\nEssa orientação respondeu sua dúvida? (s/n): ").strip().lower()
                    if resposta in ("s", "n"):
                        ajudou = resposta == "s"
                        break
                    print("Entrada inválida. Digite apenas s ou n.")

                self.registrar({
                    "data": datetime.now().isoformat(timespec="seconds"),
                    "origem": "categoria",
                    "pergunta": orientacao.titulo,
                    "id_orientacao": orientacao.id,
                    "encontrou": True,
                    "ajudou": ajudou,
                    "tentativas": 1,
                    "tempo_segundos": round(time.time() - inicio, 1)
                })

    def registrar(self, registro):
        self.historico.append(registro)
        os.makedirs("data", exist_ok=True)
        with open(self.arquivo_historico, "w", encoding="utf-8") as arquivo:
            json.dump(self.historico, arquivo, ensure_ascii=False, indent=4)

    def indicadores(self, facilidade=None):
        total = len(self.historico)
        if total == 0:
            print("\nNenhum atendimento registrado nesta execução.")
            return

        encontrados = sum(1 for item in self.historico if item["encontrou"])
        ajudou = sum(1 for item in self.historico if item["ajudou"] is True)
        tempo = sum(item["tempo_segundos"] for item in self.historico) / total
        tentativas = sum(item["tentativas"] for item in self.historico) / total
        sem_solucao = [item["pergunta"] for item in self.historico if item["ajudou"] is False]

        print("\n--- INDICADORES ---")
        print(f"Resposta encontrada: {encontrados / total * 100:.1f}%")
        print(f"Taxa de acerto (ajudou): {ajudou / total * 100:.1f}%")
        print(f"Tempo médio por atendimento: {tempo:.1f} segundos")
        print(f"Tentativas por atendimento: {tentativas:.1f}")
        if facilidade is not None:
            print(f"Facilidade de uso: {facilidade}/5")
        print("Dúvidas sem solução:")
        if sem_solucao:
            for duvida in sem_solucao:
                print("-", duvida)
        else:
            print("- Nenhuma registrada.")

    def exportar_csv(self):
        os.makedirs("data", exist_ok=True)
        campos = ["data", "origem", "pergunta", "id_orientacao", "encontrou",
                  "ajudou", "tentativas", "tempo_segundos"]
        with open("data/atendimentos.csv", "w", newline="", encoding="utf-8-sig") as arquivo:
            escritor = csv.DictWriter(arquivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(self.historico)
        print("Atendimentos exportados para data/atendimentos.csv")
