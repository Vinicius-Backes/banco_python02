from abc import ABC, abstractmethod
from datetime import datetime


# ==================================================
# CONFIGURAÇÕES
# ==================================================

AGENCIA_PADRAO = "0001"
LIMITE_SAQUE = 500
LIMITE_SAQUES_DIARIOS = 3


# ==================================================
# CLIENTES
# ==================================================

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)


class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(endereco)
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento


# ==================================================
# HISTÓRICO
# ==================================================

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        })


# ==================================================
# CONTAS
# ==================================================

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0.0
        self._numero = numero
        self._agencia = AGENCIA_PADRAO
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def depositar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para depósito! @@@")
            return False

        self._saldo += valor
        print("\n=== Depósito realizado com sucesso! ===")
        return True

    def sacar(self, valor):
        if valor <= 0:
            print("\n@@@ Valor inválido para saque! @@@")
            return False

        if valor > self._saldo:
            print("\n@@@ Saldo insuficiente! @@@")
            return False

        self._saldo -= valor
        print("\n=== Saque realizado com sucesso! ===")
        return True


class ContaCorrente(Conta):
    def __init__(
        self,
        numero,
        cliente,
        limite=LIMITE_SAQUE,
        limite_saques=LIMITE_SAQUES_DIARIOS
    ):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        total_saques = sum(
            1 for transacao in self.historico.transacoes
            if transacao["tipo"] == "Saque"
        )

        if valor > self.limite:
            print("\n@@@ Valor excede o limite permitido! @@@")
            return False

        if total_saques >= self.limite_saques:
            print("\n@@@ Limite diário de saques atingido! @@@")
            return False

        return super().sacar(valor)

    def __str__(self):
        return (
            f"Agência: {self.agencia}\n"
            f"Conta: {self.numero}\n"
            f"Titular: {self.cliente.nome}"
        )


# ==================================================
# TRANSAÇÕES
# ==================================================

class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


# ==================================================
# FUNÇÕES AUXILIARES
# ==================================================

def menu():
    return input("""
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair
=> """).lower()


def buscar_cliente(cpf, clientes):
    return next(
        (cliente for cliente in clientes if cliente.cpf == cpf),
        None
    )


def obter_conta(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return None

    return cliente.contas[0]


def solicitar_cliente(clientes):
    cpf = input("Informe o CPF: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")

    return cliente


# ==================================================
# OPERAÇÕES
# ==================================================

def operar_deposito(clientes):
    cliente = solicitar_cliente(clientes)
    if not cliente:
        return

    conta = obter_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do depósito: "))
    cliente.realizar_transacao(conta, Deposito(valor))


def operar_saque(clientes):
    cliente = solicitar_cliente(clientes)
    if not cliente:
        return

    conta = obter_conta(cliente)
    if not conta:
        return

    valor = float(input("Informe o valor do saque: "))
    cliente.realizar_transacao(conta, Saque(valor))


def exibir_extrato(clientes):
    cliente = solicitar_cliente(clientes)
    if not cliente:
        return

    conta = obter_conta(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")

    if not conta.historico.transacoes:
        print("Nenhuma movimentação realizada.")
    else:
        for transacao in conta.historico.transacoes:
            print(
                f"{transacao['tipo']}: "
                f"R$ {transacao['valor']:.2f} | "
                f"{transacao['data']}"
            )

    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("==========================================")


def criar_cliente(clientes):
    cpf = input("Informe o CPF: ")

    if buscar_cliente(cpf, clientes):
        print("\n@@@ CPF já cadastrado! @@@")
        return

    nome = input("Informe o nome: ")
    data_nascimento = input("Informe a data de nascimento: ")
    endereco = input("Informe o endereço: ")

    novo_cliente = PessoaFisica(
        cpf=cpf,
        nome=nome,
        data_nascimento=data_nascimento,
        endereco=endereco
    )

    clientes.append(novo_cliente)
    print("\n=== Cliente criado com sucesso! ===")


def criar_conta(numero_conta, clientes, contas):
    cliente = solicitar_cliente(clientes)
    if not cliente:
        return

    nova_conta = ContaCorrente(numero_conta, cliente)

    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)

    print("\n=== Conta criada com sucesso! ===")


# ==================================================
# PROGRAMA PRINCIPAL
# ==================================================

def main():
    clientes = []
    contas = []

    opcoes = {
        "d": lambda: operar_deposito(clientes),
        "s": lambda: operar_saque(clientes),
        "e": lambda: exibir_extrato(clientes),
        "nu": lambda: criar_cliente(clientes),
        "nc": lambda: criar_conta(len(contas) + 1, clientes, contas)
    }

    while True:
        opcao = menu()

        if opcao == "q":
            print("\nEncerrando sistema...")
            break

        operacao = opcoes.get(opcao)

        if operacao:
            operacao()
        else:
            print("\n@@@ Operação inválida! @@@")


if __name__ == "__main__":
    main()
