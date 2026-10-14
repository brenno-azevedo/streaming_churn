# Análise Exploratória de Churn — Plataforma de Streaming

Análise exploratória completa de uma base de 5.025 assinantes de uma plataforma de
cursos online, da limpeza de dados até quatro frameworks de decisão de negócio —
sem nenhum modelo preditivo.

**Projeto da disciplina _Dados, IA e Negócio_ — Pós-graduação em Data Science e IA (UNIPDS/Anhanguera)**

📓 **[Abrir o notebook](notebooks/01-analise-exploratoria-churn.ipynb)** ·
[Executar no Colab](https://colab.research.google.com/github/brenno-azevedo/streaming_churn/blob/master/notebooks/01-analise-exploratoria-churn.ipynb)

---

## 💼 O problema de negócio

A diretoria de uma plataforma de cursos por assinatura desconfia que o cancelamento
piorou, e ninguém sabe explicar por quê. Foi entregue um extrato de 5.025 clientes,
exportado às pressas de três sistemas diferentes — portanto com inconsistências reais.

Antes de perguntar "que modelo usar", a pergunta é mais básica: **o que existe nesse
dado, o que está errado nele, e o que ele já responde sem modelagem nenhuma.**

## 🔍 O que foi feito

| Etapa | Conteúdo |
|---|---|
| **Análise univariada** | Tipos, valores ausentes, cardinalidade, padronização de categorias e deduplicação |
| **Saneamento** | Consistência lógica entre as quatro colunas de data e tratamento de outliers por tipo |
| **Engenharia de atributos** | Criação de `recencia`, `meses_assinatura` e `receita_acumulada` |
| **Análise bivariada** | Relação de cada variável com o churn, sobre base filtrada por maturidade mínima |
| **Frameworks de decisão** | Coorte de retenção, RFM adaptado, Pareto dos motivos e funil de onboarding |

## 🧹 O que o dado tinha de errado

| Problema | Escala |
|---|---|
| Grafias inconsistentes em `plano` | 8 grafias para 3 planos |
| Grafias inconsistentes em `canal_aquisicao` | 9 grafias para 4 canais |
| Valor curinga `"?"` em `regiao` | 170 registros |
| Erro de escala em `valor_mensal` | 596 registros (~12% da base) |
| Idades impossíveis (−2, 0, 1, 150, 300) | 13 registros |
| Último acesso anterior à assinatura | 1 registro |
| Clientes duplicados | 25 `cliente_id` repetidos |

> **Detalhe que vale registrar:** as duplicatas só ficam visíveis **depois** de padronizar
> as grafias. Antes disso, `duplicated()` encontra apenas 1 linha, porque `"Padrao"` e
> `"Padrão"` não batem como texto. A ordem das etapas de limpeza muda o resultado.

## 📈 Principais achados

[ESCREVA AQUI — três a quatro frases com o que você recomendaria à diretoria.
Os números estão no notebook: o Pareto dos motivos, o gargalo do funil, o que a
coorte mostra sobre as safras recentes e o tamanho do segmento "Em risco" no RFM.]

## ⚠️ Limitações

[ESCREVA AQUI — o que esta análise **não** permite concluir. A distinção entre
descrever, prever e explicar: o Pareto diz qual motivo é mais citado, mas isso não
prova que agir sobre ele reduziria o churn.]

## 🚧 Próximos passos

[ESCREVA AQUI]

---

## 📁 Estrutura do projeto

```
├── README.md
├── requirements.txt
├── notebooks/
│   └── 01-analise-exploratoria-churn.ipynb
├── src/
│   └── exec_univariado.py      # pipeline de limpeza reutilizável
└── reports/
    └── figures/
```

## 🔁 Como reproduzir

O notebook lê os dados diretamente do repositório público da instituição, então **roda
sem nenhuma configuração**. Basta abrir no Colab pelo botão acima e executar tudo.

Para rodar localmente:

```bash
git clone https://github.com/brenno-azevedo/streaming_churn.git
cd streaming_churn
pip install -r requirements.txt
jupyter notebook notebooks/01-analise-exploratoria-churn.ipynb
```

Ou usar só o pipeline de limpeza:

```python
from src.exec_univariado import executar_pipeline
df = executar_pipeline()
```

## 🔒 Sobre os dados

A base é **sintética**, fornecida pelo curso para fins didáticos, e **não é versionada
neste repositório** — o `.gitignore` bloqueia `*.csv` deliberadamente. O notebook lê os
arquivos da fonte pública original, o que mantém a análise reprodutível sem publicar
dado algum aqui.

Nenhuma informação real de cliente é usada ou distribuída neste projeto.

---

**Brenno Azevedo** · [LinkedIn](https://www.linkedin.com/in/) · [GitHub](https://github.com/brenno-azevedo)
