# Bitcoiners que Vivem de Alavancagem

### Entendendo os riscos da alavancagem e como simular cenários de liquidação e arbitragem

**Tópicos Avançados em Engenharia — Universidade de Brasília (UnB)**

### Grupo 10

| Integrante | Matrícula |
|---|---|
| Luiz Alves Correia Neto | 190083191 |
| Jonas de Souza Fagundes | 180076272 |
| Daniel Ricardo de Araújo Seguro | 251007430 |
| Caio Vitor Martins Souza | — |

## Acessos para Apresentação e GitHub Pages

Apresentação:

[<img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSFeong-WYsEuq40MIoV-QWMaYM2UVp4DpYP6kdFq2wiNhfMDozG02jvJg&s=10" width="125"/>](https://unbbr-my.sharepoint.com/:p:/g/personal/190083191_aluno_unb_br/IQBIgUEoBlVsSLnCH6e-wQrTAZzq-LZZrRB9xPHpLBueXBg?e=2sDguR)

GitHub Pages:

[<img src="https://s18955.pcdn.co/wp-content/uploads/2018/02/github.png" width="100"/>](https://luizkaisa.github.io/Alavancagem/)

---

## Resumo

Os contratos futuros perpétuos concentram hoje parcela expressiva do volume negociado no mercado de Bitcoin e permitem, por meio da alavancagem, controlar posições muito maiores do que o capital efetivamente depositado. Esse mecanismo amplifica ganhos e perdas na mesma proporção e introduz o risco de liquidação forçada, pouco compreendido por operadores iniciantes. Este trabalho apresenta os fundamentos das operações alavancadas — margem, preço de liquidação e taxa de financiamento (*funding rate*) — e propõe um simulador em Python que quantifica esses conceitos em cenários práticos. Os resultados mostram que a distância até a liquidação decresce de forma acentuada com o aumento da alavancagem (19,5% de movimento contrário a 5x contra apenas 1,5% a 50x) e que estratégias neutras de arbitragem de *funding rate* apresentam perfil de risco fundamentalmente distinto da especulação direcional, com retorno independente da direção do preço. Conclui-se que ferramentas educacionais quantitativas contribuem para decisões mais conscientes em mercados de derivativos de criptomoedas.

**Palavras-chave:** Bitcoin; contratos perpétuos; alavancagem; liquidação; funding rate; arbitragem.

---

## 1. Introdução

O mercado de derivativos de Bitcoin tornou-se um dos segmentos mais movimentados do ecossistema de criptomoedas, superando em volume o próprio mercado à vista. Entre seus principais instrumentos estão os **contratos futuros perpétuos** (*perpetual futures*, ou *perps*), que permitem negociar a variação do preço do Bitcoin sem a posse do ativo, utilizando apenas uma fração do capital como garantia.

Esse mecanismo, conhecido como **alavancagem**, aumenta significativamente tanto o potencial de lucro quanto o risco de perdas. Corretoras oferecem alavancagens superiores a 100x a qualquer usuário de varejo, enquanto estudos de mercado apontam que mais de 75% dos operadores alavancados de varejo perdem dinheiro no longo prazo — em grande parte por não visualizarem quantitativamente o próprio risco.

Este trabalho tem dois objetivos: **(i)** apresentar de forma acessível os fundamentos das operações alavancadas — margem, liquidação e *funding rate* — e **(ii)** demonstrar esses conceitos por meio de um simulador em Python que calcula preço de liquidação, distância até a liquidação, retorno alavancado e o rendimento de uma estratégia neutra de arbitragem de *funding rate*.

---

## 2. Fundamentação Teórica

### 2.1 Contratos futuros perpétuos

Um contrato perpétuo é um derivativo que replica a variação do preço do ativo subjacente **sem data de vencimento**, diferentemente dos futuros tradicionais. O operador não compra Bitcoin: ele deposita uma garantia (**margem**) e assume uma posição comprada (*long*) ou vendida (*short*) sobre o preço. Introduzidos pela BitMEX em 2016, os perpétuos tornaram-se o instrumento dominante de negociação especulativa de criptomoedas (Coinbase Learn; crypto.news).

### 2.2 Alavancagem e margem

A alavancagem `L` é a razão entre o tamanho da posição e a margem depositada:

```
posição = margem × L
```

Com US$ 1.000 de margem e alavancagem de 10x, o operador controla uma posição de US$ 10.000. Toda variação percentual do preço incide sobre a **posição total**, mas é absorvida pela **margem** — daí o efeito multiplicador. No exemplo clássico da Coinbase Learn: se o Bitcoin sobe 5%, a posição ganha US$ 500, o que representa **+50% sobre a margem**; se cai 5%, a perda é igualmente de 50%. A alavancagem não cria retorno: ela amplifica o resultado nas duas direções.

### 2.3 Margem de manutenção e liquidação

A corretora exige que uma fração mínima da posição — a **margem de manutenção** (`mm`, tipicamente entre 0,4% e 1% para Bitcoin) — permaneça sempre coberta. Quando as perdas acumuladas reduzem a margem abaixo desse mínimo, ocorre a **liquidação**: a corretora encerra a posição à força e o operador perde a margem.

A distância até a liquidação pode ser derivada diretamente. Para uma posição *long* com alavancagem `L`, uma queda de fração `x` no preço gera perda de `margem × L × x`. A liquidação ocorre quando a margem restante iguala a exigência de manutenção:

```
1 − L·x = mm·L   ⇒   x = 1/L − mm
```

Ou seja, o movimento contrário que zera a posição é `(1/L − mm)`, e o preço de liquidação é:

```
long:  P_liq = entrada × (1 − 1/L + mm)
short: P_liq = entrada × (1 + 1/L − mm)
```

A consequência prática é geométrica: com 10x, a margem representa 10% da posição e uma queda de ~9,5% já a elimina; com 50x, a margem é apenas 2% da posição e **1,5% de movimento contrário é suficiente** — oscilação que o Bitcoin frequentemente apresenta em poucas horas.

### 2.4 Funding rate

O *funding rate* é o mecanismo que mantém o preço do contrato perpétuo ancorado ao preço à vista. Periodicamente — em geral a cada 8 horas, portanto **3 vezes ao dia** — há uma transferência entre comprados e vendidos: quando o perpétuo negocia acima do preço à vista (demanda compradora excessiva), os *longs* pagam os *shorts*, incentivando o reequilíbrio; quando negocia abaixo, o fluxo se inverte (MetaMask News; crypto.news). Cada corretora calcula sua própria taxa a partir do seu livro de ofertas, e as taxas **divergem entre corretoras**.

### 2.5 Arbitragem de funding rate

Essa divergência cria uma oportunidade de estratégia **neutra em direção** (*delta-neutral*): o operador mantém, simultaneamente e no mesmo tamanho, uma posição comprada na corretora de *funding* menor e uma vendida na corretora de *funding* maior. A exposição ao preço se cancela — se o Bitcoin sobe, ganha-se de um lado e perde-se do outro — e o lucro provém exclusivamente da **diferença entre as taxas de funding**, recebida a cada período. Segundo dados de mercado (Convex Research), operações desse tipo chegam a render entre 15% e 40% ao ano em períodos de alta volatilidade. O perfil de risco é fundamentalmente distinto da especulação direcional: retorno menor por operação, porém previsível e independente da direção do preço.

---

## 3. O Problema

Grande parte dos novos participantes do mercado de criptomoedas passa a operar com níveis elevados de alavancagem sem compreender completamente os riscos envolvidos. Embora corretoras ofereçam alavancagens superiores a 100x, poucos investidores conseguem visualizar:

- qual será seu **preço de liquidação**;
- quanto o mercado precisa variar para que **toda a margem seja perdida**;
- como a alavancagem **multiplica ganhos e perdas** simetricamente;
- como estratégias neutras, como a **arbitragem de funding rate**, diferem da especulação direcional.

Essa lacuna de compreensão faz com que muitos operadores sejam liquidados rapidamente, contribuindo para as elevadas taxas de perda observadas entre investidores de varejo.

---

## 4. Relevância para o Ecossistema Bitcoin

A negociação de contratos perpétuos representa atualmente parcela significativa do volume financeiro do mercado de Bitcoin. Além de especuladores, utilizam derivativos: operadores de **proteção (hedge)**, **formadores de mercado**, **arbitradores entre corretoras** e **estratégias quantitativas**.

Compreender o funcionamento da alavancagem é relevante porque ela influencia diretamente:

- a **volatilidade** do mercado;
- os eventos de **liquidação em cascata** — quando quedas de preço liquidam posições em massa, forçando vendas que aprofundam a queda e liquidam ainda mais posições;
- a **estabilidade das bolsas** de derivativos;
- o **gerenciamento de risco** de todos os participantes.

Ferramentas educacionais que permitam visualizar esses efeitos ajudam novos usuários a tomar decisões mais conscientes e reduzem erros decorrentes do desconhecimento desses mercados.

---

## 5. Metodologia: o Simulador

Foi desenvolvido um simulador em Python (`alavancagem.py`), sem dependências externas, que implementa os quatro cálculos centrais de uma operação alavancada:

| Função | Fórmula | Pergunta que responde |
|---|---|---|
| `preco_liquidacao(entrada, L, lado, mm)` | *long*: `entrada × (1 − 1/L + mm)` · *short*: `entrada × (1 + 1/L − mm)` | Em que preço a corretora encerra a posição? |
| `queda_pra_zerar(L, mm)` | `(1/L − mm) × 100` | Quantos % de movimento contrário zeram a margem? |
| `retorno_com_alavancagem(var%, L)` | `var% × L` | Qual o resultado sobre a margem? |
| `arbitragem_funding(fA, fB, dias)` | `(fB − fA) × 3 × dias` | Quanto rende a arbitragem no período? |

Parâmetros adotados: margem de manutenção padrão de **0,5%** (valor típico para BTC em grandes corretoras) e **3 pagamentos de funding por dia** (períodos de 8 horas). Todos os parâmetros são configuráveis, permitindo explorar diferentes preços de entrada, níveis de alavancagem e cenários de arbitragem.

O simulador compara quatro perfis de operadores: um trader novato a 50x (*long*), um trader cauteloso a 5x (*long*), um trader vendido a 10x (*short*) e um arbitrador de *funding rate* sem exposição direcional.

---

## 6. Resultados

### 6.1 Preço de liquidação e distância até a liquidação

Para entrada a US$ 60.000, o simulador produz:

```
trader novato, 50x no long
  preco de liquidacao: 59100
  basta o preco andar 1.5% contra ele pra zerar a posicao

trader mais cauteloso, 5x no long
  preco de liquidacao: 48300
  basta o preco andar 19.5% contra ele pra zerar a posicao

trader vendido, 10x no short
  preco de liquidacao: 65700
  basta o preco andar 9.5% contra ele pra zerar a posicao
```

A relação entre alavancagem e distância até a liquidação evidencia o crescimento acelerado do risco:

| Alavancagem | Movimento contrário que zera a posição |
|-------------|----------------------------------------:|
| 5x   | 19,5% |
| 10x  | 9,5%  |
| 25x  | 3,5%  |
| 50x  | 1,5%  |
| 100x | 0,5%  |

Mesma direção e mesma entrada: a única diferença entre os perfis é a alavancagem — e ela determina se o operador sobrevive a uma correção normal de mercado ou é liquidado por ruído de curto prazo.

### 6.2 Retorno alavancado

Se o Bitcoin varia +3% em um dia:

| Alavancagem | Retorno sobre a margem |
|-------------|-----------------------:|
| 1x  | 3%   |
| 5x  | 15%  |
| 10x | 30%  |
| 25x | 75%  |
| 50x | 150% |

É esse número que atrai o operador iniciante — mas o mesmo mecanismo atua simetricamente nas perdas, e é ele que o liquida.

### 6.3 Arbitragem de funding rate

Com *funding* de 0,01% por período na corretora A e 0,06% na corretora B (diferença de 0,05% por período, paga 3 vezes ao dia):

```
arbitrador de funding rate, sem direcao nenhuma:
  captura a diferenca de funding entre duas corretoras
  retorno anualizado aproximado: 54.7%
  sem apostar se o preco sobe ou desce
```

O valor de 54,7% ao ano assume que a diferença de *funding* se mantém constante — um teto otimista; a faixa observada em dados de mercado é de 15% a 40% ao ano (Convex Research). Ainda assim, o contraste com a especulação direcional é evidente: o retorno independe da direção do preço e não há risco de liquidação por movimento de mercado enquanto as duas pernas permanecerem balanceadas.

---

## 7. Discussão e Limitações

Os resultados quantificam a assimetria central do mercado de perpétuos: a alavancagem alta transforma a operação em uma aposta de curtíssimo prazo contra a volatilidade natural do ativo (a 50x, o operador aposta que o Bitcoin não oscila 1,5% — aposta quase impossível de vencer repetidamente), enquanto a estratégia neutra converte o mesmo instrumento em fonte de renda previsível.

O simulador é deliberadamente simplificado, com finalidade educacional. Não são modelados:

- **custos operacionais** (taxas de negociação, *slippage*, spread entre corretoras);
- **variação temporal do funding rate**, que oscila e pode inverter de sinal;
- **risco de contraparte** (falência ou indisponibilidade de corretora), relevante na arbitragem que exige capital em duas plataformas;
- **fórmulas exatas de liquidação** de cada corretora, que variam conforme o tipo de margem (isolada ou cruzada) e o tamanho da posição.

Essas simplificações não comprometem o objetivo do trabalho — tornar visíveis as ordens de grandeza do risco — mas indicam que os valores não devem ser usados como previsão de resultado real.

---

## 8. Trabalhos Futuros

A aplicação pode ser expandida para incluir: custos operacionais e *slippage*; volatilidade histórica do Bitcoin para estimar a **probabilidade de liquidação** em dado horizonte; modelos probabilísticos (simulação de Monte Carlo); e integração com **dados reais de corretoras** via API para acompanhar *funding rates* ao vivo — tornando-se um instrumento ainda mais útil para estudo e treinamento de estratégias em mercados de derivativos de Bitcoin.

---

## 9. Conclusão

A alavancagem não é intrinsecamente boa ou má: é um multiplicador que exige gerenciamento rigoroso de risco. O simulador desenvolvido transforma conceitos frequentemente abstratos — margem, liquidação, *funding* — em exemplos quantitativos de fácil compreensão, mostrando que a diferença entre "viver de alavancagem" e ser liquidado não está em prever o preço, e sim em **controlar a distância até a própria liquidação** — ou em nem depender de direção, como faz o arbitrador de *funding rate*.

---

## Como Executar

O simulador não possui dependências externas — basta Python 3:

```bash
python alavancagem.py
```

O código-fonte (`alavancagem.py`) implementa todas as funções utilizadas nas simulações e pode ser facilmente adaptado para diferentes cenários de negociação, níveis de alavancagem, preços de entrada e estratégias de arbitragem.

---

## Referências

- Coinbase Learn — *What are Perpetual Futures?*
- MetaMask News — *Understanding leverage and margin in perpetual futures trading*
- Convex Research — *BTC Perpetual Funding Rates*
- crypto.news — *What are perpetual futures? Perps, funding rates, and liquidations explained*
