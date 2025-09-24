***DESAFIO:***

> **Data: 17/09/2025**

__Criar um sistema Bancario onde terá somente as 3 operacões: Depositar, sacar e ver o extrato!__

**Regras:**

*Deposito* = Depositar somente valores positivos. Todos os depositos devem ser salvos em uma variavel.

*Saque =* Deve permitir somente 3 saques diários. O limite de cada saque deve ser de R$ 500,00. Se não tiver saldo, uma mensagem deve ser exibida.
*Extrato* = Todas as operações devem aparecer no extrato bancário. 

No tinal da operação, deve exibir o saldo da conta bancaria no formato R$ xxx.xxx



> **Data: 23/09/2025**

__Com os novos conhecimentos adquiridos sobre data e hora, você foi encarregado de implementar as seguintes funcionalidades no sistema:__

- Estabelecer um limite de 10 transações diárias para uma conta;
- ser o usuário tentar fazer uma transação após atingir o limite, deve ser informado que ele excedeu o número de transações permitidas para aquele dia; e
- mostre no extrato, a data e hora de todas as transações.

 > **Data: 24/09/2025**

__Desario:__


**Orientação:**

Separar as funções existentes de saque, depósito e extrato em funções. Criar duas novas funções: Cadastrar usuários (clientes) e cadastrar conta bancaria.

**Objetivo:**

Precisamos deixar nosso código mais modularizado, para isso vamos criar funções para as operações existentes: sacar, depositar e visualizar histórico. Além disso, deve se criar duas funções: Criar usuário (cliente do banco) e criar conta corrente (vincular com o usuário).

> **Aluno: Ronaldo Ferreira dos Santos**

-------------------------------------------------

O meu código est usando a Biblioteca json para armazenar os dados e recupera-los toda vez que for rodado o código. 


A biblioteca json no Python serve para trabalhar com o formato JSON (JavaScript Object Notation), que é um formato de texto muito usado para armazenar e trocar dados entre sistemas.

Ela faz basicamente duas coisas principais:

🔑 **1. Converter objetos Python para JSON (Serialização)**

Quando você tem um dicionário, lista ou outro objeto Python, pode transformá-lo em texto JSON usando json.dump() ou json.dumps().
Isso é útil para salvar em arquivos ou enviar para APIs.

Exemplo:

import json

dados = {"nome": "Ronaldo", "idade": 35}

*Converte para JSON em texto*

texto_json = json.dumps(dados, indent=4)
print(texto_json)


Saída:

{
    "nome": "Ronaldo",
    "idade": 35
}


E para salvar em um arquivo:

with open("dados.json", "w") as f:
    json.dump(dados, f, indent=4)

🔑 **2. Converter JSON de volta para objetos Python (Desserialização)**

Quando você lê um arquivo JSON ou recebe um JSON de uma API, pode transformá-lo em um objeto Python com json.load() ou json.loads().

Exemplo:

with open("dados.json", "r") as f:
    dados_carregados = json.load(f)

print(dados_carregados["nome"])  # Ronaldo


Agora dados_carregados é um dicionário Python, e você pode manipulá-lo normalmente.

✅ Resumo simples
O que você faz	Função JSON	Resultado
Python ➡ JSON	json.dump() ou json.dumps()	Transforma listas/dicionários em texto para salvar ou enviar
JSON ➡ Python	json.load() ou json.loads()	Transforma texto JSON em listas/dicionários para usar no programa
