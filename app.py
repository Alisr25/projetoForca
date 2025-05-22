from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

palavras = [
    "engenheiro", "advogado", "medico", "programador", "professor",
    "arquiteto", "dentista", "jornalista", "artista", "enfermeiro", "astronauta", "estudante", "psicologo", "psiquiatra", "veterinario", "faxineiro", "motorista", "zelador", "recepcionista", "cozinheiro", "pedreiro", "engenheiro"
]

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
    # NÃO reinicia o jogo aqui
    novo_jogo()
    return render_template("index.html", estado=jogo["estado"], tentativas=jogo["tentativas"])

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

@app.route("/novo")
def novo():
    novo_jogo()
    return render_template("index.html", estado=jogo["estado"], tentativas=jogo["tentativas"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
