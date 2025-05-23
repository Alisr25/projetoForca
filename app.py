from flask import Flask, render_template, request, jsonify, session
import random
import os


app = Flask(__name__)
app.secret_key = os.urandom(24)  # segredo para criptografar a sessão


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
    palavra = random.choice(palavras)
    estado = ["_"] * len(palavra)
    tentativas = 6
    session["jogo"] = {
        "palavra": palavra,
        "estado": estado,
        "tentativas": tentativas
    }


# Inicia o jogo uma vez quando o servidor sobe
novo_jogo()

@app.route("/")
def index():
    if "jogo" not in session:
        novo_jogo()
    jogo = session["jogo"]
    return render_template("index.html", estado=jogo["estado"], tentativas=jogo["tentativas"])


@app.route("/jogar", methods=["POST"])
def jogar():
    letra = request.json["letra"]
    jogo = session.get("jogo")
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

    session["jogo"] = jogo  # atualiza a sessão

    return jsonify({
        "estado": jogo["estado"],
        "tentativas": jogo["tentativas"],
        "fim": fim,
        "palavra": jogo["palavra"] if fim == "perdeu" else None
    })


@app.route("/novo")
def novo():
    novo_jogo()
    jogo = session["jogo"]
    return render_template("index.html", estado=jogo["estado"], tentativas=jogo["tentativas"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
