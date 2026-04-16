from flask import Flask, jsonify, request
from validator import val_funcionario

app = Flask(__name__)

funcionarios = []


@app.route("/funcionario", methods=["GET"])
def listar_funcionarios():
    return jsonify(funcionarios)


@app.route("/funcionario", methods=["POST"])
def adicionar_funcionario():
    nova_entrada = request.get_json()

    if val_funcionario(nova_entrada):
        funcionarios.append(nova_entrada)
        return jsonify({"mensagem": "funcionário adicionado com sucesso!"}), 201
    else:
        return jsonify({"erro": "Dados inválidos, verifique os campos"}), 400


@app.route("/funcionario/<int:indice>", methods=["GET"])
def buscar_funcionario(indice):
    if indice >= len(funcionarios) or indice < 0:
        return jsonify({"erro": "funcionário não encontrado"}), 404
    return jsonify(funcionarios[indice])


@app.route("/funcionario/<int:indice>", methods=["PUT"])
def atualizar_funcionario(indice):
    if indice >= len(funcionarios) or indice < 0:
        return jsonify({"erro": "funcionário não encontrado"}), 404

    dados = request.get_json()
    if not val_funcionario(dados):
        return jsonify({"erro": "Dados inválidos para atualização"}), 400

    funcionarios[indice].update(dados)
    return jsonify({"mensagem": "funcionário atualizado com sucesso!"})


@app.route("/funcionario/<int:indice>", methods=["DELETE"])
def deletar_funcionario(indice):
    if indice >= len(funcionarios) or indice < 0:
        return jsonify({"erro": "funcionário não encontrado"}), 404

    funcionarios.pop(indice)
    return jsonify({"mensagem": "Removido com sucesso!"})


if __name__ == "__main__":
    app.run(debug=True)