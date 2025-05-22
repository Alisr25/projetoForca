const alfabeto = "abcdefghijklmnopqrstuvwxyz".split("");
const letrasDiv = document.getElementById("letras");

alfabeto.forEach((letra) => {
  const btn = document.createElement("button");
  btn.textContent = letra;
  btn.classList.add("letra");
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

  const erros = 6 - dados.tentativas;
  document.getElementById("bonequinho").src = `/static/midia/forca${erros}.png`;

  if (dados.fim === "ganhou") {
    document.getElementById("resultado").textContent = " Você ganhou! 🎉🎉🎉";
    desativarBotoes();
  } else if (dados.fim === "perdeu") {
    document.getElementById("resultado").textContent =
      "😢Você perdeu! A palavra era: " + dados.palavra;
    desativarBotoes();
  }
}

let erros = 0;

function erro() {
  erros++;
  const novaImagem = `/static/midia/forca${erros}.png?cache=${new Date().getTime()}`;
  document.getElementById("bonequinho").src = novaImagem;
}


function desativarBotoes() {
  document.querySelectorAll(".letra").forEach((btn) => (btn.disabled = true));
  document.getElementById("jogarNovamente").style.display = "inline-block";
}
document.getElementById("jogarNovamente").onclick = () => {
  window.location.href = "/novo";
};
