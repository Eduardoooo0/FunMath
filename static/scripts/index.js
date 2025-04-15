// function fecharModal() {
//     const overlay = document.getElementById('bloco_bemvindo');
//     overlay.style.opacity = 0; // Esconde com transição

//     setTimeout(() => {
//         overlay.style.display = 'none';
//         localStorage.setItem('boasVindas', 'true'); // Marca que o modal foi exibido
//     }, 500); // Tempo deve ser igual ao da transição
// }

// window.addEventListener('load', () => {
//     const jaMostrou = localStorage.getItem('boasVindas');

//     if (!jaMostrou) {
//         // Mostrar tela de boas-vindas
//         const overlay = document.getElementById('bloco_bemvindo');
//         overlay.style.display = 'flex'; // Mostra o modal
//         setTimeout(() => {
//             overlay.style.opacity = 1; // Faz a transição de opacidade
//         }, 10); // Um pequeno delay para permitir a exibição
//     }
// });