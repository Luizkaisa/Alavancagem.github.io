# Grupo 10
# Luiz Alves Correia Neto – 190083191​
# Jonas de Souza Fagundes – 180076272​
# Daniel Ricardo de Araújo Seguro - 251007430​
# Caio Vitor Martins Souza -   251007108


def preco_liquidacao(entrada, alavancagem, lado, margem_manutencao=0.005):
    if lado == "long":
        return entrada * (1 - 1 / alavancagem + margem_manutencao)
    else:
        return entrada * (1 + 1 / alavancagem - margem_manutencao)


def queda_pra_zerar(alavancagem, margem_manutencao=0.005):
    return (1 / alavancagem - margem_manutencao) * 100


def retorno_com_alavancagem(variacao_pct, alavancagem):
    return variacao_pct * alavancagem


def arbitragem_funding(funding_exchange_a, funding_exchange_b, dias=365):
    diferenca_diaria = (funding_exchange_b - funding_exchange_a) * 3
    return diferenca_diaria * dias


pessoas = [
    ("trader novato, 50x no long",        60000, 50, "long"),
    ("trader mais cauteloso, 5x no long",  60000, 5,  "long"),
    ("trader vendido, 10x no short",       60000, 10, "short"),
]

for nome, entrada, alav, lado in pessoas:
    liq = preco_liquidacao(entrada, alav, lado)
    queda = queda_pra_zerar(alav)
    print(nome)
    print(f"  entrada: {entrada}, alavancagem: {alav}x")
    print(f"  preco de liquidacao: {liq:.0f}")
    print(f"  basta o preco andar {queda:.1f}% contra ele pra zerar a posicao")
    print()

print("se bitcoin sobe 3% num dia:")
for alav in [1, 5, 10, 25, 50]:
    print(f"  {alav:>2}x -> {retorno_com_alavancagem(3, alav):>6.0f}% de retorno sobre a margem")

print()
print("arbitrador de funding rate, sem direcao nenhuma:")
ganho_ano = arbitragem_funding(funding_exchange_a=0.0001, funding_exchange_b=0.0006)
print(f"  captura a diferenca de funding entre duas corretoras")
print(f"  retorno anualizado aproximado: {ganho_ano*100:.1f}%")
print(f"  sem apostar se o preco sobe ou desce")
