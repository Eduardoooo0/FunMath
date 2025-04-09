window.addEventListener('load', () => {
    setTimeout(() => {
      const overlay = document.getElementById('splash-overlay');
      overlay.style.opacity = 0;
  
      setTimeout(() => {
        overlay.style.display = 'none';
      }, 500); // tempo do fade
    }, 3000); // mostra por 3 segundos
  });
  