# -*- coding: utf-8 -*-


# Importa os módulos necessários para o funcionamento do sistema.
import json  # Para trabalhar com arquivos JSON (salvar e carregar dados).
import sys  # Fornece acesso a variáveis e funções do sistema, como os argumentos da linha de comando.
from pathlib import Path  # Oferece uma maneira orientada a objetos de lidar com caminhos de arquivos.
from datetime import datetime, date  # Para trabalhar com datas e horas.
from abc import ABC, abstractmethod  # Para criar classes abstratas (modelos para outras classes).


# --------------------------- UTIL ---------------------------
# Seção de utilitários, com funções e variáveis de apoio.

def get_base_dir():
    """Retorna o diretório base do script em execução."""
    try:
        # Tenta obter o caminho do arquivo atual (__file__).
        return Path(__file__).resolve().parent
    except NameError:
        # Se __file__ não estiver definido (por exemplo, em um ambiente interativo),
        # tenta usar o primeiro argumento da linha de comando (sys.argv[0]).
        if len(sys.argv) > 0 and sys.argv[0]:
            p = Path(sys.argv[0]).resolve()
            if p.exists():
                return p.parent
        # Se nada funcionar, retorna o diretório de trabalho atual.
        return Path.cwd()

# Define o diretório base para salvar os arquivos de dados.
BASE_DIR = get_base_dir()
# Define os caminhos completos para os arquivos JSON.
ARQ_CLIENTES = BASE_DIR / "clientes.json"
ARQ_CONTAS = BASE_DIR / "contas.json"
ARQ_EXTRATOS = BASE_DIR / "extratos.json"
ARQ_TRANSACOES_DIARIAS = BASE_DIR / "transacoes_diarias.json"

# Imprime os caminhos dos arquivos de dados para informar ao usuário onde eles serão salvos.
print(f"\n> Arquivos JSON serão lidos/salvos em: {BASE_DIR}")
print(f"> {ARQ_CLIENTES}")
print(f"> {ARQ_CONTAS}")
print(f"> {ARQ_EXTRATOS}")
print(f"> {ARQ_TRANSACOES_DIARIAS}\n")


# --------------------------- UML CLASSES ---------------------------
# Seção com a definição das classes que representam as entidades do sistema bancário.

class Cliente:
    """Classe base para representar um cliente do banco."""
    def __init__(self, endereco):
        """Inicializa um objeto Cliente."""
        self.endereco = endereco  # O endereço do cliente.
        self.contas = []  # Uma lista para armazenar as contas do cliente.

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self.contas.append(conta)

    def to_dict(self):
        """Converte os dados do cliente para um dicionário, para facilitar a serialização em JSON."""
        return {
            "endereco": self.endereco,
            "contas": [c.numero for c in self.contas]  # Salva apenas os números das contas.
        }


class PessoaFisica(Cliente):
    """Classe para representar um cliente do tipo Pessoa Física, herdando de Cliente."""
    def __init__(self, nome, cpf, data_nascimento, endereco):
        """Inicializa um objeto PessoaFisica."""
        super().__init__(endereco)  # Chama o construtor da classe pai (Cliente).
        self.nome = nome  # O nome do cliente.
        self.cpf = cpf  # O CPF do cliente.
        self.data_nascimento = data_nascimento  # A data de nascimento do cliente.

    def to_dict(self):
        """Converte os dados da pessoa física para um dicionário."""
        d = super().to_dict()  # Obtém o dicionário da classe pai.
        d.update({"nome": self.nome, "cpf": self.cpf, "data_nascimento": self.data_nascimento})  # Adiciona os campos específicos.
        return d


class Historico:
    """Classe para armazenar o histórico de transações de uma conta."""
    def __init__(self):
        """Inicializa um objeto Historico."""
        self.transacoes = []  # Uma lista para armazenar as transações.

    def adicionar_transacao(self, transacao, cpf_usuario=None, numero_conta=None):
        """Adiciona uma nova transação ao histórico."""
        self.transacoes.append({
            "tipo": transacao.__class__.__name__,  # O tipo da transação (Saque, Deposito).
            "valor": transacao.valor,  # O valor da transação.
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),  # A data e hora da transação.
            "cpf": cpf_usuario,  # O CPF do cliente que realizou a transação.
            "conta": numero_conta  # O número da conta onde a transação foi realizada.
        })

    def mostrar(self, cpf=None, conta_num=None):
        """Exibe o histórico de transações, com filtros opcionais por CPF e número da conta."""
        filtradas = [t for t in self.transacoes if (cpf is None or t.get("cpf") == cpf) and (conta_num is None or t.get("conta") == conta_num)]
        for t in filtradas:
            print(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}")

    def to_list(self):
        """Retorna a lista de transações."""
        return self.transacoes[:]


class Conta:
    """Classe base para representar uma conta bancária."""
    def __init__(self, numero, cliente):
        """Inicializa um objeto Conta."""
        self.saldo = 0  # O saldo inicial da conta é zero.
        self.numero = numero  # O número da conta.
        self.agencia = "0001"  # A agência é fixa.
        self.cliente = cliente  # O cliente associado a esta conta.
        self.historico = Historico()  # Um objeto para registrar o histórico de transações.

    def sacar(self, valor):
        """Realiza um saque na conta."""
        if valor > self.saldo:
            print("\n> Operação falhou! Você não tem saldo suficiente.")
            return False
        elif valor <= 0:
            print("\n> Operação falhou! O valor informado é inválido (deve ser positivo).")
            return False
        self.saldo -= valor
        print(f"\n> Saque de R$ {valor:.2f} realizado com sucesso!")
        return True

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        if valor <= 0:
            print("\n> Operação falhou! O valor informado é inválido (deve ser positivo).")
            return False
        self.saldo += valor
        print(f"\n> Depósito de R$ {valor:.2f} realizado com sucesso!")
        return True

    def registrar_transacao(self, transacao, cpf_usuario=None, empresa_conta_numero=None):
        """Registra uma transação na conta."""
        # O registro efetivo (persistência e contagem de transações diárias)
        if transacao.registrar(self):
            # Adiciona ao histórico da conta.
            self.historico.adicionar_transacao(transacao, cpf_usuario, self.numero)
            return True
        return False

    def to_dict(self):
        """Converte os dados da conta para um dicionário."""
        return {"numero": self.numero, "agencia": self.agencia, "saldo": self.saldo, "cliente_cpf": self.cliente.cpf}


class ContaCorrente(Conta):
    """Classe para representar uma conta corrente, herdando de Conta."""
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        """Inicializa um objeto ContaCorrente."""
        super().__init__(numero, cliente)  # Chama o construtor da classe pai (Conta).
        self.limite = limite  # O limite de valor por saque.
        self.limite_saques = limite_saques  # O limite de quantidade de saques por dia.
        self.saques_realizados = {}  # Um dicionário para controlar os saques diários.

    def sacar(self, valor):
        """Realiza um saque na conta corrente, com validações de limite e quantidade."""
        hoje = date.today().isoformat()  # Obtém a data de hoje no formato 'YYYY-MM-DD'.
        self.saques_realizados.setdefault(hoje, 0)  # Garante que a data de hoje exista no dicionário.

        if self.saques_realizados[hoje] >= self.limite_saques:
            print(f"\n> Operação falhou! Número máximo de {self.limite_saques} saques diários foi excedido para esta conta.")
            return False
        elif valor > self.limite:
            print(f"\n> Operação falhou! O valor do saque excede o limite de R$ {self.limite:.2f} por saque.")
            return False

        if super().sacar(valor):  # Chama o método sacar da classe pai (Conta).
            self.saques_realizados[hoje] += 1  # Incrementa o contador de saques diários.
            return True
        return False


class Transacao(ABC):
    """Classe abstrata (interface) para definir o contrato de uma transação."""
    @property
    @abstractmethod
    def valor(self):
        """Propriedade abstrata para o valor da transação."""
        pass

    @abstractmethod
    def registrar(self, conta):
        """Método abstrato para registrar a transação em uma conta."""
        pass


class Saque(Transacao):
    """Classe para representar uma transação de saque."""
    def __init__(self, valor):
        """Inicializa um objeto Saque."""
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do saque."""
        return self._valor

    def registrar(self, conta):
        """Registra o saque na conta."""
        return conta.sacar(self.valor)


class Deposito(Transacao):
    """Classe para representar uma transação de depósito."""
    def __init__(self, valor):
        """Inicializa um objeto Deposito."""
        self._valor = valor

    @property
    def valor(self):
        """Retorna o valor do depósito."""
        return self._valor

    def registrar(self, conta):
        """Registra o depósito na conta."""
        return conta.depositar(self.valor)


# --------------------------- SISTEMA (Bank) ---------------------------
class Bank:
    """Classe principal que orquestra todo o sistema bancário."""
    LIMITE_TRANSACOES_DIARIAS_POR_CONTA = 10  # Limite de transações diárias por conta.

    def __init__(self):
        """Inicializa o objeto Bank, carregando todos os dados dos arquivos JSON."""
        self.clientes = []  # Lista de objetos PessoaFisica.
        self.contas = []  # Lista de objetos ContaCorrente.
        self.extratos = []  # Lista de todas as transações (histórico global).
        self.transacoes_diarias_por_conta = {}  # Dicionário para controlar as transações diárias.
        self.saldos = {}  # Dicionário para armazenar os saldos das contas.
        self.saques_realizados = {}  # Dicionário para controlar os saques realizados.
        self.usuario_logado = None  # O cliente atualmente logado no sistema.
        self.conta_logada = None  # A conta atualmente selecionada pelo cliente.
        self.load_all()  # Carrega todos os dados dos arquivos JSON.

    # ------------------ I/O JSON ------------------
    def save_all(self):
        """Salva todos os dados do sistema (clientes, contas, extratos, etc.) em arquivos JSON."""
        # Salva os dados dos clientes.
        clientes_data = [c.to_dict() for c in self.clientes]
        salvar_json(ARQ_CLIENTES, clientes_data)

        # Salva os dados das contas.
        contas_data = [c.to_dict() for c in self.contas]
        salvar_json(ARQ_CONTAS, contas_data)

        # Salva o extrato geral (juntando os históricos de todas as contas).
        extrato_geral = []
        for c in self.contas:
            extrato_geral.extend(c.historico.to_list())
        salvar_json(ARQ_EXTRATOS, extrato_geral)

        # Salva o controle de transações diárias.
        salvar_json(ARQ_TRANSACOES_DIARIAS, self.transacoes_diarias_por_conta)

    def load_all(self):
        """Carrega todos os dados dos arquivos JSON e reconstrói os objetos em memória."""
        # Carrega os dados brutos dos arquivos JSON.
        clientes_raw = carregar_json(ARQ_CLIENTES)
        contas_raw = carregar_json(ARQ_CONTAS)
        extratos_raw = carregar_json(ARQ_EXTRATOS)
        transacoes_diarias_raw = carregar_json(ARQ_TRANSACOES_DIARIAS)

        # Reconstrói os objetos de cliente.
        cpf_para_cliente = {}
        for cr in clientes_raw:
            c = PessoaFisica(cr.get("nome", ""), cr.get("cpf", ""), cr.get("data_nascimento", ""), cr.get("endereco", ""))
            self.clientes.append(c)
            cpf_para_cliente[c.cpf] = c

        # Reconstrói os objetos de conta.
        for cr in contas_raw:
            cpf = cr.get("cliente_cpf")
            cliente = cpf_para_cliente.get(cpf)
            numero = cr.get("numero")
            if cliente:
                conta = ContaCorrente(numero, cliente)
                conta.saldo = cr.get("saldo", 0)
                cliente.adicionar_conta(conta)
                self.contas.append(conta)
                self.saldos[numero] = conta.saldo
                self.saques_realizados[numero] = conta.saques_realizados

        # Popula os históricos das contas com as transações carregadas.
        for t in extratos_raw:
            conta_num = t.get("conta")
            conta = next((c for c in self.contas if c.numero == conta_num), None)
            if conta:
                conta.historico.transacoes.append(t)
            self.extratos.append(t)

        # Carrega o controle de transações diárias.
        self.transacoes_diarias_por_conta = transacoes_diarias_raw or {}

    # ------------------ VALIDAÇÃO ------------------
    @staticmethod
    def validar_cpf(cpf):
        """Valida se um CPF é uma string de 11 dígitos numéricos."""
        return isinstance(cpf, str) and cpf.isdigit() and len(cpf) == 11

    # ------------------ CRUD CLIENTE/CONTA ------------------
    def criar_cliente(self, cpf=None):
        """Cria um novo cliente no sistema."""
        if not cpf:
            cpf = input("Digite o CPF do cliente (apenas números): ")
        while not self.validar_cpf(cpf):
            print("CPF inválido! Digite apenas números e com 11 dígitos.")
            cpf = input("Digite o CPF do cliente (apenas números): ")

        if any(c.cpf == cpf for c in self.clientes):
            print(f"\n> Cliente com CPF {cpf} já cadastrado.")
            return cpf

        nome = input("Digite o nome completo do cliente: ")
        data_nascimento = input("Digite a data de nascimento (dd/mm/aaaa): ")
        endereco = input("Digite o endereço (logradouro, número - bairro - cidade/estado): ")

        cliente = PessoaFisica(nome, cpf, data_nascimento, endereco)
        self.clientes.append(cliente)
        self.save_all()  # Salva os dados após a criação do cliente.
        print(f"\n> Cliente '{nome}' criado com sucesso!")
        return cpf

    def criar_conta(self, cpf=None):
        """Cria uma nova conta para um cliente existente."""
        if not cpf:
            cpf = input("Digite o CPF do cliente para vincular a conta (apenas números): ")
        while not self.validar_cpf(cpf):
            print("CPF inválido! Digite apenas números e com 11 dígitos.")
            cpf = input("Digite o CPF do cliente para vincular a conta (apenas números): ")

        cliente_existente = next((c for c in self.clientes if c.cpf == cpf), None)

        if cliente_existente:
            numero_conta = str(len(self.contas) + 1).zfill(4)  # Gera um novo número de conta.
            conta = ContaCorrente(numero_conta, cliente_existente)
            self.contas.append(conta)
            cliente_existente.adicionar_conta(conta)
            self.saldos[numero_conta] = 0
            self.saques_realizados[numero_conta] = 0
            self.save_all()  # Salva os dados após a criação da conta.
            print(f"\n> Conta '{numero_conta}' criada com sucesso para '{cliente_existente.nome}'.")
        else:
            print("\n> Cliente não encontrado. Por favor, crie o cliente antes de criar uma conta.")
            confirmar_criar_cliente = input("Deseja criar um novo cliente agora? (s/n): ").lower()
            if confirmar_criar_cliente == 's':
                novo_cpf = self.criar_cliente(cpf)
                if novo_cpf:
                    self.criar_conta(novo_cpf)

    def listar_contas(self):
        """Lista todas as contas cadastradas no sistema."""
        if not self.contas:
            print("\n> Nenhuma conta cadastrada no momento.")
            return

        print("\n================ LISTA DE CONTAS ================")
        for conta in self.contas:
            print(f"Conta: {conta.numero} \n| Cliente: {conta.cliente.nome} \n| CPF: {conta.cliente.cpf} \n| Saldo: R$ {conta.saldo:.2f}")
            print()
        print("=================================================")

    # ------------------ LOGIN / IDENTIFICAÇÃO ------------------
    def identificar_usuario(self):
        """Identifica o usuário através do CPF e seleciona a sua conta."""
        self.usuario_logado = None
        self.conta_logada = None

        while self.usuario_logado is None:
            cpf_digitado = input("\nInforme seu CPF (apenas números) para acessar: ")
            while not self.validar_cpf(cpf_digitado):
                print("CPF inválido! Digite apenas números e com 11 dígitos.")
                cpf_digitado = input("Informe seu CPF (apenas números) para acessar: ")

            usuario_encontrado = next((c for c in self.clientes if c.cpf == cpf_digitado), None)

            if not usuario_encontrado:
                print("\n> Usuário não encontrado. É necessário cadastrá-lo.")
                confirmar_cadastro = input("Deseja cadastrar um novo usuário agora? (s/n): ").lower()
                if confirmar_cadastro == 's':
                    novo_cpf = self.criar_cliente(cpf_digitado)
                    if novo_cpf:
                        self.criar_conta(novo_cpf)
                        usuario_encontrado = next((c for c in self.clientes if c.cpf == novo_cpf), None)
                        if usuario_encontrado:
                            self.usuario_logado = usuario_encontrado
                            self.conta_logada = usuario_encontrado.contas[-1] if usuario_encontrado.contas else None
                            if self.conta_logada:
                                print(f"\n> Bem-vindo(a), {usuario_encontrado.nome}! Sua conta {self.conta_logada.numero} foi selecionada.")
                            else:
                                print("\n> Erro: Conta não encontrada para o novo usuário. Por favor, tente novamente.")
                                self.usuario_logado = None
                        else:
                            print("\n> Erro inesperado ao cadastrar e logar o usuário. Tente novamente.")
                            self.usuario_logado = None
                else:
                    print("\n> Operação cancelada. Por favor, tente novamente com um CPF válido ou cadastre-se.")
            else:
                conta_do_usuario = next((c for c in self.contas if c.cliente.cpf == cpf_digitado), None)
                if conta_do_usuario:
                    self.usuario_logado = usuario_encontrado
                    self.conta_logada = conta_do_usuario
                    print(f"\n> Bem-vindo(a), {usuario_encontrado.nome}! Sua conta {self.conta_logada.numero} foi selecionada.")
                else:
                    print("\n> Nenhuma conta encontrada para este CPF. Por favor, crie uma conta.")
                    confirmar_criar_conta = input("Deseja criar uma nova conta agora? (s/n): ").lower()
                    if confirmar_criar_conta == 's':
                        self.criar_conta(cpf_digitado)
                        conta_do_usuario = next((c for c in self.contas if c.cliente.cpf == cpf_digitado), None)
                        if conta_do_usuario:
                            self.usuario_logado = usuario_encontrado
                            self.conta_logada = conta_do_usuario
                            print(f"\n> Bem-vindo(a), {usuario_encontrado.nome}! Sua conta {self.conta_logada.numero} foi selecionada.")
                        else:
                            print("\n> Erro: Conta não encontrada após a criação. Tente novamente.")
                            self.usuario_logado = None
                    else:
                        print("\n> Operação cancelada. Por favor, tente novamente.")

    # ------------------ TRANSACOES & EXTRATO ------------------
    def registrar_transacao(self, tipo, valor):
        """Registra uma transação (saque ou depósito) na conta do usuário logado."""
        if not self.conta_logada or not self.usuario_logado:
            print("\n> Nenhuma conta ou usuário logado.")
            return False

        numero_conta = self.conta_logada.numero
        hoje_str = datetime.now().strftime("%Y-%m-%d")

        # Controle de limite de transações diárias.
        key = f"{numero_conta}_{hoje_str}"
        self.transacoes_diarias_por_conta.setdefault(key, 0)
        if self.transacoes_diarias_por_conta[key] >= self.LIMITE_TRANSACOES_DIARIAS_POR_CONTA:
            print(f"\n> Operação falhou! Limite de {self.LIMITE_TRANSACOES_DIARIAS_POR_CONTA} transações diárias excedido para esta conta.")
            return False

        # Cria o objeto da transação (Saque ou Deposito).
        transacao = None
        if tipo == "Saque":
            transacao = Saque(valor)
        elif tipo == "Depósito":
            transacao = Deposito(valor)
        else:
            print("\n> Tipo de transação inválido.")
            return False

        # Registra a transação na conta.
        if self.conta_logada.registrar_transacao(transacao, self.usuario_logado.cpf):
            self.transacoes_diarias_por_conta[key] += 1
            self.save_all()  # Salva os dados após cada transação.
            return True
        return False

    def mostrar_extrato(self):
        """Mostra o extrato da conta do usuário logado."""
        if not self.conta_logada or not self.usuario_logado:
            print("\n> Nenhuma conta ou usuário logado.")
            return

        print(f"\n================ EXTRATO DA CONTA {self.conta_logada.numero} ================")
        print(f"\t|Cliente: {self.usuario_logado.nome}")
        print()
        self.conta_logada.historico.mostrar()
        print(f"\nSaldo atual: R$ {self.conta_logada.saldo:.2f}")
        print("=======================================================")

    #-------------------IMPRIMIR EXTRATO EM TXT----------------------------
    def exportar_extrato_txt(self):
        #Exporta o extrato bancário para um arquivo TXT na pasta Downloads do usuário.
        if not self.conta_logada or not self.usuario_logado:
            print("\n> Nenhuma conta ou usuário logado.")
            return

        # Caminho fixo para Downloads (Windows)
        caminho_downloads = Path(r"C:\Users\ronaldo.santos\Downloads")
        caminho_downloads.mkdir(parents=True, exist_ok=True)

        # Nome do arquivo com data/hora para não sobrescrever
        nome_arquivo = f"extrato_conta_{self.conta_logada.numero}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        caminho_arquivo = caminho_downloads / nome_arquivo

        try:
            with open(caminho_arquivo, "w", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write(f"\t|Extrato da Conta {self.conta_logada.numero}\n")
                f.write(f"\t|Cliente: {self.usuario_logado.nome} \n\t|CPF: {self.usuario_logado.cpf}\n")
                f.write("-" * 50 + "\n")

                # Escreve todas as transações no arquivo
                for t in self.conta_logada.historico.transacoes:
                    f.write(f"{t['data']} - {t['tipo']}: R$ {t['valor']:.2f}\n")

                f.write("-" * 50 + "\n")
                f.write(f"Saldo atual: R$ {self.conta_logada.saldo:.2f}\n")
                f.write(f"Data e Hora da Impressão: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
                f.write(f"=" * 50)

            print(f"\n> Extrato exportado com sucesso para: {caminho_arquivo}")

        except Exception as e:
            print(f"\n> Erro ao exportar extrato: {e}")


    def zerar_dados(self):
        """Apaga todos os dados do sistema (clientes, contas, etc.)."""
        confirmar = input("\n> ATENÇÃO: Esta ação apagará TODOS os dados (clientes, contas, extratos). Deseja continuar? (s/n): ").lower()
        if confirmar == 's':
            self.clientes = []
            self.contas = []
            self.extratos = []
            self.transacoes_diarias_por_conta = {}
            self.saldos = {}
            self.saques_realizados = {}
            self.usuario_logado = None
            self.conta_logada = None
            self.save_all()  # Salva o estado vazio dos dados.
            print("\n> Todos os dados foram zerados com sucesso.")
        else:
            print("\n> Operação de zerar dados cancelada.")

    # ------------------ MENU E EXECUÇÃO ------------------
    def menu(self):
        """Exibe o menu de opções e retorna a opção escolhida pelo usuário."""
        return input(f"""
Olá, {self.usuario_logado.nome}! Conta: {self.conta_logada.numero} | Saldo: R$ {self.conta_logada.saldo:.2f}

Por gentileza, informe uma das opções abaixo:

[d] Depositar
[s] Sacar
[e] Extrato
[ee] Exportar Extrato em TXT
[n] Nova Conta
[lc] Listar Contas
[u] Novo Usuário
[trocar] Trocar de Usuário
[z] Zerar Dados
[x] Sair

=> Opção:  """).lower()

    def run(self):
        """Inicia a execução do sistema bancário, exibindo o menu e processando as opções do usuário."""
        print("""
===========================================
      Seja bem-vindo ao banco RONALDO!
===========================================
""")

        # Pede o login do usuário uma vez ao iniciar o sistema.
        self.identificar_usuario()

        while True:
            if not self.usuario_logado or not self.conta_logada:
                print("\n> Nenhum usuário ou conta logada. Por favor, faça login ou crie um novo.")
                self.identificar_usuario()
                continue

            opcao = self.menu()

            if opcao == "d":
                try:
                    valor = float(input(f"\n{self.usuario_logado.nome}, informe o valor do depósito: "))
                except ValueError:
                    print("\n> Valor inválido.")
                    continue
                if valor > 0:
                    self.registrar_transacao("Depósito", valor)
                else:
                    print("\n> Operação falhou! O valor informado é inválido (deve ser positivo).")

            elif opcao == "s":
                try:
                    valor = float(input(f"\n{self.usuario_logado.nome}, informe o valor do saque: "))
                except ValueError:
                    print("\n> Valor inválido.")
                    continue

                # As validações de saque (limite, etc.) são feitas dentro de ContaCorrente.sacar.
                self.registrar_transacao("Saque", valor)

            elif opcao == "e":
                self.mostrar_extrato()
             
            elif opcao == "ee": #Função de Imprimir extrato
                self.exportar_extrato_txt()

            elif opcao == "n":
                self.criar_conta(self.usuario_logado.cpf if self.usuario_logado else None)

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "u":
                self.criar_cliente()

            elif opcao == "trocar":
                print("\n> Trocando de usuário...")
                self.identificar_usuario()

            elif opcao == "z":
                self.zerar_dados()

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


# --------------------------- JSON HELPERS ---------------------------
# Funções auxiliares para salvar e carregar dados em formato JSON.

def salvar_json(arquivo: Path, dados):
    """Salva um dicionário ou lista em um arquivo JSON."""
    try:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erro ao salvar {arquivo}: {e}")


def carregar_json(arquivo: Path):
    """Carrega dados de um arquivo JSON."""
    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existir ou estiver em um formato JSON inválido, retorna uma lista vazia.
        return []


# --------------------------- ENTRYPOINT ---------------------------
# Ponto de entrada do programa.
if __name__ == "__main__":
    # Cria uma instância da classe Bank.
    bank = Bank()
    # Inicia a execução do sistema.
    bank.run()

