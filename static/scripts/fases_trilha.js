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
        if (fase === faseAtual) {
            button.classList.add('fase-atual');
            button.classList.add('desbloqueado');
        } else if (fase < faseAtual) {
            button.classList.add('desbloqueado');
        } else {
            button.classList.add('bloqueado');
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
                    b.classList.remove('fase-atual');

                    if (bFase === faseAtual) {
                        b.classList.add('fase-atual');
                        b.classList.add('desbloqueado');
                    } else if (bFase < faseAtual) {
                        b.classList.add('desbloqueado');
                    } else {
                        b.classList.add('bloqueado');
                        b.classList.remove('desbloqueado');
                    }
                });
            } else {
                event.preventDefault(); // Impede o envio se a fase não estiver desbloqueada
            }
        });
    });
});