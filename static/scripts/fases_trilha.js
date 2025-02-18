function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

document.addEventListener('DOMContentLoaded', function () {
    const buttons = document.querySelectorAll('.button_fases_trilha');
    let faseAtual = parseInt(getCookie('trilha_desbloqueada')) || 1; // Lê o cookie

    // Inicializa os botões
    buttons.forEach(button => {
        const fase = parseInt(button.value);
        if (fase > faseAtual) {
            button.classList.add('bloqueado');
        } else {
            button.classList.add('desbloqueado');
        }
    });

    // Simulação de passar de fase
    buttons.forEach(button => {
        button.addEventListener('click', function (event) {
            const fase = parseInt(this.value);
            if (fase === faseAtual) {
                faseAtual++; // Avança para a próxima fase
                buttons.forEach(b => {
                    const bFase = parseInt(b.value);
                    if (bFase > faseAtual) {
                        b.classList.add('bloqueado');
                        b.classList.remove('desbloqueado');
                    } else {
                        b.classList.remove('bloqueado');
                        b.classList.add('desbloqueado');
                    }
                });
            } else {
                event.preventDefault(); // Impede o envio se a fase não estiver desbloqueada
            }
        });
    });
});
