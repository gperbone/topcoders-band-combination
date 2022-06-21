import csv
import ast

def obter_dados() -> list:
    '''
    Função para obter os dados salvos no programa.
    PARAMETROS: N/A
    RETORNO: lista com todas as entradas existentes
    '''
    try:
        with open(('dados.csv'), 'r') as arq:
            dados = list(csv.reader(arq, delimiter=',', lineterminator='\n'))
        #converter strings em listas
        dados = [[item[0], item[1], ast.literal_eval(item[2]), ast.literal_eval(item[3])] for item in dados]
    except:
        with open(('dados.csv'), 'w') as arq:
            pass
        dados = []

    return dados

def salvar_dados(dados: list) -> None:
    '''
    Função para reescrever dados no programa.
    PARAMETROS: lista
    RETORNO: N/A
    '''
    with open(('dados.csv'), 'w') as arq:
        escritor = csv.writer(arq, delimiter=",", lineterminator="\n")
        escritor.writerows(dados)

def pega_opcao() -> str:
    '''
    Função para obter a opção desejada pelo user.
    PARAMETROS: N/A
    RETORNO: string, já validado, representando uma das opções disponíveis
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

    return opt if int(opt) in [1, 2, 3, 4, 0] else pega_opcao()

def valida_nome() -> str:
    '''
    Função para obter o nome do músico, validado segundo regras (deve conter apenas letras e espaços).
    PARAMETROS: N/A
    RETORNO: string, já validado e formatado, representando o nome do músico
    '''
    nome = input("Digite o nome do músico: ").strip()
    nome_helper = nome.replace(" ", "")
    if nome_helper.isalpha():
        return nome.title()
    else:
        print("O nome deve conter apenas letras e espaços. Tente novamente.")
        return valida_nome()

def valida_email(dados:list) -> str:
    '''
    Função para obter o email do músico, validado segundo regras (letras, underscore (_), ponto (.), dígitos numéricos e, obrigatoriamente, exatamente 1 arroba (@)).
    PARAMETROS: N/A
    RETORNO: string, já validado e formatado, representando o email do músico
    '''
    email = input("Digite o e-mail do músico: ").strip().lower()
    eh_repetido = any([True if email == entrada[1] else False for entrada in dados])
    email_helper = email.replace("_", "").replace(".", "").replace("@", "")
    if email_helper.isalnum() and email.count("@") == 1 and eh_repetido == False:
        return email
    elif eh_repetido:
        print("Este email já existe na base de dados! O email deve ser único. Tente novamente.")
        return valida_email()
    else:
        print("O email deve conter apenas letras, underline, pontos e exatamente um @ apenas letras e espaços. Tente novamente.")
        return valida_email()

def valida_genero() -> list:
    generos = input("Digite os gêneros musicais de interesse do músico (se for mais de 1, separar com vírgulas): ").strip()
    if generos == "":
        print("Digite pelo menos um!")
        return valida_genero()
    else: 
        return [genero.strip().lower() for genero in generos.split(",")]
    
def valida_instrumento() -> list:
    instrumentos = input("Digite os instrumentos que o músico toca (se for mais de 1, separar com vírgulas): ").strip()
    if instrumentos == "":
        print("Digite pelo menos um!")
        return valida_instrumento()
    else: 
        return [instrumento.strip().lower() for instrumento in instrumentos.split(",")]

def cadastrar_musico(dados:list) -> list:
    nome = valida_nome()
    email = valida_email(dados)
    lista_generos = valida_genero()
    lista_instrumentos = valida_instrumento()

    lista_dados = [nome, email, lista_generos, lista_instrumentos]

    dados.append(lista_dados)

    return dados

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

def buscar_musicos(dados:list) -> list:
    nome = input("Digite um nome para busca, ou aperte enter para continuar: ").strip().title()
    email = input("Digite um e-mail para busca, ou aperte enter para continuar: ").strip().lower()
    genero = input("Digite um gênero musical, ou aperte enter para continuar: ").strip().lower()
    instrumento = input("Digite um instrumento, ou aperte enter para continuar: ").strip().lower()
    modo = input("Digite 1 se a busca deve corresponder a todos os campos digitados, ou 2 para pelo menos um: ")

    try:
        modo_de_busca = int(modo)
        dados_para_busca = [nome, email, genero, instrumento]
        if modo_de_busca == 1 or modo_de_busca == 2:
            resultados = busca_de_dados(dados, dados_para_busca, modo_de_busca)
            imprimir_resultados_busca(resultados)
        else:
            raise Exception
    except (ValueError, Exception) as e:
        print("Parâmetros incorretos. Tente novamente!")
    finally:
        return dados

def substituicao_de_dados(dados: list, user_encontrado:list) -> None:

    print(f"User: {dados[user_encontrado][0]} | Gênero(s) de interesse cadastrados: {', '.join(dados[user_encontrado][2])}")
    for i in range(len(dados[user_encontrado][2])):
        input_user = input(f"{dados[user_encontrado][2][i].upper()} : Aperte ENTER para MANTER o gênero ou digite QUALQUER COISA para EXCLUIR: ").strip().lower()
        dados[user_encontrado][2][i] = dados[user_encontrado][2][i] if input_user == "" else ""
    input_user = input(f"Caso deseje adicionar mais gêneros, digite-os separados por vírgula: ").strip().lower()
    input_user = [item.strip() for item in input_user.split(",")]
    dados[user_encontrado][2].extend(input_user)
    while '' in dados[user_encontrado][2]:
        dados[user_encontrado][2].remove('')

    print(f"User: {dados[user_encontrado][0]} | Instrumento(s) de interesse cadastrados: {', '.join(dados[user_encontrado][3])}")
    for i in range(len(dados[user_encontrado][3])):
        input_user = input(f"{dados[user_encontrado][3][i].upper()} : Aperte ENTER para MANTER o gênero ou digite QUALQUER COISA para EXCLUIR: ").strip().lower()
        dados[user_encontrado][3][i] = dados[user_encontrado][3][i] if input_user == "" else ""
    input_user = input(f"Caso deseje adicionar mais instrumentos, digite-os separados por vírgula: ").strip().lower()
    input_user = [item.strip() for item in input_user.split(",")]
    dados[user_encontrado][3].extend(input_user)
    while '' in dados[user_encontrado][3]:
        dados[user_encontrado][3].remove('')

    return dados

def modificar_musico(dados:list) -> None:
    email = input("Digite o email do usuário para modificar: ").strip().lower()
    email_helper = email.replace("_", "").replace(".", "").replace("@", "")
    if email_helper.isalnum() and email.count("@") == 1:
        user_encontrado = [index for index in range(len(dados)) if dados[index][1] == email][0]
        if user_encontrado != []:
            dados_substituidos = substituicao_de_dados(dados, user_encontrado)
            print(f"Usuário {dados_substituidos[user_encontrado][0]} atualizado com sucesso!")
        else:
           print(f"Não há usuários com o e-mail digitado. Tente novamente!") 
           dados_substituidos = dados
    else: 
        print("O e-mail digitado é inválido. Tente novamente.")
        dados_substituidos = dados

    return dados

def executa_combinacoes(musicos_por_instrumento:list, instrumentos:list) -> list:
    combinacoes = []

    while len(musicos_por_instrumento) > 1:
        for musico in musicos_por_instrumento[0]:
            for outro_musico in musicos_por_instrumento[1]:
                combinacoes.append([musico, outro_musico])
            
        restante = [combinacoes] + musicos_por_instrumento[2:]

    return combinacoes(restante) if len(musicos_por_instrumento) > 1 else musicos_por_instrumento

def limpa_combinacoes(resultado: list) -> list:
    lista_emails = [musico[1] for musico in resultado for musicos in resultado]

    return [banda for index, banda in enumerate(resultado) if len(set(lista_emails[index])) == len(banda)]

def imprime_combinacoes(resultado: list, instrumentos: list) -> None:
    for i in range(len(resultado)):
        print(f"Banda {i+1}:")
        for item in resultado[i]:
            print(f"{instrumentos[i]}.upper() : {resultado[i][0]} | {resultado[i][1]} | {', '.join(resultado[i][2])} | {', '.join(resultado[i][3])}")

def montar_banda(dados: list):
    genero_busca = input("Digite o gênero desejado para sua banda: ").strip().lower()
    quantidade = input("Digite a quantidade de músicos para sua banda: ").strip()
    while not(quantidade.isdigit()):
        quantidade = input("Digite a quantidade de músicos para sua banda: ").strip()
    quantidade = int(quantidade)
    instrumentos = []
    for i in range(quantidade):
        instrumentos.append(input(f"Digite o {i+1}o instrumento para sua banda: ").strip())
    #filtra musicos do genero por instrumentos

    lista_por_instrumentos = []
    for i in range(len(instrumentos)):
        for musico in dados:
            if instrumentos[i] in musico[3] and genero_busca in musico[2]:
                lista_por_instrumentos.append(musico)

    resultado = executa_combinacoes(lista_por_instrumentos, instrumentos)
    resultado = limpa_combinacoes(resultado)
    imprime_combinacoes(resultado, instrumentos)

    return dados

def menu(dados:list) -> None:
    opcoes = {
        "1": cadastrar_musico,
        "2": buscar_musicos,
        "3": modificar_musico,
        "4": montar_banda
    }
    opt = pega_opcao()
    while opt != "0":
        dados = opcoes[opt](dados)
        opt = pega_opcao()
    else:
        salvar_dados(dados)
        print("Até mais!")

dados = obter_dados()
menu(dados)
