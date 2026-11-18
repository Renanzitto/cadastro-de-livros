from flask import Flask, request, jsonify

from database import (
    criar_tabela,
    cadastrar_livro,
    listar_livros,
    excluir_livro
)

# Inicializa o servidor Flask
app = Flask(__name__)


# Permite a comunicação com o Front-end
@app.after_request
def configurar_cors(resposta):
    resposta.headers["Access-Control-Allow-Origin"] = "*"
    resposta.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resposta.headers["Access-Control-Allow-Methods"] = "GET, POST, DELETE, OPTIONS"

    return resposta


# Rota inicial
@app.route("/")
def inicio():
    return jsonify({
        "mensagem": "Servidor da Biblioteca Digital funcionando!"
    })


# Lista todos os livros
@app.route("/api/livros", methods=["GET"])
def obter_livros():
    livros = listar_livros()

    return jsonify(livros), 200


# Cadastra um novo livro
@app.route("/api/livros", methods=["POST"])
def adicionar_livro():
    dados = request.get_json(silent=True)

    if not dados:
        return jsonify({"erro": "Envie os dados do livro."}), 400

    titulo = dados.get("titulo")
    autor = dados.get("autor")
    ano = dados.get("ano")

    if not titulo or not autor or ano is None:
        return jsonify({
            "erro": "Preencha todos os campos."
        }), 400

    try:
        ano = int(ano)
    except (ValueError, TypeError):
        return jsonify({"erro": "O ano precisa ser um número."}), 400

    if ano < 1 or ano > 2100:
        return jsonify({"erro": "Informe um ano válido."}), 400

    livro_id = cadastrar_livro(
        titulo.strip(),
        autor.strip(),
        ano
    )

    return jsonify({
        "mensagem": "Livro cadastrado com sucesso!",
        "id": livro_id
    }), 201


# Exclui um livro
@app.route("/api/livros/<int:livro_id>", methods=["DELETE"])
def remover_livro(livro_id):
    excluido = excluir_livro(livro_id)

    if not excluido:
        return jsonify({
            "erro": "Livro não encontrado."
        }), 404

    return jsonify({
        "mensagem": "Livro excluído com sucesso!"
    }), 200


# Inicia o servidor
if __name__ == "__main__":
    criar_tabela()

    app.run(debug=True, port=5000)