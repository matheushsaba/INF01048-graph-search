from typing import Iterable, Set, Tuple
import numpy as np
import heapq

class DadosSolucaoPuzzle:
    estado_final = "12345678_"
    matriz_estado_final = np.array([['1','2','3'],['4','5','6'],['7','8','_']])
    valor_posicao_estado_final = None

    @staticmethod
    def gera_dicionario_estado_final():
        """
        Gera e retorna um dicionário dos valores finais para uma tupla com suas posições
        :return: dict
        """
        dicionario_matriz_estado_final = {}

        for i in range(len(DadosSolucaoPuzzle.matriz_estado_final)):                                   
            for j in range(len(DadosSolucaoPuzzle.matriz_estado_final[i])):
                dicionario_matriz_estado_final[DadosSolucaoPuzzle.matriz_estado_final[i][j]] = (i, j)
        
        DadosSolucaoPuzzle.valor_posicao_estado_final = dicionario_matriz_estado_final 

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado:str, pai, acao:str, custo:int):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __str__(self):
        estado = self.estado
        pai = self.pai.estado if self.pai else "raiz"
        acao = self.acao if self.acao else "raiz"
        custo = self.custo
        return f"Nodo (estado: {estado}, pai: {pai}, acao: {acao}, custo: {custo})"
    
    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, Nodo):
            return self.estado == __value.estado
        return False
    
    def __hash__(self) -> int:
        return hash(self.estado)
    
    

def sucessor(estado:str)->Set[Tuple[str,str]]:
    """
    Recebe um estado (string) e retorna um conjunto de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    # Posições do tabuleiro no formato string
    # 0 1 2
    # 3 4 5
    # 6 7 8

    # Posições do tabuleiro no formato matriz
    # 00 01 02
    # 10 11 12
    # 20 21 22

    possiveis_acoes = pega_acoes_possiveis(estado)
    acoes_e_estados = []

    for acao in possiveis_acoes:
        novo_estado = altera_estado(estado, acao)
        tupla_acao_estado = (acao, novo_estado)
        acoes_e_estados.append(tupla_acao_estado)
    
    return acoes_e_estados

def pega_acoes_possiveis(estado:str)->list[str]:
    """
    Recebe um estado (string) e retorna uma lista de ações possíveis
    :param estado: str
    :return: list[str]
    """
    # Inicializa o conjunto de ações possíveis
    possiveis_acoes = ['acima', 'esquerda', 'abaixo', 'direita']
    tabuleiro = estado_string_para_matriz(estado)
    posicao_vazia = np.where(tabuleiro == '_')
    linha_posicao_vazia = posicao_vazia[0]
    coluna_posicao_vazia = posicao_vazia[1]

    # Remove as ações que não são possíveis
    if (linha_posicao_vazia == 0):
        possiveis_acoes.remove('acima')
    if (coluna_posicao_vazia == 0):
        possiveis_acoes.remove('esquerda')
    if (linha_posicao_vazia == 2):
        possiveis_acoes.remove('abaixo')
    if (coluna_posicao_vazia == 2):
        possiveis_acoes.remove('direita')

    return possiveis_acoes

def estado_string_para_matriz(estado:str)->np.array:
    """
    Recebe um estado (string) e retorna um numpy array 3x3 com o estado
    :param estado: str
    :return: np.array
    """
    # Separa o estado do tabuleiro em 3 linhas ['123', '456', '789']
    linhas_do_tabuleiro = [estado[i:i+3] for i in range(0, len(estado), 3)] 
    tabuleiro = np.empty((3, 3), dtype=str)

    for linha_do_tabuleiro in linhas_do_tabuleiro:
        for elemento in linha_do_tabuleiro:
            index_linha = linhas_do_tabuleiro.index(linha_do_tabuleiro)
            index_coluna = linha_do_tabuleiro.index(elemento)
            tabuleiro[index_linha][index_coluna] = elemento

    return tabuleiro

def altera_estado(estado:str, acao:str)->str:
    """
    Recebe um estado (string) e uma ação (string) e retorna o estado resultante apos
    mover o espaço vazio na direção da ação.
    :param estado: str
    :param acao: str
    :return: str
    """
    tabuleiro = estado_string_para_matriz(estado)
    tabuleiro_resultante = mover_vazio_na_matriz(tabuleiro, acao)

    return estado_matriz_para_string(tabuleiro_resultante)

def mover_vazio_na_matriz(tabuleiro:np.array, acao:str)->np.array:
    """
    Recebe um tabuleiro (matriz) e uma ação (string) e retorna o tabuleiro resultante apos
    mover o espaço vazio na direção da ação.
    :param tabuleiro: np.array
    :param acao: str
    :return: np.array
    """
    posicao_vazia = np.where(tabuleiro == '_')
    linha_posicao_vazia = posicao_vazia[0]
    coluna_posicao_vazia = posicao_vazia[1]

    if (acao == 'acima'):
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia] = tabuleiro[linha_posicao_vazia - 1, coluna_posicao_vazia]
        tabuleiro[linha_posicao_vazia - 1, coluna_posicao_vazia] = '_'

    if (acao == 'esquerda'):
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia] = tabuleiro[linha_posicao_vazia, coluna_posicao_vazia - 1]
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia - 1] = '_'

    if (acao == 'abaixo'):
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia] = tabuleiro[linha_posicao_vazia + 1, coluna_posicao_vazia]
        tabuleiro[linha_posicao_vazia + 1, coluna_posicao_vazia] = '_'

    if (acao == 'direita'):
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia] = tabuleiro[linha_posicao_vazia, coluna_posicao_vazia + 1]
        tabuleiro[linha_posicao_vazia, coluna_posicao_vazia + 1] = '_'

    return tabuleiro

def estado_matriz_para_string(tabuleiro:np.array)->str:
    """
    Recebe um estado (matriz) e retorna um string
    :param estado: np.array
    :return: str
    """
    return ''.join(tabuleiro.flatten().tolist())

def expande(nodo:Nodo)->Set[Nodo]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um conjunto de nodos.
    Cada nodo do conjunto é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    acoes_e_estados_possiveis = sucessor(nodo.estado)

    sucessores = set()
    for acao, estado in acoes_e_estados_possiveis:
        nodo_sucessor = Nodo(estado, nodo, acao, nodo.custo + 1)
        sucessores.add(nodo_sucessor)

    return sucessores

def astar_hamming(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # Seguindo a nomenclatura de variáveis descrita no exercício nos comentários
    estados_explorados = set()                                          # conjunto de estados explorados X
    nodo_raiz = Nodo(estado, None, None, 0)                             # estado inicial s
    custo_hamming = funcao_de_custo_hamming(nodo_raiz)                  # custo de h(v) para o estado inicial
    heap_id = 0                                                         # id para cada valor da heap ser único
    tupla_custo_hamming_nodo = (custo_hamming, heap_id, nodo_raiz)
    fronteira = []                                                      # inicialização da fronteira F
    heapq.heappush(fronteira, tupla_custo_hamming_nodo)
    nodos_expandidos = 0

    while len(fronteira) != 0:                                          # enquanto houver nodos na fronteira
        tupla_custo_hamming_nodo = fronteira[0]
        heapq.heappop(fronteira)
        nodo_fronteira = tupla_custo_hamming_nodo[2]                    # pega o primeiro nodo v da fronteira

        if nodo_fronteira.estado == DadosSolucaoPuzzle.estado_final:    # se o estado do nodo é o estado final, retorna o caminho percorrido
            return trilha_de_estados_a_partir_da_raiz(nodo_fronteira)
        
        estados_explorados.add(nodo_fronteira.estado)                   # adiciona o estado aos explorados
        nodos_vizinhos = expande(nodo_fronteira)                        # expande o nodo e retorna os vizinhos
        nodos_expandidos += 1                                           # atualiza o contados de nós expandidos

        for vizinho in nodos_vizinhos:                                  # para cada vizinho u do nodo
            if vizinho.estado not in estados_explorados:                # se o vizinho não estiver nos nodos já explorados
                custo_hamming = funcao_de_custo_hamming(vizinho)        # calcula o custo de hamming do vizinho
                heap_id += 1                                            # cria o id único do heap para o vizinho
                tupla_custo_hamming_nodo = (custo_hamming, heap_id, vizinho)
                heapq.heappush(fronteira, tupla_custo_hamming_nodo)     # adiciona o vizinho a fronteira                     

    return None                                                         # retorna falha

def trilha_de_estados_a_partir_da_raiz(nodo:Nodo)->list[str]:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna uma lista de ações que leva do
    nodo raiz até o nodo de entrada.
    :param nodo: objeto da classe Nodo
    :return: list[str]
    """
    trilha = []
    nodo_atual = nodo

    while nodo_atual.pai != None:         # faz um loop que pega o pai dos nodos até chegar na raiz
        acao_atual = nodo_atual.acao
        trilha.insert(0, acao_atual)      # salva o valor da ação na trilha
        nodo_atual = nodo_atual.pai       # atualiza o valor atual do nodo para o pai do nodo analizado

    return trilha

def funcao_de_custo_hamming(nodo:Nodo)->int:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um inteiro com o valor da função de custo.
    :param nodo: objeto da classe Nodo
    :return: int
    """
    custo = nodo.custo + distancia_hamming(nodo.estado)
    return custo

def distancia_hamming(estado:str)->int:
    """
    Recebe um estado (string) e retorna a distância de Hamming calculada a partir das distâncias dos dígitos
    :param estado: str
    :return: int
    """
    distancia = 0

    if estado == DadosSolucaoPuzzle.estado_final:              # se o estado for o final, a distância é 0
        return distancia
    
    for i in range(len(estado)):                               # senão verifica se cada dígito é diferente do estado final
        if estado[i] != DadosSolucaoPuzzle.estado_final[i]:
            distancia += 1

    return distancia

def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # Seguindo a nomenclatura de variáveis descrita no exercício nos comentários
    estados_explorados = set()                                          # conjunto de estados explorados X
    nodo_raiz = Nodo(estado, None, None, 0)                             # estado inicial s
    custo_manhattan = funcao_de_custo_manhattan(nodo_raiz)              # custo de h(v) para o estado inicial
    heap_id = 0                                                         # id para cada valor da heap ser único
    tupla_custo_manhattan_nodo = (custo_manhattan, heap_id, nodo_raiz)
    fronteira = []                                                      # inicialização da fronteira F
    heapq.heappush(fronteira, tupla_custo_manhattan_nodo)
    nodos_expandidos = 0

    while len(fronteira) != 0:                                          # enquanto houver nodos na fronteira
        tupla_custo_manhattan_nodo = fronteira[0]
        heapq.heappop(fronteira)
        nodo_fronteira = tupla_custo_manhattan_nodo[2]                  # pega o primeiro nodo v da fronteira

        if nodo_fronteira.estado == DadosSolucaoPuzzle.estado_final:    # se o estado do nodo é o estado final, retorna o caminho percorrido
            return trilha_de_estados_a_partir_da_raiz(nodo_fronteira)
        
        estados_explorados.add(nodo_fronteira.estado)                   # adiciona o estado aos explorados
        nodos_vizinhos = expande(nodo_fronteira)                        # expande o nodo e retorna os vizinhos
        nodos_expandidos += 1                                           # atualiza o contados de nós expandidos

        for vizinho in nodos_vizinhos:                                  # para cada vizinho u do nodo
            if vizinho.estado not in estados_explorados:                # se o vizinho não estiver nos nodos já explorados
                custo_manhattan = funcao_de_custo_manhattan(vizinho)    # calcula o custo de hamming do vizinho
                heap_id += 1                                            # cria o id único do heap para o vizinho
                tupla_custo_manhattan_nodo = (custo_manhattan, heap_id, vizinho)
                heapq.heappush(fronteira, tupla_custo_manhattan_nodo)   # adiciona o vizinho a fronteira                     

    return None                                                         # retorna falha

def funcao_de_custo_manhattan(nodo:Nodo)->int:
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um inteiro com o valor da função de custo.
    :param nodo: objeto da classe Nodo
    :return: int
    """
    custo = nodo.custo + distancia_manhattan(nodo.estado)
    return custo

def distancia_manhattan(estado:str)->int:
    """
    Recebe um estado (string) e retorna a distância de Manhattan calculada a partir de quantos movimentos
    horizontais e verticais são necessários para chegar à posição correta
    :param estado: str
    :return: int
    """
    distancia_total = 0

    if estado == DadosSolucaoPuzzle.estado_final:                               # se o estado for o final, a distância é 0
        return distancia_total
    
    matriz_estado = estado_string_para_matriz(estado)                           # transforma numa matriz para calcular a distância em dosi eixos
    DadosSolucaoPuzzle.gera_dicionario_estado_final()                           # gera o dicionário com a posição de cada valor na matriz final

    for i in range(len(matriz_estado)):                                         # itera sobre as linhas e colunas da matriz do estado atual
        for j in range(len(matriz_estado[i])):
            valor_atual = matriz_estado[i][j]
            valor_final = DadosSolucaoPuzzle.matriz_estado_final[i][j]

            if valor_atual != valor_final:                                                      # compara o valor atual com o valor final
                i_final, j_final = DadosSolucaoPuzzle.valor_posicao_estado_final[valor_atual]   # se forem diferentes, pega a posição do valor atual na matriz final
                distancia_valor = abs(i_final - i) + abs(j_final - j)                           # e calcula a distância de manhattan
                distancia_total += distancia_valor                                              # soma a distância total
                
    return distancia_total

# Não preenchidos ===========
def bfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def dfs(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

def astar_new_heuristic(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = sua nova heurística e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError
