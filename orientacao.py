class Orientacao:
    def __init__(self, dados):
        self.id = dados["id"]
        self.categoria = dados["categoria"]
        self.titulo = dados["titulo"]
        self.palavras_chave = dados["palavras_chave"]
        self.resposta = dados["resposta"]
        self.documentos = dados["documentos"]
        self.onde = dados["onde"]
        self.fonte = dados["fonte"]
        self.verificado_em = dados["verificado_em"]

    def exibir(self):
        print("\n>>", self.titulo, f"[{self.categoria}]")
        print(self.resposta)
        print("Documentos necessários:")
        for documento in self.documentos:
            print("-", documento)
        print("Onde:", self.onde)
        print("Fonte:", self.fonte)
        print("Verificado em:", self.verificado_em)
        print("Aviso: este assistente não é um canal oficial.")
