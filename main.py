"""LogiRota — Semana 1: persistencia dos pontos, ruas e pedidos.

Execute com: python main.py
"""
from logirota import banco
from logirota.busca import bfs, componentes_conexos, dfs
from logirota.grafo import GrafoLista
from logirota.ponto import Ponto

# Dados iniciais usados somente para popular um banco ainda vazio.
# Depois da primeira inicializacao, a fonte de dados e o SQLite.
PONTOS_INICIAIS = [
    ("Mercado Barra", "Barra", 2, 8),
    ("Farmacia Bela Vista", "Bela Vista", 6, 3),
    ("Oficina Safira", "Safira", 9, 5),
    ("Padaria Distrito", "Distrito", 12, 1),
    ("Loja Boa Familia", "Boa Familia", 14, 0),
    ("Posto Central", "Centro", 5, 5),
    ("Escola Norte", "Zona Norte", 3, 9),
    ("Farmacia Ilha", "Ilha", 25, 25),
]
RUAS_INICIAIS = [
    ("Escola Norte", "Mercado Barra"),
    ("Mercado Barra", "Farmacia Bela Vista"),
    ("Mercado Barra", "Posto Central"),
    ("Farmacia Bela Vista", "Posto Central"),
    ("Posto Central", "Oficina Safira"),
    ("Posto Central", "Padaria Distrito"),
    ("Oficina Safira", "Padaria Distrito"),
    ("Padaria Distrito", "Loja Boa Familia"),
]

def carregar_dados_iniciais_se_necessario():
    """Migra os dados conhecidos apenas se a tabela de pontos estiver vazia."""
    if banco.quantidade_pontos() != 0:
        return
    for ponto in PONTOS_INICIAIS:
        banco.salvar_ponto(ponto)
    for origem, destino in RUAS_INICIAIS:
        banco.salvar_rua(origem, destino)

def carregar_grafo():
    """Reconstrui os objetos de dominio a partir das tuplas retornadas pelo banco."""
    pontos = [Ponto(nome, bairro, x, y) for nome, bairro, x, y in banco.listar_pontos()]
    ruas = banco.listar_ruas()
    grafo = GrafoLista(pontos)
    for origem, destino in ruas:
        grafo.adicionar_rua(origem, destino)
    return pontos, ruas, grafo

def mostrar_pedidos():
    pedidos = banco.listar_pedidos_pendentes()
    print("\nPedidos pendentes:")
    if not pedidos:
        print("  Nenhum pedido pendente.")
    else:
        for identificador, destino, status in pedidos:
            print(f"  #{identificador}: {destino} ({status})")

def cadastrar_pedido():
    pontos = banco.listar_pontos()
    if not pontos:
        print("Nao ha pontos cadastrados.")
        return
    print("\nDestinos disponiveis:")
    for nome, bairro, _x, _y in pontos:
        print(f"  - {nome} ({bairro})")
    destino = input("Digite o nome exato do destino: ").strip()
    if destino not in {p[0] for p in pontos}:
        print("Destino nao encontrado. Nenhum pedido foi cadastrado.")
        return
    identificador = banco.salvar_pedido(destino)
    print(f"Pedido #{identificador} salvo no banco de dados.")

def main():
    banco.inicializar()
    carregar_dados_iniciais_se_necessario()

    while True:
        print("\n=== LogiRota — Semana 1: Persistencia ===")
        print("1 - Mostrar analise da malha (BFS/DFS/conectividade)")
        print("2 - Cadastrar pedido de entrega")
        print("3 - Listar pedidos pendentes")
        print("4 - Listar pontos e vias carregados do banco")
        print("0 - Sair")
        opcao = input("Escolha: ").strip()

        if opcao == "0":
            print("Encerrando. Os dados permanecem salvos em logirota.db.")
            break
        elif opcao == "1":
            pontos, _ruas, grafo = carregar_grafo()
            if not pontos:
                print("Nao ha pontos cadastrados.")
                continue
            origem = "Posto Central" if any(p.nome == "Posto Central" for p in pontos) else pontos[0].nome
            print(f"\nPartindo de '{origem}':")
            print(f"  BFS (fila): {' -> '.join(bfs(grafo, origem))}")
            print(f"  DFS (pilha): {' -> '.join(dfs(grafo, origem))}")
            componentes = componentes_conexos(grafo, [p.nome for p in pontos])
            print(f"\nComponentes conexos da malha ({len(componentes)}):")
            for grupo in componentes:
                print(f"  {{{', '.join(grupo)}}}")
        elif opcao == "2":
            cadastrar_pedido()
        elif opcao == "3":
            mostrar_pedidos()
        elif opcao == "4":
            pontos, ruas, _grafo = carregar_grafo()
            print(f"\nPontos carregados: {len(pontos)}")
            for ponto in pontos:
                print(f"  {ponto.nome} ({ponto.bairro})")
            print(f"Vias carregadas: {len(ruas)}")
            for origem, destino in ruas:
                print(f"  {origem} <-> {destino}")
        else:
            print("Opcao invalida. Tente novamente.")

if __name__ == "__main__":
    main()
