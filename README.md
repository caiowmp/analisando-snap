# Análise de Redes Complexas: Grafo da Plataforma Bitcoin OTC

Bem-vindo(a) ao repositório do projeto de **Teoria dos Grafos e Redes Complexas**.

Este projeto realiza uma análise estrutural e algorítmica sobre a rede social de confiança da plataforma **Bitcoin OTC**, utilizando conceitos avançados de grafos direcionados e ponderados.

Na rede analisada:

* **Vértices** representam utilizadores da plataforma.
* **Arestas direcionadas** representam avaliações de confiança ou desconfiança entre utilizadores.
* Os pesos das arestas variam de **-10 a +10**, indicando o nível da avaliação atribuída.

---

# 📖 Sobre o Projeto

O arquivo principal (`main.py`) foi desenvolvido para:

* Ler e processar o dataset Bitcoin OTC;
* Aplicar filtros e técnicas de poda da rede;
* Construir grafos direcionados e ponderados;
* Calcular métricas estruturais;
* Avaliar propriedades de redes complexas;
* Executar algoritmos clássicos de grafos;
* Realizar testes de robustez e resiliência.

O objetivo é compreender a estrutura topológica da rede e analisar o comportamento de algoritmos fundamentais da Teoria dos Grafos em um cenário real.

---

# 🎯 Conceitos Estudados

Durante o desenvolvimento do projeto foram explorados os seguintes tópicos:

## Grafos Direcionados e Ponderados

Representação de relações de confiança através de vértices e arestas com direção e peso.

## Small-World Networks (Mundo Pequeno)

Análise de:

* Diâmetro
* Raio
* Comprimento médio dos caminhos
* Coeficiente de clusterização

para verificar a eficiência da propagação de informação na rede.

## Redes Livres de Escala (Scale-Free)

Estudo da distribuição de graus para identificar a presença de hubs altamente conectados e validar comportamentos compatíveis com Lei de Potência.

## Complexidade de Algoritmos

Comparação empírica entre:

* BFS
* DFS
* Tarjan
* Kruskal
* Bellman-Ford
* Floyd-Warshall

utilizando benchmarking estatístico e intervalos de confiança.

## Robustez e Resiliência

Simulações de:

* Falhas aleatórias
* Ataques direcionados por centralidade

para avaliar a resistência da rede à remoção de vértices.

---

# 🚀 Instalação

## Pré-requisitos

* Python 3.8 ou superior

## Dependências

Instale as bibliotecas necessárias:

```bash
pip install igraph matplotlib numpy scipy
```

---

# 📥 Download do Projeto

Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

---

# 📊 Dataset

O projeto utiliza o conjunto de dados:

**Bitcoin OTC Trust Weighted Signed Network**

Arquivo esperado:

```text
soc-sign-bitcoinotc.csv
```

Caso o dataset não esteja incluído no repositório, faça o download através do projeto SNAP (Stanford Network Analysis Project) e coloque o arquivo na raiz do projeto.

Estrutura recomendada:

```text
projeto/
│
├── main.py
├── soc-sign-bitcoinotc.csv
├── README.md
│
└── imgs/
```

Crie a pasta destinada aos gráficos:

```bash
mkdir imgs
```

---

# ▶️ Execução

Após instalar as dependências e posicionar o dataset corretamente:

```bash
python main.py
```

Dependendo das análises habilitadas no método `main()`, a execução pode levar alguns minutos devido ao custo computacional de alguns algoritmos.

---

# 🛠️ Estrutura do Código

## Leitura e Construção do Grafo

### `ler_arquivo(filtrar_arestas=False)`

Responsável por:

* Ler o arquivo CSV;
* Ordenar temporalmente os registros;
* Selecionar os 20% mais recentes (opcional);
* Remover avaliações fracas (|peso| < 5).

### `criar_grafo(arestas, arquivo_gml)`

Cria um grafo direcionado e ponderado utilizando a biblioteca `igraph`.

Se o arquivo `.gml` já existir, ele é carregado diretamente para reduzir o tempo de processamento.

### `gerar_imagem_grafo(grafo, arquivo)`

Gera uma visualização do grafo e salva a imagem em formato PNG.

---

# 📈 Análises Estruturais

## `analisar_grafo(grafo, titulo)`

Calcula métricas fundamentais da rede:

* Número de vértices
* Número de arestas
* Grau mínimo
* Grau máximo
* Grau médio
* Densidade
* Componentes conexas
* Diâmetro
* Raio
* Caminho médio
* Clusterização global

---

## `analisar_distribuicao_grau(grafo, titulo)`

Gera histogramas da distribuição dos graus da rede.

Resultados são exportados em formato PNG.

---

## `analisar_lei_potencia(grafo, titulo)`

Produz gráficos em escala Log-Log para avaliar a aderência da distribuição de graus à Lei de Potência.

---

# ⚙️ Benchmark de Algoritmos

## `analisar_algoritmos(grafo, algoritmo, n_execucoes)`

Executa benchmarks estatísticos para algoritmos clássicos de grafos.

Algoritmos suportados:

* BFS
* DFS
* Verificação Euleriana
* Tarjan
* Kruskal
* Bellman-Ford
* Floyd-Warshall

Métricas calculadas:

* Tempo médio
* Desvio padrão
* Intervalo de confiança de 95%

---

# 🛡️ Robustez e Resiliência

## `analisar_robustez_aleatoria(grafo, percentual)`

Remove vértices aleatoriamente para simular falhas naturais na rede.

Retorna:

* Tamanho da maior componente sobrevivente (`S_rand`)
* Número de componentes resultantes (`C_rand`)

---

## `analisar_robustez_centralidade(grafo, percentual)`

Remove os vértices mais importantes segundo a métrica de Betweenness Centrality.

Retorna:

* Tamanho da maior componente sobrevivente (`S_cent`)
* Número de componentes resultantes (`C_cent`)

---

## `analisar_robustez_total(grafo, n_execucoes)`

Compara:

* Falhas aleatórias
* Ataques direcionados

demonstrando o comportamento típico de redes complexas:

* Alta tolerância a falhas aleatórias;
* Alta vulnerabilidade a ataques direcionados.

---

# 📂 Saídas Geradas

Durante a execução, o projeto pode gerar:

* Gráficos da distribuição de graus;
* Gráficos Log-Log da Lei de Potência;
* Imagens da estrutura da rede;
* Relatórios estatísticos no terminal;
* Resultados dos benchmarks de algoritmos.

Todos os gráficos são armazenados na pasta:

```text
imgs/
```

---

# 📚 Tecnologias Utilizadas

* Python
* igraph
* NumPy
* SciPy
* Matplotlib

---

# 👨‍💻 Autor

Projeto desenvolvido para estudos e aplicações de:

* Teoria dos Grafos
* Redes Complexas
* Análise de Redes Sociais
* Algoritmos em Grafos
* Ciência de Dados
* Sistemas Distribuídos
