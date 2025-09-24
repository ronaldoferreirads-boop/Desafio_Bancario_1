# -*- coding: utf-8 -*-
import json #Carrega o módulo json, que permite trabalhar com dados no formato JSON (JavaScript Object Notation).
import os #Carrega o módulo os, que fornece funções para interagir com o sistema operacional.
import sys #Importa o módulo sys, que fornece acesso a variáveis e funções do interpretador Python.
from pathlib import Path #Importa a classe Path do módulo pathlib, que facilita trabalhar com caminhos de arquivos e pastas de forma mais moderna e intuitiva que os.path.
from datetime import datetime #Importa a classe datetime do módulo datetime, que permite trabalhar com datas e horários.



def get_base_dir():
    """Retorna o diretório base para os arquivos de dados.

    Esta função tenta determinar o diretório onde o script Python está sendo executado.
    Ela utiliza múltiplas estratégias para garantir robustez em diferentes ambientes:
    1. Tenta usar `__file__` (o método mais comum quando o script é executado como um arquivo).
    2. Se `__file__` não estiver disponível, usa `sys.argv[0]` (útil quando o script é chamado diretamente).
    3. Como último recurso, se as opções anteriores falharem, retorna o diretório de trabalho atual (`Path.cwd()`).

    Returns:
        Path: Um objeto Path representando o diretório base.
    """
    try:
        # Tenta obter o diretório do arquivo atual
        return Path(__file__).resolve().parent
    except NameError:
        # Fallback para sys.argv[0] se __file__ não estiver definido (ex: em alguns ambientes interativos)
        if len(sys.argv) > 0 and sys.argv[0]:
            p = Path(sys.argv[0]).resolve()
            if p.exists():
                return p.parent
        # Último recurso: diretório de trabalho atual
        return Path.cwd()

BASE_DIR = get_base_dir()
# Garante que o diretório base exista. `exist_ok=True` evita erro se já existir.
BASE_DIR.mkdir(parents=True, exist_ok=True)

# Define os caminhos completos para os arquivos de persistência de dados (JSON).
# Eles serão armazenados no diretório base do script.
ARQ_CLIENTES = str(BASE_DIR / "clientes.json")
ARQ_CONTAS = str(BASE_DIR / "contas.json")
ARQ_EXTRATO = str(BASE_DIR / "extrato.json")

# Informa ao usuário onde os arquivos de dados serão manipulados.
print(f"\n> Arquivos JSON serão lidos/salvos em: {BASE_DIR}")
print(f"> {ARQ_CLIENTES}")
print(f"> {ARQ_CONTAS}")
print(f"> {ARQ_EXTRATO}\n")

print("""
===========================================
      Seja bem-vindo ao banco RONALDO!
===========================================
""")

# Menu principal do sistema bancário.
menu = """
---------------------------------------
Por gentileza, digite a opção desejada:
[d] Depositar
[s] Sacar
[e] Extrato
[n] Nova conta
[lc] Listar contas
[u] Novo usuário
[trocar] Trocar usuário
[z] Zerar sistema
[x] Sair
> Opção: """

def carregar_dados():
    """Carrega os dados de clientes, contas e extrato dos arquivos JSON.

    Se um arquivo não for encontrado ou estiver corrompido (JSON inválido),
    uma lista vazia é retornada para aquela categoria de dados.

    Returns:
        tuple: Uma tupla contendo (clientes, contas, extrato).
    """
    clientes = []
    contas = []
    extrato = []

    try:
        with open(ARQ_CLIENTES, "r", encoding='utf-8') as f:
            clientes = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Arquivo não existe ou está vazio/inválido, clientes permanece como lista vazia

    try:
        with open(ARQ_CONTAS, "r", encoding='utf-8') as f:
            contas = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Contas permanece como lista vazia

    try:
        with open(ARQ_EXTRATO, "r", encoding='utf-8') as f:
            extrato = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Extrato permanece como lista vazia

    transacoes_diarias_por_conta = {}
    try:
        with open(str(BASE_DIR / "transacoes_diarias.json"), "r", encoding='utf-8') as f:
            transacoes_diarias_por_conta = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    return clientes, contas, extrato, transacoes_diarias_por_conta

def salvar_dados():
    """Salva os dados atuais de clientes, contas e extrato nos arquivos JSON.

    Os dados são salvos com indentação para melhor legibilidade e `ensure_ascii=False`
    para preservar caracteres acentuados e especiais.
    """
    with open(ARQ_CLIENTES, "w", encoding='utf-8') as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)
    with open(ARQ_CONTAS, "w", encoding='utf-8') as f:
        json.dump(contas, f, indent=4, ensure_ascii=False)
    with open(ARQ_EXTRATO, "w", encoding='utf-8') as f:
        json.dump(extrato, f, indent=4, ensure_ascii=False)
    with open(str(BASE_DIR / "transacoes_diarias.json"), "w", encoding='utf-8') as f:
        json.dump(TRANSACOES_DIARIAS_POR_CONTA, f, indent=4, ensure_ascii=False)
def zerar_dados():
    """Reinicia todos os dados do sistema (clientes, contas, extratos, saldos e saques).

    Esta função redefine as listas e dicionários globais para seus estados iniciais
    e então salva essas alterações nos arquivos JSON, efetivamente limpando o sistema.
    """
    global clientes, contas, extrato, saldos, saques_realizados, TRANSACOES_DIARIAS_POR_CONTA
    clientes = []
    contas = []
    extrato = []
    saldos = {}
    saques_realizados = {}
    TRANSACOES_DIARIAS_POR_CONTA = {}
    salvar_dados()
    print("\n> Todos os dados foram zerados com sucesso!")


# Carrega os dados existentes ao iniciar o sistema.
clientes, contas, extrato, TRANSACOES_DIARIAS_POR_CONTA = carregar_dados()

# Dicionário para armazenar saldos por número de conta.
# Inicializa com 0 se a conta não tiver saldo definido.
saldos = {conta['numero']: conta.get('saldo', 0) for conta in contas}

# Dicionário para armazenar o número de saques realizados por conta.
# Inicializa com 0 se a conta não tiver saques definidos.
saques_realizados = {conta['numero']: conta.get('saques', 0) for conta in contas}

# Limites e variáveis de estado globais do sistema.
LIMITE_POR_SAQUE = 500  # Limite máximo por operação de saque.
LIMITE_SAQUES_DIARIOS = 3  # Número máximo de saques permitidos por dia por conta.

USUARIO_LOGADO = None  # CPF do usuário atualmente logado.
CONTA_LOGADA = None  # Dicionário da conta atualmente logada.

def validar_cpf(cpf):
    """Valida se o CPF fornecido é composto apenas por 11 dígitos numéricos.

    Args:
        cpf (str): A string contendo o CPF a ser validado.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    return cpf.isdigit() and len(cpf) == 11

def registrar_transacao(tipo, valor, numero_conta):
    """Registra uma transação no extrato e atualiza o contador de transações diárias.

    Verifica se o limite de transações diárias foi atingido antes de registrar.

    Args:
        tipo (str): O tipo da transação (ex: "Depósito", "Saque").
        valor (float): O valor da transação.

    Returns:
        bool: True se a transação foi registrada com sucesso, False se o limite diário foi atingido.
    """
    global TRANSACOES_DIARIAS_POR_CONTA
    hoje_str = datetime.now().strftime("%Y-%m-%d")

    if numero_conta not in TRANSACOES_DIARIAS_POR_CONTA:
        TRANSACOES_DIARIAS_POR_CONTA[numero_conta] = {}

    if hoje_str not in TRANSACOES_DIARIAS_POR_CONTA[numero_conta]:
        TRANSACOES_DIARIAS_POR_CONTA[numero_conta][hoje_str] = 0

    # Limite de 10 transações diárias por conta.
    LIMITE_TRANSACOES_DIARIAS_POR_CONTA = 10
    transacoes_hoje = TRANSACOES_DIARIAS_POR_CONTA[numero_conta][hoje_str]

    if transacoes_hoje >= LIMITE_TRANSACOES_DIARIAS_POR_CONTA:
        print(f"\n> Operação falhou! Você excedeu o limite de {LIMITE_TRANSACOES_DIARIAS_POR_CONTA} transações diárias para a conta {numero_conta}.")
        return False

    TRANSACOES_DIARIAS_POR_CONTA[numero_conta][hoje_str] += 1
    transacoes_restantes = LIMITE_TRANSACOES_DIARIAS_POR_CONTA - TRANSACOES_DIARIAS_POR_CONTA[numero_conta][hoje_str]
    print(f"\n> Transação registrada. Você tem {transacoes_restantes} operações restantes para hoje na conta {numero_conta}.")
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    extrato.append({
        "data": data_hora,
        "tipo": tipo,
        "valor": valor,
        "cpf": USUARIO_LOGADO,
        "conta": CONTA_LOGADA['numero']
    })
    salvar_dados()
    return True

def criar_cliente(cpf=None):
    """Cria um novo cliente no sistema.

    Solicita informações do cliente (nome, data de nascimento, endereço)
    e o adiciona à lista de clientes. Se um CPF for fornecido, ele é usado;
    caso contrário, é solicitado ao usuário.

    Args:
        cpf (str, optional): O CPF do cliente, se já conhecido. Defaults to None.

    Returns:
        str: O CPF do cliente recém-criado ou existente.
    """
    if not cpf:
        cpf = input("Digite o CPF do cliente (apenas números): ")
    while not validar_cpf(cpf):
        print("CPF inválido! Digite apenas números e com 11 dígitos.")
        cpf = input("Digite o CPF do cliente (apenas números): ")

    # Verifica se o cliente já existe
    if any(c['cpf'] == cpf for c in clientes):
        print(f"\n> Cliente com CPF {cpf} já cadastrado.")
        return cpf

    nome = input("Digite o nome completo do cliente: ")
    data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Digite o endereço (logradouro, número - bairro - cidade/estado): ")

    clientes.append({
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    })
    salvar_dados()
    print(f"\n> Cliente '{nome}' criado com sucesso!")
    return cpf

def criar_conta(cpf=None):
    """Cria uma nova conta bancária para um cliente existente.

    Se o cliente não existir, solicita a criação do cliente primeiro.
    Atribui um número de conta sequencial e inicializa saldo e saques.

    Args:
        cpf (str, optional): O CPF do cliente para vincular a conta. Defaults to None.
    """
    if not cpf:
        cpf = input("Digite o CPF do cliente para vincular a conta (apenas números): ")
    while not validar_cpf(cpf):
        print("CPF inválido! Digite apenas números e com 11 dígitos.")
        cpf = input("Digite o CPF do cliente para vincular a conta (apenas números): ")

    cliente_existente = next((c for c in clientes if c["cpf"] == cpf), None)

    if cliente_existente:
        # Gera um número de conta sequencial (ex: 0001, 0002)
        numero_conta = str(len(contas) + 1).zfill(4)
        conta = {
            "numero": numero_conta,
            "cpf": cpf,
            "nome_cliente": cliente_existente["nome"],
            "saldo": 0,
            "saques_hoje": 0  # Reinicia a contagem de saques diários para a nova conta
        }
        contas.append(conta)
        saldos[numero_conta] = 0
        saques_realizados[numero_conta] = 0
        salvar_dados()
        print(f"\n> Conta '{numero_conta}' criada com sucesso para '{cliente_existente['nome']}'.")
    else:
        print("\n> Cliente não encontrado. Por favor, crie o cliente antes de criar uma conta.")
        # Oferece para criar o cliente
        confirmar_criar_cliente = input("Deseja criar um novo cliente agora? (s/n): ").lower()
        if confirmar_criar_cliente == 's':
            novo_cpf = criar_cliente(cpf) # Passa o CPF já digitado
            if novo_cpf: # Se o cliente foi criado com sucesso
                criar_conta(novo_cpf) # Tenta criar a conta novamente para o novo cliente

def listar_contas():
    """Exibe uma lista de todas as contas cadastradas no sistema.

    Para cada conta, mostra o número da conta, nome do cliente, CPF e saldo atual.
    """
    if not contas:
        print("\n> Nenhuma conta cadastrada no momento.")
        return

    print("\n================ LISTA DE CONTAS ================")
    for conta in contas:
        print(f"Conta: {conta['numero']} \n| Cliente: {conta['nome_cliente']} \n| CPF: {conta['cpf']} \n| Saldo: R$ {saldos.get(conta['numero'], 0):.2f}")
        print()
    print("=================================================")

def identificar_usuario():
    """Permite ao usuário logar no sistema ou criar um novo usuário/conta.

    Solicita o CPF do usuário. Se o usuário não for encontrado, oferece a opção
    de cadastrá-lo e criar uma conta automaticamente. Define as variáveis
    globais `USUARIO_LOGADO` e `CONTA_LOGADA`.
    """
    global USUARIO_LOGADO, CONTA_LOGADA
    USUARIO_LOGADO = None
    CONTA_LOGADA = None

    while USUARIO_LOGADO is None:
        cpf_digitado = input("\nInforme seu CPF (apenas números) para acessar: ")
        while not validar_cpf(cpf_digitado):
            print("CPF inválido! Digite apenas números e com 11 dígitos.")
            cpf_digitado = input("Informe seu CPF (apenas números) para acessar: ")

        usuario_encontrado = next((c for c in clientes if c["cpf"] == cpf_digitado), None)

        if not usuario_encontrado:
            print("\n> Usuário não encontrado. É necessário cadastrá-lo.")
            confirmar_cadastro = input("Deseja cadastrar um novo usuário agora? (s/n): ").lower()
            if confirmar_cadastro == 's':
                novo_cpf = criar_cliente(cpf_digitado) # Tenta criar o cliente com o CPF digitado
                if novo_cpf: # Se o cliente foi criado com sucesso
                    criar_conta(novo_cpf) # Cria uma conta para o novo cliente
                    # Após criar, tenta identificar novamente
                    usuario_encontrado = next((c for c in clientes if c["cpf"] == novo_cpf), None)
                    if usuario_encontrado: # Se agora o usuário existe, loga ele
                        USUARIO_LOGADO = novo_cpf
                        CONTA_LOGADA = next((c for c in contas if c["cpf"] == novo_cpf), None)
                        if CONTA_LOGADA:
                            print(f"\n> Bem-vindo(a), {usuario_encontrado['nome']}! Sua conta {CONTA_LOGADA['numero']} foi selecionada.")
                        else:
                            print("\n> Erro: Conta não encontrada para o novo usuário. Por favor, tente novamente.")
                            USUARIO_LOGADO = None # Força a repetição do loop de login
                    else:
                        print("\n> Erro inesperado ao cadastrar e logar o usuário. Tente novamente.")
                        USUARIO_LOGADO = None # Força a repetição do loop de login
            else:
                print("\n> Operação cancelada. Por favor, tente novamente com um CPF válido ou cadastre-se.")
                # O loop continua para pedir o CPF novamente
        else:
            # Usuário encontrado, agora busca a conta
            conta_do_usuario = next((c for c in contas if c["cpf"] == cpf_digitado), None)
            if conta_do_usuario:
                USUARIO_LOGADO = cpf_digitado
                CONTA_LOGADA = conta_do_usuario
                print(f"\n> Bem-vindo(a), {usuario_encontrado['nome']}! Sua conta {CONTA_LOGADA['numero']} foi selecionada.")
            else:
                print("\n> Nenhuma conta encontrada para este CPF. Por favor, crie uma conta.")
                confirmar_criar_conta = input("Deseja criar uma nova conta agora? (s/n): ").lower()
                if confirmar_criar_conta == 's':
                    criar_conta(cpf_digitado)
                    # Após criar, tenta identificar novamente
                    conta_do_usuario = next((c for c in contas if c["cpf"] == cpf_digitado), None)
                    if conta_do_usuario:
                        USUARIO_LOGADO = cpf_digitado
                        CONTA_LOGADA = conta_do_usuario
                        print(f"\n> Bem-vindo(a), {usuario_encontrado['nome']}! Sua conta {CONTA_LOGADA['numero']} foi selecionada.")
                    else:
                        print("\n> Erro: Conta não encontrada após a criação. Tente novamente.")
                        USUARIO_LOGADO = None # Força a repetição do loop de login
                else:
                    print("\n> Operação cancelada. Por favor, tente novamente.")
                    # O loop continua para pedir o CPF novamente

# Pede login apenas uma vez ao iniciar o programa.
identificar_usuario()

# Loop principal de execução do sistema.
while True:
    if not USUARIO_LOGADO or not CONTA_LOGADA:
        print("\n> Nenhum usuário ou conta logada. Por favor, faça login ou crie um novo.")
        identificar_usuario()
        continue # Reinicia o loop após o login

    cliente_atual = next((c for c in clientes if c["cpf"] == USUARIO_LOGADO), None)
    nome_cliente = cliente_atual["nome"] if cliente_atual else "Usuário Desconhecido"
    numero_conta_logada = CONTA_LOGADA['numero']

    opcao = input(menu)

    if opcao == "d":
        valor = float(input(f"\n{nome_cliente}, informe o valor do depósito: "))
        if valor > 0:
            if registrar_transacao("Depósito", valor, numero_conta_logada):
                saldos[numero_conta_logada] += valor
                CONTA_LOGADA['saldo'] = saldos[numero_conta_logada]
                salvar_dados()
                print(f"\n> Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n> Operação falhou! O valor informado é inválido (deve ser positivo).")

    elif opcao == "s":
        valor = float(input(f"\n{nome_cliente}, informe o valor do saque: "))

        saldo_atual = saldos[numero_conta_logada]
        saques_feitos_hoje = saques_realizados[numero_conta_logada]

        excedeu_saldo = valor > saldo_atual
        excedeu_limite_por_saque = valor > LIMITE_POR_SAQUE
        excedeu_limite_saques_diarios = saques_feitos_hoje >= LIMITE_SAQUES_DIARIOS

        if excedeu_saldo:
            print("\n> Operação falhou! Você não tem saldo suficiente.")
        elif excedeu_limite_por_saque:
            print(f"\n> Operação falhou! O valor do saque excede o limite de R$ {LIMITE_POR_SAQUE:.2f} por saque.")
        elif excedeu_limite_saques_diarios:
            print(f"\n> Operação falhou! Número máximo de {LIMITE_SAQUES_DIARIOS} saques diários foi excedido para esta conta.")
        elif valor <= 0:
            print("\n> Operação falhou! O valor informado é inválido (deve ser positivo).")
        else:
            if registrar_transacao("Saque", valor, numero_conta_logada):
                saldos[numero_conta_logada] -= valor
                saques_realizados[numero_conta_logada] += 1
                CONTA_LOGADA['saldo'] = saldos[numero_conta_logada]
                CONTA_LOGADA['saques_hoje'] = saques_realizados[numero_conta_logada]
                salvar_dados()
                print(f"\n> Saque de R$ {valor:.2f} realizado com sucesso!")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        print(f"\thora de impressão do extrato: \n\t{datetime.now()}")
        print()
        if CONTA_LOGADA:
            print(f"|Cliente: {cliente_atual['nome']} \n|CPF: {cliente_atual['cpf']} \n|Conta: {CONTA_LOGADA['numero']}")
            print()
        
        # Filtra as transações para o usuário e conta logados
        transacoes_da_conta = [op for op in extrato if op["cpf"] == USUARIO_LOGADO and op["conta"] == numero_conta_logada]

        if not transacoes_da_conta:
            print("Não foram realizadas movimentações para esta conta.")
        else:
            for operacao in transacoes_da_conta:
                print(f"{operacao['data']} - {operacao['tipo']}: R$ {operacao['valor']:.2f}")
        print(f"\nSaldo atual: R$ {saldos[numero_conta_logada]:.2f}")
        print("==========================================")

    elif opcao == "n":
        criar_conta(USUARIO_LOGADO) # Tenta criar conta para o usuário logado

    elif opcao == "lc":
        listar_contas()

    elif opcao == "u":
        criar_cliente()

    elif opcao == "trocar":
        print("\n> Trocando de usuário...")
        identificar_usuario()

    elif opcao == "z":
        confirmar = input("\nTem certeza que deseja zerar TODOS os dados do sistema? (s/n): ").lower()
        if confirmar == 's':
            zerar_dados()
        else:
            print("\n> Operação de zerar dados cancelada.")

    elif opcao == "x":
        print("""
=========================================
Volte sempre! O banco RONALDO agradece
por ter você como cliente!
=========================================
""")
        break

    else:
        print("\n> Operação inválida, por favor selecione uma opção válida do menu.")




# Dicionário para armazenar a contagem de transações diárias por conta.
# A chave será o número da conta e o valor será um dicionário com a data e a contagem.
TRANSACOES_DIARIAS_POR_CONTA = {}

