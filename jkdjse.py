
def eh_territorio(t):
    '''
    Irá verificar se t é um territorio válido
    
    Primeiro verificamos se t corresponde a um tuplo com tamanho entre 1 e 26 (número de colunas)
    De seguida verificamos se cada elemento de t é um tuplo, todos com o mesmo tamanho, entre 1 e 99 (número de linhas) 
    Por fim verificamos se cada elemento dentro desses tuplos corresponde a 0 ou 1(representações válidas de interseções vazias ou ocupadas)
    
    '''
    if (isinstance(t,tuple) and 1<=len(t)<=26):
        if isinstance(t[0],tuple) and 1<=len(t[0])<=99:
            for n in range(len(t)):
                if (not isinstance(t[n],tuple) or len(t[n])!=len(t[0])):
                    return False
                for a in t[n]:
                    if a not in (0,1):
                        return False
            return True
        else:return False
    else:return False
def obtem_ultima_intersecao(t):
    '''Devolve a ultima interseção do território
    Devolve um tuplo constituido pela letra correspondente à ultima coluna e pelo número correspondente à ultima linha.
    '''
    return (chr(64+len(t)),len(t[0]))
def eh_intersecao(arg):
    '''
    Irá verificar se arg é um territorio válido
    
    Primeiro verificamos se t corresponde a um tuplo com tamanho entre 1 e 26 (número de colunas)
    De seguida verificamos se cada elemento de t é um tuplo, todos com o mesmo tamanho, entre 1 e 99 (número de linhas) 
    Por fim verificamos se cada elemento dentro desses tuplos corresponde a 0 ou 1(representações válidas de interseções vazias ou ocupadas)
    
    '''
    return (type(arg)==tuple and len(arg)==2 and type(arg[0])== str and len(arg[0])==1 and 64<ord(arg[0])<92 and type(arg[1])==int and 0<arg[1]<=99)
#ja está verificado

def eh_intersecao_valida(t,arg):
    if eh_intersecao(arg):
        return (ord(arg[0]) <= 64+len(t) and arg[1] <=len(t[0]))
    else:
        return False
def eh_intersecao_livre(t,i):
    if eh_intersecao_valida(t,i):
        return t[ord(i[0])-65][i[1]-1] == 0
    else:return False
def obtem_intersecoes_adjacentes(t,i):
    linha=i[1]
    coluna=ord(i[0])-65
    intersecoes=[]
    if linha>1:
        intersecoes.append((chr(65+coluna),linha-1))
    if coluna>0:
        intersecoes.append((chr(65+coluna-1),linha))
    if coluna<(len(t)-1):
        intersecoes.append((chr(coluna+1+65),linha))
    if linha<len(t[0]):
        intersecoes.append((chr(65+coluna),linha+1))
    return tuple(intersecoes)
def ordena_intersecoes(tup):
    lista= [x for x in tup]
    lista=sorted(lista, key= lambda lista: (lista[1] ,lista[0]))
    return tuple(lista)        
def territorio_para_str(t):
    #parece muito grande
    if not eh_territorio(t):
        raise ValueError('territorio_para_str: argumento invalido')
    linhas=len(t[0])
    colunas=len(t)
    linha1='  '
    territorio=''
    for n in range(colunas):
        linha1+=(' '+chr(65+n))
    territorio+=(linha1+'\n')
    for n in range(linhas,0,-1):
        if n<10:
            territorio+=(' '+str(n)+' ')
        else:
            territorio+=(str(n)+' ')
        for a in range(colunas):
            if t[a][n-1]==0:
                territorio+='. '
            else:
                territorio+='X '
        if n<10:
            territorio+=(' '+str(n)+'\n')
        else:
            territorio+=(str(n)+'\n')
    territorio+=linha1
    return territorio

#Funções das cadeias de montanhas e dos vales

def obtem_cadeia(t,i):
    if (not eh_territorio(t) or not eh_intersecao_valida(t,i)):
        raise ValueError('obtem_cadeia: argumentos invalidos')
    valor_do_inicial=(eh_intersecao_livre(t,i))
    lista_de_conecoes=[i]
    for n in lista_de_conecoes:
        adj=obtem_intersecoes_adjacentes(t,n)
        for a in adj:
            if (valor_do_inicial==eh_intersecao_livre(t,a) and a not in lista_de_conecoes) :
                lista_de_conecoes.append(a)
    return ordena_intersecoes(tuple(lista_de_conecoes))
def obtem_vale(t,i):
    vale=[]
    if not eh_intersecao_valida(t,i):
        raise ValueError('obtem_vale: argumentos invalidos')
    if eh_intersecao_livre(t,i):
        raise ValueError('obtem_vale: argumentos invalidos')
    cadeia=obtem_cadeia(t,i)
    for n in cadeia:
        adj = obtem_intersecoes_adjacentes(t,n)
        for a in adj:
            if (eh_intersecao_livre(t,a) and a not in vale):
                vale.append(a)
    return ordena_intersecoes(tuple(vale))

#Funções de informação de um território

def verifica_conexao(t,i1,i2):
    if (not eh_territorio(t) or not eh_intersecao_valida(t,i1) or not eh_intersecao_valida(t,i2)):
        raise ValueError("verifica_conexao: argumentos invalidos")
    if eh_intersecao_livre(t,i1)!=eh_intersecao_livre(t,i2):
        return False
    elif i2 in obtem_cadeia(t,i1):
        return True
    else: return False
    
def calcula_numero_montanhas(t):
    if not eh_territorio(t):
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    montanha=0
    for n in t:
        for a in n:
            if a==1:
                montanha+=1
    return montanha
def lista_de_montanhas(t):
    if not eh_territorio(t):
        raise ValueError('calcula_numero_montanhas: argumento invalido')
    montanhas=[]
    for n in range(len(t)):
        for a in range(len(t[n])):
            if t[n][a]==1:
                montanhas.append((chr(65+n),a+1))
    return montanhas
def calcula_numero_cadeias_montanhas(t):
    if not eh_territorio(t):
        raise ValueError('calcula_numero_cadeias_montanhas: argumento invalido')
    cadeias=tuple([])
    numero_cadeias=0
    montanhas=lista_de_montanhas(t)
    for n in montanhas:
        if n not in cadeias:
            numero_cadeias+=1
            cadeias+=obtem_cadeia(t,n)
    return numero_cadeias
def calcula_tamanho_vales(t):
    if not eh_territorio(t):
        raise ValueError('calcula_tamanho_vales: argumento invalido')
    montanhas=lista_de_montanhas(t)
    vales=[]
    for n in montanhas:
        anexos=obtem_intersecoes_adjacentes(t,n)
        for a in anexos :
            if (eh_intersecao_livre(t,a) and a not in vales):
                vales.append(a)
    return len(vales)


