import csv
import ast

def obter_dados() -> list:
    '''
    Função para obter os dados salvos no programa.
    PARAMETROS: N/A
    RETORNO: lista contendo todas as categorias existentes nos produtos da lista de entrada
    '''
    with open(('dados.csv'), 'r') as arq:
        dados = list(csv.reader(arq, delimiter=',', lineterminator='\n'))

    #converter strings em listas
    dados = [[item[0], item[1], ast.literal_eval(item[2]), ast.literal_eval(item[3])] for item in dados]

    return dados

def apendar_dados(novo_dado: dict) -> None:
    '''
    Função para gravar novos dados no programa.
    PARAMETROS: dict ou lista contendo mais de um dict
    RETORNO: N/A
    '''
    with open(('dados.csv'), 'a') as arq:
        escritor = csv.writer(arq, delimiter=",", lineterminator="\n")
        escritor.writerow(novo_dado)

def pega_opcao() -> str:
    '''
    Função para obter a opção desejada pelo user.
    PARAMETROS: N/A
    RETORNO: inteiro, já validado, representando uma das opções disponíveis
    '''
    print('''
::: LISTA DE OPÇÕES :::
[1] Cadastrar músico
[2] Buscar músicos
[3] Modificar músico
[4] Montar banda
[0] Sair
    ''')

    opt = input("Digite a opção desejada: ")

    while not(opt.isdigit()):
        opt = input("Digite apenas números! Digite a opção desejada: ")

    return int(opt) if opt in "12340" else pega_opcao()

def valida_nome() -> str:
    '''
    Função para obter o nome do músico, validado segundo regras (deve conter apenas letras e espaços).
    PARAMETROS: N/A
    RETORNO: string, já validado e formatado, representando o nome do músico
    '''
    nome = input("Digite o nome do músico: ")
    nome_helper = nome.replace(" ", "")
    if nome_helper.isalpha():
        return nome.title()
    else:
        print("O nome deve conter apenas letras e espaços. Tente novamente.")
        return valida_nome()

def valida_email() -> str:
    '''
    Função para obter o email do músico, validado segundo regras (letras, underscore (_), ponto (.), dígitos numéricos e, obrigatoriamente, exatamente 1 arroba (@)).
    PARAMETROS: N/A
    RETORNO: string, já validado e formatado, representando o email do músico
    '''
    email = input("Digite o e-mail do músico: ")
    eh_repetido = any([True if email == entrada[1] else False for entrada in obter_dados()])
    email_helper = email.replace("_", "").replace(".", "").replace("@", "")
    if email_helper.isalnum() and email.count("@") == 1 and eh_repetido == False:
        return email.lower()
    elif eh_repetido:
        print("Este email já existe na base de dados! O email deve ser único. Tente novamente.")
        return valida_email()
    else:
        print("O email deve conter apenas letras, underline, pontos e exatamente um @ apenas letras e espaços. Tente novamente.")
        return valida_email()

def cadastrar_musico() -> None:
    nome = valida_nome()
    email = valida_email()
    generos = input("Digite os gêneros musicais de interesse do músico (se for mais de 1, separar com vírgulas): ")
    lista_generos = [genero.strip().lower() for genero in generos.split(",")]
    instrumentos = input("Digite os instrumentos que o músico toca (se for mais de 1, separar com vírgulas): ")
    lista_instrumentos = [instrumento.strip().lower() for instrumento in instrumentos.split(",")]

    lista_dados = [nome, email, lista_generos, lista_instrumentos]

    apendar_dados(lista_dados)

def busca_de_dados(dados: list, dados_para_busca: list, modo_de_busca: int) -> list:
    indices_nome, indices_email, indices_genero, indices_instrumento= [], [], [], []
    contagem = 0

    if dados_para_busca[0] != "":
        indices_nome.extend([index for index in range(len(dados)) if dados[index][0] == dados_para_busca[0]])
        contagem += 1
    if dados_para_busca[1] != "":   
        indices_email.extend([index for index in range(len(dados)) if dados[index][1] == dados_para_busca[1]])
        contagem += 1
    if dados_para_busca[2] != "":
        indices_genero.extend(set([index for index in range(len(dados)) for index2 in range(len(dados[index][2])) if dados[index][2][index2] == dados_para_busca[2]]))
        contagem += 1
    if dados_para_busca[3] != "":
        indices_instrumento.extend(set([index for index in range(len(dados)) for index2 in range(len(dados[index][3])) if dados[index][3][index2] == dados_para_busca[3]]))
        contagem += 1
    
    if modo_de_busca == 1: # MODO E
        indices_total = indices_nome + indices_email + indices_genero + indices_instrumento
        indices_E = set([index for index in indices_total if indices_total.count(index) == contagem])

        return [ocorrencia for index, ocorrencia in enumerate(dados) if index in indices_E]
    else: #MODO OU
        indices_total = indices_nome + indices_email + indices_genero + indices_instrumento
        indices_OU = set(indices_total)

        return [ocorrencia for index, ocorrencia in enumerate(dados) if index in indices_OU]

def imprimir_resultados_busca(resultados:list) -> None:
    if resultados != []:
        print("RESULTADO # : NOME | EMAIL | GÊNEROS | INSTRUMENTOS")
        for i in range(len(resultados)):
            print(f"Resultado {i+1} : {resultados[i][0]} | {resultados[i][1]} | {', '.join(resultados[i][2])} | {', '.join(resultados[i][3])}")
    else:
        print("Não há resultados que correpondam à sua busca!")

def buscar_musicos() -> None:
    nome = input("Digite um nome para busca, ou aperte enter para continuar: ").strip().title()
    email = input("Digite um e-mail para busca, ou aperte enter para continuar: ").strip().lower()
    genero = input("Digite um gênero musical, ou aperte enter para continuar: ").strip().lower()
    instrumento = input("Digite um instrumento, ou aperte enter para continuar: ").strip().lower()
    modo = input("Digite 1 se a busca deve corresponder a todos os campos digitados, ou 2 para pelo menos um: ")

    try:
        modo_de_busca = int(modo)
        dados = obter_dados()
        dados_para_busca = [nome, email, genero, instrumento]
        if modo_de_busca == 1 or modo_de_busca == 2:
            resultados = busca_de_dados(dados, dados_para_busca, modo_de_busca)
            imprimir_resultados_busca(resultados)
        else:
            raise Exception
    except (ValueError, Exception):
        print("Parâmetros incorretos. Tente novamente!")


def menu() -> None:
    ativo = 1

    while ativo == 1:
        opt = pega_opcao()

        if opt == 1:
            cadastrar_musico()
            #falta validar se nao eh email repetid
            ativo = 1

        elif opt == 2:
            buscar_musicos()
            ativo = 1

        elif opt == 0:
            print("Até mais!")
            ativo = 0

        else: 
            print("Opção inválida. Tente novamente.")
            ativo = 1


menu()
