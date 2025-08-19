from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Simulando banco de dados em memória
investimentos = []
next_id = 1  # contador de IDs

# Função de validação
def validar_investimento(dados):
    try:
        if float(dados["valor"]) <= 0:
            return "Valor deve ser maior que 0."
        if datetime.fromisoformat(dados["data"]) > datetime.now():
            return "Data não pode estar no futuro."
    except Exception as e:
        return "Dados inválidos."
    return None

# Listar todos os investimentos
@app.route("/investimentos", methods=["GET"])
def listar():
    return jsonify(investimentos)

# Cadastrar novo investimento
@app.route("/investimentos", methods=["POST"])
def cadastrar():
    global next_id
    dados = request.get_json()
    erro = validar_investimento(dados)
    if erro:
        return jsonify({"error": erro}), 400

    novo = {
        "id": next_id,
        "nome": dados["nome"],
        "tipo": dados["tipo"],
        "valor": float(dados["valor"]),
        "data": dados["data"]
    }
    investimentos.append(novo)
    next_id += 1
    return jsonify(novo), 201

# Atualizar investimento existente
@app.route("/investimentos/<int:id>", methods=["PUT"])
def atualizar(id):
    dados = request.get_json()
    erro = validar_investimento(dados)
    if erro:
        return jsonify({"error": erro}), 400

    for inv in investimentos:
        if inv["id"] == id:
            inv["nome"] = dados["nome"]
            inv["tipo"] = dados["tipo"]
            inv["valor"] = float(dados["valor"])
            inv["data"] = dados["data"]
            return jsonify(inv)
    return jsonify({"error": "Investimento não encontrado."}), 404

# Excluir investimento
@app.route("/investimentos/<int:id>", methods=["DELETE"])
def deletar(id):
    global investimentos
    for inv in investimentos:
        if inv["id"] == id:
            investimentos = [i for i in investimentos if i["id"] != id]
            return "", 204
    return jsonify({"error": "Investimento não encontrado."}), 404

# Rodar o servidor
if __name__ == "__main__":
    app.run(port=3000, debug=True)