let selectedColor = localStorage.getItem('selectedColor') || '#00AEEF';
let selectedAvatar = localStorage.getItem('selectedAvatar') || '🐶'; // Avatar padrão

function abrirModal() {
    document.getElementById('modal').style.display = 'flex';
}

function fecharModal() {
    document.getElementById('modal').style.display = 'none';
}

function selectAvatar(emoji) {
    const preview = document.getElementById('avatarPreview');
    preview.textContent = emoji;
    preview.style.backgroundColor = selectedColor;
    
    // Salva o avatar selecionado
    localStorage.setItem('selectedAvatar', emoji);
    fecharModal();
}

function selectColor(element) {
    const colors = document.querySelectorAll('.color');
    colors.forEach(color => color.classList.remove('selected'));
    element.classList.add('selected');
    selectedColor = element.style.backgroundColor;
    
    // Salva a cor selecionada
    localStorage.setItem('selectedColor', selectedColor);
    
    const preview = document.getElementById('avatarPreview');
    preview.style.backgroundColor = selectedColor;
}

// Função para carregar a seleção salva ao iniciar a página
function carregarSelecoes() {
    const preview = document.getElementById('avatarPreview');
    preview.textContent = selectedAvatar;
    preview.style.backgroundColor = selectedColor;
}

// Chame a função ao carregar a página
window.onload = carregarSelecoes;