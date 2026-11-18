# Citizen Assist AI

**Global Solution 2026.2 — Pensamento Computacional e Automação com Python**

## 1. Proposta
Assistente executado no terminal que orienta jovens e cidadãos sobre documentos, emprego, saúde, educação e serviços públicos. O sistema responde somente com informações verificadas cadastradas em uma base JSON e apresenta fonte oficial, data de verificação e aviso de limitação.

## 2. Público e problema
- **Público:** jovens e cidadãos que precisam localizar informações confiáveis sobre documentos, emprego, saúde e serviços públicos.
- **Problema:** orientações oficiais costumam estar espalhadas em diferentes portais do governo, com linguagem técnica, dificultando o acesso rápido aos requisitos e canais corretos.

## 3. ODS relacionados
- **ODS 4 — Educação de qualidade:** facilita o acesso a informações sobre ENEM, SISU, Prouni, Fies e documentação estudantil.
- **ODS 8 — Trabalho decente e crescimento econômico:** reúne orientações sobre Carteira de Trabalho Digital, seguro-desemprego e FGTS/PIS.
- **ODS 16 — Paz, justiça e instituições eficazes:** democratiza o acesso a informações de serviços públicos, documentação civil e direitos do consumidor.

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
3. Abra a pasta no PyCharm ou VS Code.
4. No terminal, execute:
   ```bash
   python main.py
   ```
Não são necessárias bibliotecas externas.

## 6. Organização em classes
- `Orientacao` (`orientacao.py`): representa um registro da base de conhecimento e possui o método `exibir()`.
- `BaseConhecimento` (`base_conhecimento.py`): carrega o JSON, lista categorias, filtra orientações e realiza a busca com pontuação.
- `Assistente` (`assistente.py`): controla o fluxo de atendimento, validação de privacidade, histórico em JSON, cálculo de indicadores e exportação para CSV.

A composição é aplicada porque o objeto `Assistente` recebe um objeto `BaseConhecimento`, que por sua vez armazena uma lista de objetos `Orientacao`.

## 7. Regra de busca e confiança
A função `normalizar()` converte o texto para minúsculas, remove acentos, pontuação e espaços repetidos, além de aplicar remoção de stopwords e normalização simples de plural (`radical()`):
- Cada palavra-chave encontrada na pergunta vale **3 pontos**.
- Cada palavra da pergunta com 4 letras ou mais que aparece no título vale **1 ponto**.
- **6 pontos ou mais:** confiança ALTA.
- **3 a 5 pontos:** confiança MÉDIA.
- **Menos de 3 pontos:** o sistema informa que não encontrou uma orientação confiável e permite reformular a dúvida ou navegar pelas categorias.

O método `buscar()` retorna uma lista de tuplas `(pontos, orientacao)`, ordenada da maior para a menor pontuação.

## 8. Privacidade e limitações
O programa recusa perguntas contendo `@` ou 8 ou mais dígitos numéricos (mesmo formatados com pontos ou traços, como CPF e telefone) e não registra essas entradas recusadas no histórico. O sistema nunca solicita nome, CPF, telefone ou e-mail. Como limitação, a busca é baseada em regras léxicas e pontuação de palavras-chave (não interpreta semântica profunda fora do vocabulário cadastrado), não substitui atendimento oficial e responde apenas com o conteúdo verificado no arquivo JSON.

## 9. Fontes consultadas
As fontes oficiais e as datas de verificação constam em cada registro de `data/base_conhecimento.json`. Foram consultados portais oficiais do Governo Federal (`gov.br`), Ministério do Trabalho e Emprego, Ministério da Saúde, Ministério da Defesa, Ministério do Desenvolvimento e Assistência Social, Ministério da Justiça e Segurança Pública, Ministério da Educação / INEP, Polícia Federal, Receita Federal e Tribunal Superior Eleitoral (TSE).

## 10. Teste com usuários
Teste realizado com **3 participantes** de fora da equipe, totalizando **11 atendimentos** (sem coleta de nomes ou dados pessoais):
- **Número de participantes:** 3
- **Total de atendimentos:** 11
- **Resposta encontrada (%):** 90,9%
- **Taxa de acerto / ajudou (%):** 90,9%
- **Tempo médio por atendimento:** 23,1 segundos
- **Tentativas médias por atendimento:** 1,5
- **Facilidade média (1 a 5):** 4,7 / 5 (notas: 5, 4 e 5)
- **Dúvidas sem solução:** `"Como fazer a inscrição pro enem"`
- **Melhoria realizada após o teste:** inclusão da palavra-chave `"inscricao pro enem"` e `"enem"` no registro 20 (`Inscrever-se no ENEM, SISU, Prouni ou Fies e emitir ID Estudantil`) da base de conhecimento e adição de preposições coloquiais nas stopwords, garantindo que perguntas formuladas com variações naturais sejam encontradas com confiança alta.

## 11. Integrantes
- Thiago Maluf Hofmann — RM: 569852
- Pedro Yoshikado Garcia — RM: 570449
- Pedro Andreassa Zamai — RM: 569318

## 12. Vídeo técnico
Link do vídeo não listado no YouTube: **PREENCHER**