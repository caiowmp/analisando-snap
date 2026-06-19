import csv
import igraph as ig
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean

ARQUIVO = "soc-sign-bitcoinotc.csv"

def ler_arquivo(filtrar_arestas=False):
    """
    Lê o arquivo CSV e retorna uma lista de arestas no formato:
    (source, target, rating)
    """
    
    arestas = []

    if(Path("grafo_original.gml").exists() and Path("grafo_podado.gml").exists()):
        print("Grafo já existe. Não é necessário ler o arquivo CSV novamente.")
        return arestas

    with open(ARQUIVO, mode="r", encoding="utf-8") as csvfile:
        leitor = csv.reader(csvfile)

        for linha in leitor:
            arestas.append(
                (
                    int(linha[0]),  # source
                    int(linha[1]),  # target
                    int(linha[2]),  # rating
                    float(linha[3]) # timestamp
                )
            )

    if filtrar_arestas:
        arestas_ordenadas = sorted(
            arestas,
            key=lambda x: x[3]  # timestamp
        )
        indice = int(len(arestas_ordenadas) * 0.8)
        arestas_recentes = arestas_ordenadas[indice:]
        arestas_recentes = [
            (source, target, rating)
            for source, target, rating, timestamp in arestas_recentes
            if abs(rating) >= 5
        ]     
        return arestas_recentes  

    return arestas


def criar_grafo(arestas, arquivo_gml="grafo_original.gml"):
    """
    Cria um grafo direcionado e ponderado utilizando igraph.
    """

    if(Path(arquivo_gml).exists()):
        print("Grafo já existe. Carregando grafo do arquivo...")
        grafo = ig.Graph.Read_GML(arquivo_gml)
        return grafo

    # Conjunto de todos os vértices
    vertices = set()

    for source, target, _ in arestas:
        vertices.add(source)
        vertices.add(target)

    vertices = sorted(vertices)

    # Mapeamento:
    # id original -> índice interno do igraph
    mapa_vertices = {
        vertice: indice
        for indice, vertice in enumerate(vertices)
    }

    # Converte as arestas para índices do igraph
    arestas_igraph = []

    for source, target, _ in arestas:
        arestas_igraph.append(
            (
                mapa_vertices[source],
                mapa_vertices[target]
            )
        )

    pesos = [rating for _, _, rating in arestas]

    # Criação do grafo
    grafo = ig.Graph(
        n=len(vertices),
        edges=arestas_igraph,
        directed=True
    )

    # Guarda o ID original de cada vértice
    grafo.vs["id"] = vertices

    # Guarda o peso de cada aresta
    grafo.es["weight"] = pesos

    grafo.save(arquivo_gml)

    return grafo

def gerar_imagem_grafo(grafo, arquivo):
    """
    Gera uma imagem do grafo utilizando igraph.
    """

    if(Path(arquivo).exists()):
        print(f"A imagem já existe {arquivo}. Caso queira gerar novamente, por favor, remova o arquivo existente.")
        return
    

    # fig, ax = plt.subplots(figsize=(50, 50))  # Tamanho da figura em polegadas
    fig, ax = plt.subplots(figsize=(30, 30))  # Tamanho da figura em polegadas
    
    layout = grafo.layout("fr")
    layout.scale(10)
    ig.plot(
        grafo,
        target=ax,
        layout=layout, 
        vertex_size= 5,
        vertex_color="black",
        vertex_frame_width=4.0,
        vertex_frame_color="gray",
        vertex_label=None,
        vertex_label_size=4.0,
        edge_width=0.3,
        edge_color="black",
        edge_label=grafo.es["weight"],
        edge_label_size=5)

    fig.savefig(
    arquivo,
    dpi=600,
    bbox_inches="tight"
    )

def analisar_grafo(grafo, titulo="ANÁLISE ESTRUTURAL DO GRAFO"):
    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)

    # Informações básicas
    num_vertices = grafo.vcount()
    num_arestas = grafo.ecount()

    print(f"Número de vértices: {num_vertices}")
    print(f"Número de arestas : {num_arestas}")

    # Graus
    graus = grafo.degree()

    print("\n--- Graus ---")
    print(f"Grau mínimo : {min(graus)}")
    print(f"Grau máximo : {max(graus)}")
    print(f"Grau médio  : {mean(graus):.2f}")

    # Densidade
    print("\n--- Densidade ---")
    print(f"Densidade: {grafo.density():.6f}")

    # Componentes
    print("\n--- Componentes Conexas ---")

    componentes = grafo.connected_components(mode="weak")

    print(f"Número de componentes: {len(componentes)}")

    tamanhos = componentes.sizes()

    for i, tamanho in enumerate(tamanhos):
        print(f"Componente {i+1}: {tamanho} vértices")

    # Métricas de distância
    print("\n--- Distâncias ---")

    try:
        diametro = grafo.diameter(directed=False)
        raio = grafo.radius(mode="all")
        caminho_medio = grafo.average_path_length(
            directed=False
        )

        print(f"Diâmetro                 : {diametro}")
        print(f"Raio                     : {raio}")
        print(f"Comprimento médio caminho: {caminho_medio:.4f}")

    except Exception as e:
        print(f"Erro ao calcular distâncias: {e}")

    # Clusterização
    print("\n--- Clusterização ---")

    try:
        clustering = grafo.transitivity_undirected()

        print(
            f"Coeficiente de clusterização global: "
            f"{clustering:.6f}"
        )

    except Exception as e:
        print(f"Erro ao calcular clusterização: {e}")

    # Triângulos
    print("\n--- Triângulos ---")

    try:
        triangulos = grafo.list_triangles()

        print(f"Número de triângulos: {len(triangulos)}")

    except Exception as e:
        print(f"Erro ao calcular triângulos: {e}")

    print("=" * 60)

def analisar_distribuicao_grau(grafo, titulo="DISTRIBUIÇÃO DE GRAU"):
    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)

    plt.figure(figsize=(10, 6))
    plt.hist(grafo.degree(), bins=30, edgecolor='black', alpha=0.7)
    plt.title("Distribuição de Graus do Grafo")
    plt.xlabel("Grau")
    plt.ylabel("Frequência (Quantidade de Nós)")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    if(Path.exists("imgs/distribuicao_grau.png")):
        print("A imagem da distribuição de grau já existe. Caso queira gerar novamente, por favor, remova o arquivo existente.")
        return
    plt.savefig("imgs/distribuicao_grau.png", dpi=300, bbox_inches="tight")

def main():
    arestas = ler_arquivo()

    grafo = criar_grafo(arestas, "grafo_original.gml")
    gerar_imagem_grafo(grafo, "imgs/grafo_completo.png")

    # maior_componente_grafo_completo = grafo.connected_components(mode="weak").giant()
    # gerar_imagem_grafo(maior_componente_grafo_completo, "imgs/grafo_completo_maior_componente.png")

    arestas_filtradas = ler_arquivo(filtrar_arestas=True)
    grafo_podado = criar_grafo(arestas_filtradas, "grafo_podado.gml")
    gerar_imagem_grafo(grafo_podado, "imgs/grafo_podado.png")

    maior_componente_grafo_podado = grafo_podado.connected_components(mode="weak").giant()
    # gerar_imagem_grafo(maior_componente_grafo_podado, "imgs/grafo_podado_maior_componente.png")

    # analisar_grafo(grafo, "Análise do grafo completo")
    analisar_grafo(maior_componente_grafo_podado, "Análise estrutural do grafo podado")

    # analisar_distribuicao_grau(grafo, "Distribuição de grau do grafo completo")
    # analisar_distribuicao_grau(maior_componente_grafo_podado, "Distribuição de grau do grafo podado")


if __name__ == "__main__":
    main()