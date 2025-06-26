function carregarQuiz() {
    const codigo = document.getElementById("codigo-input").value.trim();
    const container = document.getElementById("quiz-carregado");
    const respostaBox = document.getElementById("resposta");
    const mensagem = document.getElementById("mensagem-resposta");

    container.innerHTML = "";
    respostaBox.style.display = "none";

    if (!codigo) {
        alert("Digite um código válido.");
        return;
    }

    fetch(`/quiz/${codigo}`)
        .then(res => res.json())
        .then(data => {
            if (data.erro) {
                container.innerHTML = `<p style="color: red;">${data.erro}</p>`;
                return;
            }

            data.perguntas.forEach((p, index) => {
                const div = document.createElement("div");
                div.className = "questao";
                div.innerHTML = `<p><strong>${index + 1}. ${p.pergunta}</strong></p>`;

                p.opcoes.forEach((opcao, i) => {
                    const botao = document.createElement("button");
                    botao.className = "botao-opcao";
                    botao.textContent = opcao;

                    botao.onclick = () => {
                        const correta = p.correta;
                        const selecionada = i + 1;

                        if (selecionada === correta) {
                            botao.classList.add("correta");
                            mensagem.textContent = "✅ Resposta correta!";
                            mensagem.style.color = "green";
                        } else {
                            botao.classList.add("errada");
                            mensagem.textContent = "❌ Resposta incorreta.";
                            mensagem.style.color = "red";
                        }

                        // Desabilita todos os botões da questão
                        div.querySelectorAll("button").forEach(b => {
                            b.disabled = true;
                        });

                        respostaBox.style.display = "block";

                        // Esconde após 2 segundos
                        setTimeout(() => {
                            respostaBox.style.display = "none";
                        }, 2000);
                    };

                    div.appendChild(botao);
                });

                container.appendChild(div);
            });
        });
}
