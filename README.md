## |Análise Detalhada do Sistema Bancário em Python - o que o código faz?

Este documento oferece uma análise aprofundada do código de um sistema bancário desenvolvido em Python. O objetivo é dissecar sua arquitetura, funcionalidades e os conceitos de programação empregados, tornando-o um recurso didático valioso para estudantes e entusiastas da programação, especialmente aqueles que estão se aprofundando em Programação Orientada a Objetos (POO).

### |Visão Geral do Sistema

O projeto implementa um sistema bancário simples, porém funcional, que permite a gestão de clientes e suas respectivas contas correntes. As operações básicas como depósito, saque e visualização de extrato estão disponíveis, além de funcionalidades administrativas como a criação de novos clientes e contas. Uma característica central do sistema é a **persistência de dados**, que garante que as informações dos clientes e contas sejam salvas e recuperadas entre as sessões de uso, utilizando arquivos no formato JSON.

### |Funcionalidades Principais

O sistema oferece uma interface de linha de comando interativa, através da qual o usuário pode realizar as seguintes ações:

| Funcionalidade | Descrição |
| :--- | :--- |
| **Login de Usuário** | O sistema inicia solicitando o CPF do usuário. Caso o CPF não seja encontrado, oferece a opção de cadastrar um novo cliente e, subsequentemente, uma nova conta. |
| **Depósito** | Permite ao usuário logado adicionar um valor monetário à sua conta. O sistema valida se o valor é positivo. |
| **Saque** | Permite ao usuário logado retirar um valor de sua conta. Esta operação possui regras de negócio específicas, como um limite de valor por saque e um número máximo de saques diários. |
| **Extrato** | Exibe o histórico de todas as transações (depósitos e saques) realizadas na conta do usuário logado, juntamente com o saldo final. |
| **Criar Novo Cliente** | Cadastra uma nova pessoa física no sistema, solicitando informações como nome, data de nascimento e endereço. |
| **Criar Nova Conta** | Cria uma nova conta corrente e a vincula a um cliente já existente (identificado pelo CPF). |
| **Listar Contas** | Exibe uma lista de todas as contas cadastradas no banco, mostrando o número da conta, o nome do titular, o CPF e o saldo. |
| **Persistência de Dados** | Todas as informações de clientes, contas e transações são salvas em arquivos JSON, permitindo que os dados persistam após o encerramento do programa. |

### |Arquitetura e Programação Orientada a Objetos (POO)

O código é estruturado de forma elegante em torno dos princípios da Programação Orientada a Objetos. As entidades do mundo real (cliente, conta, transação) são modeladas como classes, o que organiza o código, facilita a manutenção e promove o reuso.

> A **Programação Orientada a Objetos** é um paradigma de programação baseado no conceito de "objetos", que podem conter dados na forma de campos (atributos ou propriedades) e código, na forma de procedimentos (métodos).

As principais classes do sistema são:

- **`Cliente` e `PessoaFisica`**: A classe `Cliente` serve como uma classe base, contendo atributos gerais como `endereco`. A classe `PessoaFisica` **herda** de `Cliente` e adiciona atributos específicos para este tipo de cliente, como `nome`, `cpf` e `data_nascimento`. Isso demonstra o conceito de **herança**, um pilar da POO.

- **`Conta` e `ContaCorrente`**: De forma similar, `Conta` é uma classe base com os atributos e métodos fundamentais de uma conta bancária (`saldo`, `agencia`, `numero`, `depositar()`, `sacar()`). `ContaCorrente` herda de `Conta` e implementa regras de negócio específicas, como o `limite` por saque e o `limite_saques` diários. Ela **sobrescreve** o método `sacar()` para adicionar essas validações antes de chamar a implementação da classe pai com `super().sacar()`.

- **`Transacao`, `Saque` e `Deposito`**: Aqui, o código utiliza uma **classe base abstrata (ABC)** chamada `Transacao`. Ela define um "contrato" que todas as transações devem seguir, obrigando as classes filhas a implementar a propriedade `valor` e o método `registrar()`. `Saque` e `Deposito` são classes concretas que herdam de `Transacao` e implementam essa interface, representando os tipos específicos de transação. Isso é um excelente exemplo de **polimorfismo**.

- **`Historico`**: Esta classe é um exemplo de **composição**. Cada objeto `Conta` *tem um* objeto `Historico`, que é responsável por armazenar e gerenciar a lista de transações daquela conta.

- **`Bank`**: Esta é a classe orquestradora do sistema. Ela centraliza a lógica de negócio, gerencia as listas de clientes e contas, controla o fluxo de interação com o usuário (o menu principal) e coordena a persistência dos dados, atuando como uma fachada para todas as operações do sistema.

### Persistência de Dados com JSON

Para que os dados não sejam perdidos ao fechar o programa, o sistema utiliza arquivos **JSON (JavaScript Object Notation)** para armazenamento. A classe `Bank` possui os métodos `save_all()` e `load_all()` que cuidam desse processo.

- **`save_all()`**: Este método percorre as listas de objetos (`clientes`, `contas`) e, para cada objeto, chama um método `to_dict()`. Esse método converte o estado do objeto em um dicionário Python, que pode ser facilmente serializado para o formato JSON pela biblioteca `json` do Python.

- **`load_all()`**: Ao iniciar o sistema, este método lê os arquivos JSON, converte os dados de volta para dicionários Python e os utiliza para reconstruir os objetos (`PessoaFisica`, `ContaCorrente`, etc.) em memória, restaurando o estado do sistema de onde ele parou.

### Fluxo de Execução

O ponto de entrada do programa (`if __name__ == "__main__":`) cria uma instância da classe `Bank` e chama o método `run()`. O fluxo principal é o seguinte:

1.  **Inicialização**: O construtor da classe `Bank` é chamado, e ele imediatamente invoca `load_all()` para carregar os dados dos arquivos JSON.
2.  **Identificação**: O método `run()` primeiro chama `identificar_usuario()`, que gerencia o processo de login via CPF.
3.  **Loop Principal**: O sistema entra em um loop `while True`, onde a cada iteração:
    a. O menu de opções é exibido ao usuário.
    b. A entrada do usuário é capturada.
    c. Uma estrutura `if/elif/else` direciona a execução para o método apropriado da classe `Bank` (por exemplo, `registrar_transacao` para depósito e saque, `mostrar_extrato`, etc.).
4.  **Encerramento**: O loop é quebrado quando o usuário digita a opção de sair ('x'), e uma mensagem de despedida é exibida.

Este sistema é um excelente exemplo prático de como aplicar conceitos fundamentais e avançados de Python para construir uma aplicação de console robusta e bem estruturada. Ele não apenas resolve um problema prático, mas também serve como um material de estudo completo sobre Programação Orientada a Objetos, manipulação de arquivos e design de software.



