# Citizen Assist AI

**Global Solution 2026.2 — Pensamento Computacional e Automação com Python**

## 1. Proposta
Assistente executado no terminal que orienta jovens sobre documentos, emprego, saúde e serviços públicos. O sistema responde somente com informações cadastradas em uma base JSON e apresenta fonte, data de verificação e aviso de limitação.

## 2. Público e problema
- **Público:** jovens que precisam localizar informações sobre documentos e serviços públicos.
- **Problema:** orientações oficiais podem estar espalhadas em diferentes portais e nem sempre são fáceis de localizar.

## 3. ODS relacionados
- **ODS 4 — Educação de qualidade:** facilita o acesso a informações úteis.
- **ODS 8 — Trabalho decente e crescimento econômico:** reúne orientações sobre carteira de trabalho e seguro-desemprego.
- **ODS 16 — Paz, justiça e instituições eficazes:** facilita o acesso a informações de serviços públicos e direitos.

## 4. Estrutura
```text
citizen-assist-ai/
├── README.md
├── main.py
├── orientacao.py
├── base_conhecimento.py
├── assistente.py
└── data/
    ├── base_conhecimento.json
    ├── historico.json
    └── atendimentos.csv
```

## 5. Como executar
1. Instale Python 3.
2. Baixe ou clone este repositório.
3. Abra a pasta no VS Code.
4. No terminal, execute:
   ```bash
   python main.py
   ```
Não são necessárias bibliotecas externas.

## 6. Organização em classes
- `Orientacao`: representa um registro da base e possui o método `exibir()`.
- `BaseConhecimento`: carrega o JSON, lista categorias, filtra orientações e realiza a busca.
- `Assistente`: controla o menu, os atendimentos, o histórico, os indicadores e o CSV.

A composição é feita porque o objeto `Assistente` recebe um objeto `BaseConhecimento`, que contém uma lista de objetos `Orientacao`.

## 7. Regra de busca e confiança
A função `normalizar()` converte o texto para minúsculas, remove acentos, pontuação e espaços repetidos.
- Cada palavra-chave encontrada na pergunta vale **3 pontos**.
- Cada palavra da pergunta com 4 letras ou mais que aparece no título vale **1 ponto**.
- **6 pontos ou mais:** confiança ALTA.
- **3 a 5 pontos:** confiança MÉDIA.
- **Menos de 3 pontos:** o sistema informa que não encontrou uma orientação confiável.

A busca retorna uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação.

## 8. Privacidade e limitações
O programa recusa perguntas com `@` ou sequência de 8 ou mais dígitos e não registra essas entradas recusadas. Ele não solicita nome, CPF, telefone ou e-mail. A detecção é uma proteção simples, não uma garantia de identificação de todo dado pessoal. O programa não substitui atendimento oficial e só responde com os dados cadastrados no JSON. A equipe deve revisar as fontes e datas antes da apresentação.

## 9. Fontes consultadas
As fontes oficiais e as datas de verificação estão em cada registro de `data/base_conhecimento.json`. Foram consultados portais do Governo Federal, Ministério do Trabalho e Emprego, Ministério da Saúde, Ministério da Defesa, Ministério do Desenvolvimento e Assistência Social, Ministério da Justiça e Segurança Pública e Tribunal Superior Eleitoral.

## 10. Teste com usuários — preencher após realizar
**Não invente resultados.** Teste com pelo menos 3 pessoas de fora da equipe, somando 10 ou mais atendimentos. Registre aqui os resultados reais:
- Número de participantes:
- Total de atendimentos:
- Resposta encontrada (%):
- Taxa de acerto / ajudou (%):
- Tempo médio:
- Tentativas médias:
- Facilidade média (1 a 5):
- Dúvidas sem solução:
- Melhoria realizada após o teste:

## 11. Integrantes
- Thiago Maluf Hofmann — RM:569852
- Pedro Yoshikado Garcia — RM:570449
- Pedro Andreassa Zamai — RM:569318

## 12. Vídeo técnico
Link do vídeo não listado no YouTube: **PREENCHER**

## 13. Antes da entrega
- [ ] Executar e testar todas as opções.
- [ ] Testar com 3 pessoas e pelo menos 10 atendimentos.
- [ ] Registrar os resultados reais neste README.
- [ ] Gravar o vídeo e inserir o link.
- [ ] Publicar o repositório como público.
- [ ] Preparar o arquivo TXT exigido no portal FIAP.
