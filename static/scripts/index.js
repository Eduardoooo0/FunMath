window.addEventListener('load', () => {
  const jaMostrou = localStorage.getItem('boasVindas');

  if (!jaMostrou) {
    // Mostrar tela de boas-vindas
    setTimeout(() => {
      const overlay = document.getElementById('splash-overlay');
      overlay.style.opacity = 0;

      setTimeout(() => {
        overlay.style.display = 'none';
        localStorage.setItem('boasVindas', 'true'); // marca como já mostrado
      }, 500);
    }, 3000);
  } else {
    // Esconde diretamente, sem mostrar
    const overlay = document.getElementById('splash-overlay');
    overlay.style.display = 'none';
  }
});
