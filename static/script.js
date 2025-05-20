const alfabeto = "abcdefghijklmnopqrstuvwxyz".split("");
const letrasDiv = document.getElementById("letras");

alfabeto.forEach((letra) => {
  const btn = document.createElement("button");
  btn.textContent = letra;
  btn.onclick = () => enviarLetra(letra, btn);
  letrasDiv.appendChild(btn);
});

async function enviarLetra(letra, botao) {
  botao.disabled = true;
  const resposta = await fetch("/jogar", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ letra }),
  });

  const dados = await resposta.json();

  document.getElementById("palavra").textContent = dados.estado.join(" ");
  document.getElementById("tentativas").textContent =
    "Tentativas restantes: " + dados.tentativas;

  if (dados.fim === "ganhou") {
    document.getElementById("resultado").textContent = "Você ganhou!";
    desativarBotoes();
  } else if (dados.fim === "perdeu") {
    document.getElementById("resultado").textContent =
      "Você perdeu! A palavra era: " + dados.palavra;
    desativarBotoes();
  }
}

function desativarBotoes() {
  document.querySelectorAll("button").forEach((btn) => (btn.disabled = true));
}
