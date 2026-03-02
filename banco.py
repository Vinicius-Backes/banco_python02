def menu():
    return """
[d] Depositar
[s] Sacar   
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair
=> """
def deposito(saldo, valor, extrato, /):
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print("Depósito realizado com sucesso!")
    return saldo, extrato

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    else:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1
        print("Saque realizado com sucesso!")

    return saldo, extrato, numero_saques

def ver_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Já existe usuário com esse CPF!")
            return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = {
        "nome": nome,
        "data_nascimento": data_nascimento,
        "cpf": cpf,
        "endereco": endereco
    }

    usuarios.append(usuario)

    print("Usuário criado com sucesso!")

def criar_conta(AGENCIA, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")

    usuario_encontrado = None

    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            usuario_encontrado = usuario
            break

    if usuario_encontrado:
        print("Conta criada com sucesso!")
        return {
            "agencia": AGENCIA,
            "numero_conta": numero_conta,
            "usuario": usuario_encontrado
        }
    else:
        print("Usuário não encontrado, crie um usuário primeiro.")
        return None
    

def main():
    saldo = 0
    limite = 500
    extrato = ""
    numero_saques = 0
    limite_saques = 3

    usuarios = []
    contas = []

    AGENCIA = "0001"

    while True:
        opcao = input(menu()).strip().lower()
        if opcao == "d":
            valor = float(input("Informe o valor do depósito: "))
            if valor <= 0:
                print("O valor deve ser positivo!")
            else:
                saldo, extrato = deposito(saldo, valor, extrato)

        elif opcao == "s":
            valor = float(input("Informe o valor do saque: "))
            if valor <= 0:
                print("O valor deve ser positivo!")
            else:
                saldo, extrato, numero_saques = saque(
                    saldo=saldo,
                    valor=valor,
                    extrato=extrato,
                    limite=limite,
                    numero_saques=numero_saques,
                    limite_saques=limite_saques
                )

        elif opcao == "e":
            ver_extrato(saldo, extrato=extrato)

        elif opcao == "nu":
            criar_usuario(usuarios)

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "q":
            print("Obrigado por usar nossos serviços!")
            break

        else:
            print("Operação inválida, por favor selecione novamente a.")

main()
