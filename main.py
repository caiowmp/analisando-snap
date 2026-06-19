import csv
import math
import random
import igraph as ig
import matplotlib.pyplot as plt
from pathlib import Path
from statistics import mean
import time
import numpy as np
import scipy.stats as stats
from collections import Counter


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

    vertices = set()

    for source, target, _ in arestas:
        vertices.add(source)
        vertices.add(target)

    vertices = sorted(vertices)

    mapa_vertices = {
        vertice: indice
        for indice, vertice in enumerate(vertices)
    }

    arestas_igraph = []

    for source, target, _ in arestas:
        arestas_igraph.append(
            (
                mapa_vertices[source],
                mapa_vertices[target]
            )
        )

    pesos = [rating for _, _, rating in arestas]

    grafo = ig.Graph(
        n=len(vertices),
        edges=arestas_igraph,
        directed=True
    )

    grafo.vs["id"] = vertices

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
    
    fig, ax = plt.subplots(figsize=(30, 30)) 
    
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
    """
    Calcula e exibe métricas estruturais da rede.
    """

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
    """
    Gera um histograma da distribuição de graus dos vértices.
    """
    
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

def analisar_algoritmos(grafo, algoritmo, n_execucoes):
    """
    Avalia o desempenho de algoritmos clássicos de grafos.
    """    
    
    print("=" * 60)
    print(f"ANÁLISE DE DESEMPENHO: {algoritmo.upper()}".center(60))
    print("=" * 60)

    tempos = []

    algoritmos = {
        "bfs": lambda: grafo.bfs(0),
        "dfs": lambda: grafo.dfs(0),
        "is_eulerian": lambda: grafo.is_connected() and all(grau % 2 == 0 for grau in g.degree()),

        "tarjan": lambda: grafo.connected_components(mode="strong"),

        "kruskal": lambda: grafo.spanning_tree(
            weights=grafo.es["weight"]
        ),

        "bellman_ford": lambda: grafo.distances(
            source=0,
            weights="weight",
            algorithm="bellman_ford"
        ),    

        "floyd_warshall": lambda: grafo.distances(),
    }

    for _ in range(n_execucoes):
        inicio = time.perf_counter()
        
        algoritmos[algoritmo]()        
        
        fim = time.perf_counter()
        tempos.append(fim - inicio)

    media = np.mean(tempos)
    desvio_padrao = np.std(tempos, ddof=1)

    confianca = 0.95
    z_critico = stats.norm.ppf((1 + confianca) / 2)

    margem_erro = z_critico * (
        desvio_padrao / np.sqrt(n_execucoes)
    )

    ic_inferior = media - margem_erro
    ic_superior = media + margem_erro

    print(f"Média de Tempo: {media:.6f} s")
    print(f"Desvio Padrão: {desvio_padrao:.6f} s")
    print(
        f"Intervalo de Confiança (95%): "
        f"[{ic_inferior:.6f}, {ic_superior:.6f}]"
    )

def analisar_lei_potencia(grafo, titulo="ANÁLISE DE LEI DE POTÊNCIA"):
    """
    Analisa a distribuição de graus do grafo e plota o gráfico em escala log-log.
    """

    print("=" * 60)
    print(titulo.center(60))
    print("=" * 60)    
    
    graus = grafo.degree()

    contagem_graus = Counter(graus)
    total_vertices = len(graus)

    lista_k = np.array(list(contagem_graus.keys()))
    frequencias = np.array(list(contagem_graus.values()))
    p_k = frequencias / total_vertices  # Probabilidade P(k)

    mascara = lista_k > 0
    lista_k = lista_k[mascara]
    p_k = p_k[mascara]

    plt.figure(figsize=(8, 5))
    plt.scatter(lista_k, p_k, color='darkblue', alpha=0.7, edgecolors='black', label='Dados da Rede')

    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Grau (k) - Escala Log')
    plt.ylabel('Probabilidade P(k) - Escala Log')
    plt.title('Distribuição de Graus em Escala Log-Log')
    plt.grid(True, which="both", ls="--", alpha=0.5)
    plt.legend()

    if(Path.exists("imgs/distribuicao_graus_loglog.png")):
        print("A imagem da distribuição de graus em escala log-log já existe. Caso queira gerar novamente, por favor, remova o arquivo existente.")
        return
    
    plt.savefig('imgs/distribuicao_graus_loglog.png', dpi=300, bbox_inches='tight')
    # plt.show()

def analisar_robustez_centralidade(grafo, percentual=0.05):
    """
    Simula um ataque direcionado removendo vértices mais centrais.
    """
    
    g = grafo.copy()

    n_remover = math.ceil(g.vcount() * percentual)

    bet = g.betweenness()

    vertices_ordenados = sorted(
        range(g.vcount()),
        key=lambda v: bet[v],
        reverse=True
    )

    vertices_removidos = vertices_ordenados[:n_remover]

    g.delete_vertices(vertices_removidos)

    componentes = g.connected_components(mode="weak")

    S_cent = max(componentes.sizes())
    c_cent = len(componentes)

    return S_cent, c_cent

def analisar_robustez_aleatoria(grafo, percentual=0.05):
    """
    Simula um ataque aleatório removendo vértices de forma aleatória.
    """

    g = grafo.copy()

    n_remover = math.ceil(g.vcount() * percentual)

    vertices_removidos = random.sample(
        range(g.vcount()),
        n_remover
    )

    g.delete_vertices(vertices_removidos)

    componentes = g.connected_components(mode="weak")

    S_rand = max(componentes.sizes())
    c_rand = len(componentes)

    return S_rand, c_rand

def analisar_robustez_total(grafo, n_execucoes=100):
    """
    Compara o impacto de falhas aleatórias e ataques direcionados.
    """

    print("=" * 60)
    print("ANÁLISE DE ROBUSTEZ")
    print("=" * 60)

    
    resultados_rand = []

    for _ in range(n_execucoes):
        S_rand, c_rand = analisar_robustez_aleatoria(grafo)

        resultados_rand.append(
            (S_rand, c_rand)
        )

    S_cent, c_cent = analisar_robustez_centralidade(grafo)

    media_S_rand = mean(
        x[0] for x in resultados_rand
    )

    media_c_rand = mean(
        x[1] for x in resultados_rand
    )

    print(f"S_rand = {media_S_rand:.2f}")
    print(f"c_rand = {media_c_rand:.2f}")

    print(f"S_cent = {S_cent}")
    print(f"c_cent = {c_cent}")

def main():
    """
    Coordena a execução das etapas de construção e análise da rede.
    """

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
    # analisar_grafo(maior_componente_grafo_podado, "Análise estrutural do grafo podado")

    # analisar_distribuicao_grau(grafo, "Distribuição de grau do grafo completo")
    # analisar_distribuicao_grau(maior_componente_grafo_podado, "Distribuição de grau do grafo podado")

    # analisar_algoritmos(maior_componente_grafo_podado, "bfs", 60)
    # analisar_algoritmos(maior_componente_grafo_podado, "dfs", 60)
    # analisar_algoritmos(maior_componente_grafo_podado, "is_eulerian", 60)
    # # Dijkstra não é executado devido a pesos negativos
    # # analisar_algoritmos(maior_componente_grafo_podado, "dijkstra", 1)  
    # analisar_algoritmos(maior_componente_grafo_podado, "tarjan", 60)
    # analisar_algoritmos(maior_componente_grafo_podado, "kruskal", 60)

    # # bellman_ford encontrou ciclo negativo 
    # # analisar_algoritmos(maior_componente_grafo_podado, "bellman_ford", 15)
    # analisar_algoritmos(maior_componente_grafo_podado, "floyd_warshall", 60)

    # analisar_lei_potencia(maior_componente_grafo_podado, "Análise de Lei de Potência do grafo podado")

    analisar_robustez_total(maior_componente_grafo_podado)
    


if __name__ == "__main__":
    main()