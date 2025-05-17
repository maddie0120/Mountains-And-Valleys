#--------------------------------------
# « 1º projeto: Montanhas e Vales »
#--------------------------------------

"""
Instituto Superior Tecnico - Campus Alameda
Curso: Licenciatura em Engenharia Informatica e de Computadores (LEIC - A)
Cadeira: Fundamentos de Programacao (FP)
Corpo Docente responsavel: Arlindo Oliveira
Ano letivo 2023/24
Aluno: Madalena Yang | ist1110206
"""

#***********************************************************
# 2.1 Representacao do territorio e das intersecoes
#***********************************************************

#================================================
# [2.1.1 eh_territorio: universal -> booleano]
#================================================

def eh_territorio(arg):

    """
    Esta funcao recebe um argumento de qualquer tipo (universal) e
    devolve True se o seu argumento corresponde a um territorio e
    False caso contrario
    -------------------------------
    Requisitos a ter em conta:
    - o territorio e constituido por um tuplo de tuplos
    - caminho vertical (pelo menos 1): A a Z (26 elementos)
    - caminho horizontal (pelo menos 1): 1 a 99
    - o argumento e constituido por tuplos (caminhos verticais)
    - dentro desses tuplos devem ser valores inteiros (0 ou 1),
    sendo que estes correspondem aos caminhos horizontais
    - numero de elementos (valores inteiros) que estao dentro dos
    tuplos do argumento devem ser iguais para todos os tuplos
    """

    if not isinstance(arg, tuple) or not 1 <= len(arg) <= 26:
        return False

    if not all(isinstance(tup, tuple) for tup in arg):
        return False
    
    tamanho = len(arg[0])

    for tup in arg: 

        if not all(isinstance(val, int) and\
            (val == 0 or val == 1) for val in tup) or\
            len(tup) < 1 or len (tup) > 99:
            return False
        
        if len(tup) != tamanho: 

            return False
        
    return True


#================================================
# [2.1.2 obtem_ultima_intersecao: territorio -> intersecao]
#================================================

def obtem_ultima_intersecao(t):

    """
    Esta funcao recebe um territorio e devolve a ultima intersecao
    do territorio, ou seja, a intersecao que se encontra no extremo
    superior direito do territorio
    """

    ult_intersecao = ()  

    letra, num = chr(len(t) + 64), len(t[0])

    """
    Para obter a letra da ultima intersecao, e necessario saber qual
    o tamanho do tuplo (territorio) e a ele adicionar 64, uma vez que
    ord('A') = 65. Se quiser a letra 'A' seria chr(1 + 64), sendo
    que nesse caso, o territorio so teria um caminho vertical
    -------------------------------
    Para saber qual o num da ultima intersecao, basta obter o tamanho
    de um tuplo que se encontra dentro do territorio, qualquer um,
    pois eles tem todos tamanhos iguais. Foi usado o primeiro
    """
    
    ult_intersecao = (letra,) + (num,)

    return ult_intersecao


#================================================
# [2.1.3 eh_intersecao: universal -> booleano]
#================================================

def eh_intersecao(arg):

    """
    Esta funcao recebe um argumento de qualquer tipo (universal) e
    devolve True se o seu argumento corresponder a uma intersecao e
    False caso contrario
    -------------------------------
    Sabendo que uma intersecao e um ponto do territorio onde um
    caminho horizontal encontra um caminho vertical. Ela e constituida
    por um tuplo de dois elementos: uma string (letras de 'A' a 'Z')
    e um numero inteiro positivo (1 a 99)
    """

    if not (isinstance(arg, tuple) and len(arg) == 2 and\
            isinstance(arg[0], str) and isinstance (arg[1], int) and\
            len(arg[0]) == 1 and 'A' <= arg[0] <= 'Z' and 1 <= arg[1] <= 99):
        return False
    
    return True


#================================================
# [2.1.4 eh_intersecao_valida: territorio x intersecao -> booleano]
#================================================

def eh_intersecao_valida(t, i):

    """
    Esta funcao recebe um territorio e uma intersecao, devolve True
    se a intersecao corresponder a uma intersecao do territorio, e
    False caso contrario
    """

    if not eh_intersecao(i) or not chr(65) <= i[0] <= chr(len(t) + 64):
        return False
    
    for tup in t:
        if i[1] > len(tup): 
            return False

    return True


#================================================
# [2.1.5 eh_intersecao_livre: territorio x intersecao -> booleano]
#================================================

def eh_intersecao_livre(t, i):

    """
    Esta funcao recebe um territorio e uma intersecao do territorio,
    devolve True se a intersecao corresponder a uma intersecao livre
    (nao ocupada por montanhas, ou seja, o valor que se encontra
    dentro dos tuplos e 0) dentro do territorio e False caso contrario
    """

    if not eh_intersecao_valida(t, i):
        return False

    if t[ord(i[0]) - 65][i[1] - 1] != 0:
        return False

    return True


#================================================
# [2.1.6 obtem_intersecao_adjacentes: territorio x intersecao -> tuplo]
#================================================

def obtem_intersecoes_adjacentes(t, i):

    """
    Esta funcao recebe um territorio e uma intersecao do territorio,
    devolve o tuplo formado pelas intersecoes validas adjacentes da
    intersecao em ordem de leitura de um territorio, ou seja, da
    esquerda para a direita, de baixo para cima
    """

    adj = ()
    cima = (i[0], i[1] + 1)
    baixo = (i[0], i[1] - 1)
    esq = (chr(ord(i[0]) - 1), i[1])
    dir = (chr(ord(i[0]) + 1), i[1])
    
    #as seguintes condicoes ifs verificam se a intersecao dada
    #encontra-se nalguma borda do territorio

    if i[1] > 1:
        adj += (baixo,)

    if i[0] > 'A':
        adj += (esq,)

    if i[0] < chr(64 + len(t)):
        adj += (dir,)

    if i[1] < len(t[0]):
        adj += (cima,)

    return adj


#================================================
# [2.1.7 ordena_intersecoes: tuplo -> tuplo]
#================================================

def ordena_intersecoes(tup):

    """
    Esta funcao recebe um tuplo de intersecoes (potencialmente vazio)
    e devolve um tuplo contendo as mesmas intersecoes so que ordenadas
    de acordo com a ordem de leitura do territorio
    """

    if not tup:
        return tup 
    #se o tuplo de intersecoes for vazio, devolve tuplo vazio
    
    def compara_intersecoes(tup1, tup2):

        letra1, val1 = tup1
        letra2, val2 = tup2

        if val1 < val2:
            return -1

        elif val1 > val2:
            return 1
        
        else: 
            if letra1 < letra2:
                return -1
            
            if letra1 > letra2:
                return 1
            
            else:
                return 0
            
    """
    Retornar -1 quando tup1 deve estar antes do tup2. Pelo mesmo
    raciocinio, se retornar 1, tup1 deve estar depois de tup 2, e
    por fim, se retornar 0, tup1 e igual a tup2
    """

    lista = list(tup)
    #transformar o tuplo numa lista
    #para usar um algoritmo de ordenacao: bubble sort

    for i in range(len(lista)):
        for j in range(0, len(lista) - i - 1):
            if compara_intersecoes(lista[j], lista[j + 1]) == 1:
                lista[j], lista[j + 1] = lista[j +1], lista [j]

    return tuple(lista)


#================================================
# [2.1.8 territorio_para_str: territorio -> cadeia de carateres]
#================================================

def territorio_para_str(t):

    """
    Esta funcao recebe um territorio e devolve a cadeia de caracteres
    que o representa (representacao externa ou representacao 'para os
    nossos olhos'). Se o argumento for invalido, a funcao deve gerar
    um erro com a mensagem 'territorio_para_str: argumento invalido'
    """
    
    if not eh_territorio(t):
        raise ValueError('territorio_para_str: argumento invalido')
     
    ter = ''
    letras = '  '

    for i in range(len(t)):
        letras += ' ' + ''.join(chr(65 + i))

    i = len(t[0]) - 1

    while i >= 0:

        ter += '{:2d}'.format(i + 1) + ' '

        j = 0

        while j < len(t):
            if t[j][i] == 0:
                ter += '.' + ' '

            else: 
                ter += 'X' + ' '

            j += 1

        ter +=  '{:2d}'.format(i + 1) +'\n'
            
        i -= 1

    ter_str = letras + '\n' + ter + letras
        
    return ter_str

#***********************************************************
# 2.2 Funcoes das cadeias de montanhas e dos vales
#***********************************************************

#================================================
# {2.2.1 obtem_cadeia: territorio × intersecao -> tuplo}
#================================================

def obtem_cadeia(t, i):

    """
    Esta funcao recebe um territorio e uma intersecao do territorio,
    devolve o tuplo formado por todas as intersecoes que estao
    conetadas a essa intersecao ordenadas (incluindo a si propria)
    de acordo com a ordem de leitura. Se algum dos argumentos dado
    for invalido, a funcao deve gerar um erro com a mensagem
    'obtem_cadeia: argumentos invalidos'
    """

    if not eh_territorio(t) or not eh_intersecao_valida(t, i):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    
    cadeia = (i,)
    tup = ()
    x = True

    while x:
        x = False
        for i in cadeia:
            if i not in tup:
                for j in obtem_intersecoes_adjacentes(t, i):
                    if eh_intersecao_livre(t, i) == eh_intersecao_livre(t, j) and\
                        j not in cadeia:
                        tup += (i,)
                        cadeia += (j,)
                        x = True

    return ordena_intersecoes(cadeia)


#================================================
# {2.2.2 obtem_vale: territorio × intersecao -> tuplo}
#================================================

def obtem_vale(t, i):

    """
    Esta funcao recebe um territorio e uma intersecao do territorio
    ocupada por uma montanha, devolve o tuplo (potencialmente vazio)
    formado por todas as intersecoes que formam parte do vale da
    montanha da intersecao fornecida como argumento ordenadas de
    acordo a ordem de leitura de um territorio. Se algum dos
    argumentos dados for invalido, a funcao deve gerar um erro com a
    mensagem 'obtem_vale: argumentos invalidos'
    """

    if not eh_territorio(t) or not eh_intersecao_valida(t, i) or\
        eh_intersecao_livre(t, i):
        raise ValueError("obtem_vale: argumentos invalidos")
    
    cadeia = ()

    for j in obtem_cadeia(t,i):
        for k in obtem_intersecoes_adjacentes(t,j):
            if eh_intersecao_livre(t,k) and k not in cadeia:
                cadeia += (k,)

    return ordena_intersecoes(cadeia)


#***********************************************************
# 2.3 Funcoes de informacao de um territorio
#***********************************************************

#================================================
# |2.3.1 verifica conexao: territorio × intersecao × -intersecao -> booleano|
#================================================

def verifica_conexao(t, i1, i2):

    """
    Esta funcao recebe um territorio e duas intersecoes do territorio,
    devolve True se as duas intersecoes estao conectadas e False se
    nao estiverem conectadas contrario. Se algum dos argumentos for
    invalido, a funcao deve gerar um erro com a mensagem
    'verifica_conexao: argumentos invalidos'
    """
    
    if not (eh_territorio(t) and eh_intersecao_valida(t, i1) and\
            eh_intersecao_valida(t, i2)):
        raise ValueError("verifica_conexao: argumentos invalidos")
    
    if i2 in obtem_cadeia(t, i1):
        return True
    
    else:
        return False


#================================================
# |2.3.2 calcula_numero_montanhas: territorio -> inteiro|
#================================================

def calcula_numero_montanhas(t):
    
    """ 
    Esta funcao recebe um territorio e devolve o numero de intersecoes
    ocupadas por montanhas no territorio. Se o argumento dado for
    invalido, a funcao deve gerar um erro com a mensagem
    'calcula_numero_montanhas: argumento invalido'.
    """

    if not eh_territorio(t):
        raise ValueError("calcula_numero_montanhas: argumento invalido")
    
    num = 0 
    
    for i in t:
        for j in i:
            if j == 1:
                num += 1

    return num


#================================================
# |2.3.3 calcula_numero_cadeia_montanhas: territorio -> inteiro|
#================================================

def calcula_numero_cadeias_montanhas(t):

    if not eh_territorio(t):
        raise ValueError("calcula_numero_cadeias_montanhas: argumento invalido")
    
    num = 0
    conj_montanhas = ()

    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == 1 and (chr(65 + i), j+1) not in conj_montanhas:
                cadeia_montanhas = obtem_cadeia(t, (chr(65 + i), j + 1))
                conj_montanhas += cadeia_montanhas
                num += 1

    return num


#================================================
# |2.3.4 calcula_tamanho_vales: territorio -> inteiro|
#================================================

def calcula_tamanho_vales(t):

    """
    Esta funcao recebe um territorio e devolve o numero total de
    intersecoes diferentes que formam todos os vales do territorio.
    Se o argumento dado for invalido, a funcao deve gerar um erro com
    a mensagem 'calcula_tamanho_vales: argumento invalido'
    """

    if not eh_territorio(t):
        raise ValueError("calcula_tamanho_vales: argumento invalido")

    conj_montanhas = ()
    cadeia_montanhas = ()

    for i in range(len(t)):
        for j in range(len(t[i])):
            if t[i][j] == 1 and (chr(65 + i), j+1) not in conj_montanhas:
                conj_montanhas += obtem_cadeia(t, (chr(65 + i), j + 1))
                cadeia_montanhas += obtem_vale(t, (chr(65 + i), j + 1))
     
    return len(set(cadeia_montanhas))