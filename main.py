from base_conhecimento import BaseConhecimento
from assistente import Assistente


def main():
    print("=" * 48)
    print("       CITIZEN ASSIST AI")
    print(" Assistente Digital de Orientação ao Cidadão")
    print("=" * 48)

    base = BaseConhecimento("data/base_conhecimento.json")
    base.carregar()

    assistente = Assistente("Citizen Assist AI", base)
    assistente.carregar_historico()

    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Fazer uma pergunta")
        print("2. Navegar por categorias")
        print("3. Ver indicadores desta execução")
        print("0. Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "1":
            assistente.perguntar()
        elif opcao == "2":
            assistente.navegar()
        elif opcao == "3":
            assistente.indicadores()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Escolha 0, 1, 2 ou 3.")

    facilidade = None
    while True:
        nota = input("\nDe 1 a 5, quão fácil foi usar o assistente? ").strip()
        if nota.isdigit() and 1 <= int(nota) <= 5:
            facilidade = int(nota)
            break
        print("Nota inválida. Digite um número de 1 a 5.")

    assistente.indicadores(facilidade)
    assistente.exportar_csv()
    print("\nObrigado por utilizar o Citizen Assist AI!")


if __name__ == "__main__":
    main()
