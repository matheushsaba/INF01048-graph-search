from typing import Iterable, Set, Tuple
import numpy as np 

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
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError


def astar_manhattan(estado:str)->list[str]:
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    # substituir a linha abaixo pelo seu codigo
    raise NotImplementedError

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
