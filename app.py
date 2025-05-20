from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

palavras = ["python", "flask", "github", "programar"]
jogo = {
    "palavra": "",
    "estado": [],
    "tentativas": 6
}

def novo_jogo():
    jogo["palavra"] = random.choice(palavras)
    jogo["estado"] = ["_"] * len(jogo["palavra"])
    jogo["tentativas"] = 6

@app.route("/")
def index():
    novo_jogo()
    return render_template("index.html")

@app.route("/jogar", methods=["POST"])
def jogar():
    letra = request.json["letra"]
    acertou = False

    for i, l in enumerate(jogo["palavra"]):
        if l == letra:
            jogo["estado"][i] = letra
            acertou = True

    if not acertou:
        jogo["tentativas"] -= 1

    fim = ""
    if "_" not in jogo["estado"]:
        fim = "ganhou"
    elif jogo["tentativas"] == 0:
        fim = "perdeu"

    return jsonify({
        "estado": jogo["estado"],
        "tentativas": jogo["tentativas"],
        "fim": fim,
        "palavra": jogo["palavra"] if fim == "perdeu" else None
    })


if __name__ == "__main__":
    # Use host='0.0.0.0' para o Render aceitar
    app.run(host="0.0.0.0", port=5000)
