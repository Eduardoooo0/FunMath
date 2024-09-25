window.history.pushState(null, document.title, window.location.href);
window.addEventListener('popstate', function (event) {
    const abandonQuiz = confirm('Você deseja voltar a página inicial?');
    if (abandonQuiz) {
        // Se o usuário confirmar, permita que ele saia
        window.location.href = '/'; // Redirecione para a página de fases
    } else {
        // Caso contrário, reverte a navegação
        window.history.pushState(null, document.title, window.location.href);
    }
});