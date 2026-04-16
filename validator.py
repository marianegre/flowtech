def val_funcionario(dados):
    if not dados:
        return False

    campos = [
        "nome",
        "cpf",
        "email",
        "setor",
        "salario",
        "turno",
        "senha",
        "telefone",
        "data_nascimento"
    ]

    for campo in campos:
        if campo not in dados or str(dados[campo]).strip() == "":
            return False

    return True