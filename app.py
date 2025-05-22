from flask import Flask, render_template, request, jsonify
from flask import session 
import random

app = Flask(__name__)
app.secret_key = "sua_chave_segura"

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
    session["palavra"] = random.choice(palavras)
    session["estado"] = ["_"] * len(jogo["palavra"])
    session["tentativas"] = 6


@app.route("/")
def index():
    # NÃO reinicia o jogo aqui
    novo_jogo()
    return render_template("index.html", estado=session["estado"], tentativas=session["tentativas"])

@app.route("/jogar", methods=["POST"])
def jogar():
    letra = request.json["letra"]

    palavra = session.get("palavra")
    estado = session.get("estado")
    tentativas = session.get("tentativas")
    
    acertou = False

    for i, l in enumerate(jogo["palavra"]):
        if l == letra:
            jogo["estado"][i] = letra
            acertou = True

    if not acertou:
        jogo["tentativas"] -= 1

    session["estado"] = estado
    session["tentativas"] = tentativas 

    fim = ""
    if "_" not in estado:
        fim = "ganhou"
    elif tentativas == 0:
        fim = "perdeu"

    return jsonify({
        "estado": estado,
        "tentativas": tentativas,
        "fim": fim,
        "palavra": palavra if fim == "perdeu" else None
    })

@app.route("/novo")
def novo():
    novo_jogo()
    return render_template("index.html", estado=jogo["estado"], tentativas=jogo["tentativas"])

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
