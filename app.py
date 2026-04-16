from flask import Flask, render_template, request, redirect, url_for, flash
from models.produto import Produto
from models.movimentacao import Movimentacao

app = Flask(__name__)
app.secret_key = "chave_secreta_simples"


@app.route("/")
def index():
    produtos_baixo = Produto.listar_estoque_baixo()
    return render_template("index.html", produtos_baixo=produtos_baixo)


@app.route("/produtos")
def listar_produtos():
    produtos = Produto.listar()
    return render_template("produtos.html", produtos=produtos)


@app.route("/produto/novo")
def novo_produto():
    return render_template("cadastrar_produto.html")


@app.route("/produto/salvar", methods=["POST"])
def salvar_produto():
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    unidade_medida = request.form["unidade_medida"]
    quantidade = int(request.form["quantidade"])
    estoque_minimo = int(request.form["estoque_minimo"])
    preco_custo = float(request.form["preco_custo"])
    preco_venda = float(request.form["preco_venda"])

    if nome.strip() == "":
        flash("O nome do produto é obrigatório.")
        return redirect(url_for("novo_produto"))

    if quantidade < 0 or estoque_minimo < 0 or preco_custo < 0 or preco_venda < 0:
        flash("Valores não podem ser negativos.")
        return redirect(url_for("novo_produto"))

    produto = Produto(
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        unidade_medida=unidade_medida,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
        preco_custo=preco_custo,
        preco_venda=preco_venda
    )
    produto.cadastrar()

    flash("Produto cadastrado com sucesso.")
    return redirect(url_for("listar_produtos"))


@app.route("/produto/editar/<int:id>")
def editar_produto(id):
    produto = Produto.buscar_por_id(id)
    return render_template("editar_produto.html", produto=produto)


@app.route("/produto/atualizar/<int:id>", methods=["POST"])
def atualizar_produto(id):
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    categoria = request.form["categoria"]
    unidade_medida = request.form["unidade_medida"]
    quantidade = int(request.form["quantidade"])
    estoque_minimo = int(request.form["estoque_minimo"])
    preco_custo = float(request.form["preco_custo"])
    preco_venda = float(request.form["preco_venda"])

    if nome.strip() == "":
        flash("O nome do produto é obrigatório.")
        return redirect(url_for("editar_produto", id=id))

    if quantidade < 0 or estoque_minimo < 0 or preco_custo < 0 or preco_venda < 0:
        flash("Valores não podem ser negativos.")
        return redirect(url_for("editar_produto", id=id))

    produto = Produto(
        id=id,
        nome=nome,
        descricao=descricao,
        categoria=categoria,
        unidade_medida=unidade_medida,
        quantidade=quantidade,
        estoque_minimo=estoque_minimo,
        preco_custo=preco_custo,
        preco_venda=preco_venda
    )
    produto.atualizar()

    flash("Produto atualizado com sucesso.")
    return redirect(url_for("listar_produtos"))


@app.route("/produto/excluir/<int:id>")
def excluir_produto(id):
    Produto.excluir(id)
    flash("Produto excluído com sucesso.")
    return redirect(url_for("listar_produtos"))


@app.route("/movimentacoes")
def listar_movimentacoes():
    movimentacoes = Movimentacao.listar()
    return render_template("movimentacoes.html", movimentacoes=movimentacoes)


@app.route("/movimentacao/entrada/<int:produto_id>")
def tela_entrada(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    return render_template("entrada.html", produto=produto)


@app.route("/movimentacao/entrada/<int:produto_id>", methods=["POST"])
def registrar_entrada(produto_id):
    quantidade = int(request.form["quantidade"])

    if quantidade <= 0:
        flash("A quantidade deve ser maior que zero.")
        return redirect(url_for("tela_entrada", produto_id=produto_id))

    mensagem = Movimentacao.registrar_entrada(produto_id, quantidade)
    flash(mensagem)
    return redirect(url_for("listar_produtos"))


@app.route("/movimentacao/saida/<int:produto_id>")
def tela_saida(produto_id):
    produto = Produto.buscar_por_id(produto_id)
    return render_template("saida.html", produto=produto)


@app.route("/movimentacao/saida/<int:produto_id>", methods=["POST"])
def registrar_saida(produto_id):
    quantidade = int(request.form["quantidade"])

    if quantidade <= 0:
        flash("A quantidade deve ser maior que zero.")
        return redirect(url_for("tela_saida", produto_id=produto_id))

    mensagem = Movimentacao.registrar_saida(produto_id, quantidade)
    flash(mensagem)
    return redirect(url_for("listar_produtos"))


if __name__ == "__main__":
    app.run(debug=True)
