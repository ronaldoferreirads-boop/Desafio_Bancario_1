"""DESAFIO:
Cliar um sistema Bancario onde terá somente as 3 operacões: Depositar, sacar e ver o extrato!

Regras:
Deposito = Depositar somente valores positivos. Todos os depositos devem ser salvos em uma variavel.
Saque = Deve permitir somente 3 saques diários. O limite de cada saque deve ser de R$ 500,00. Se não tiver saldo, uma mensagem deve ser exibida.
Extrato = Todas as operações devem aparecer no extrato bancário. 

No tinal da operação, deve exibir o saldo da conta bancaria no formato R$ xxx.xxx

"""

print("""
===========================================
      Seja bem vindo ao banco RONALDO!
===========================================
""")

menu = """
---------------------------------------
Por gentiza, digite a opção que deseja!
[d] Para Depositar
[s] Para Sacar
[e] Para Extrato
[x] Para Sair
> Opção: """

saldo = 0
limite = 500
extrato = []  # agora é uma lista
numero_saques = 0
limite_saque = 3

while True:

    opcao = input(menu)

    
    if opcao == "d":
        valor = float(input("\n>Informe o valor do depósito: "))

        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: R$ {valor:.2f}")  # adiciona na lista
            print(f"\n>Depósito de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n>Operação falhou! O valor informado é inválido.")

    elif opcao == "s":
        valor = float(input("\n>Informe o valor do saque: "))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= limite_saque

        if excedeu_saldo:
            print("\n>Operação falhou! Você não tem saldo suficiente.")

        elif excedeu_limite:
            print(f"\n>Operação falhou! O valor do saque excede o limite de R$ {limite:.2f} por saque!")

        elif excedeu_saques:
            print(f"\n>Operação falhou! Número máximo de saques diarios foi excedido.\nVocê pode realizar {limite_saque} diarios!")

        elif valor > 0:
            saldo -= valor
            extrato.append(f"Saque: R$ {valor:.2f}")  # adiciona na lista
            numero_saques += 1
            print(f"\n>Saque de R$ {valor:.2f} realizado com sucesso!")
        else:
            print("\n>Operação falhou! O valor informado é inválido.")

    elif opcao == "e":
        print("\n================ EXTRATO ================")
        if not extrato: #verifica se o extrato está vazio
            print("Não foram realizadas movimentações.")
        else:
            for operacao in extrato:
                print(operacao)
        print(f"\nSaldo: R$ {saldo:.2f}")
        print("==========================================")

    elif opcao == "x":
        print("""
=========================================
Volte sempre! O banco RONALDO agradece
por ter você como cliente!
========================================
              """)
        break

    else:
        print("\n>Operação inválida, por favor selecione novamente a operação desejada!")