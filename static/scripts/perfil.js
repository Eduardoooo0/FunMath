
let selectedColor = '#00AEEF';

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
    fecharModal();
}

function selectColor(element) {
    const colors = document.querySelectorAll('.color');
    colors.forEach(color => color.classList.remove('selected'));
    element.classList.add('selected');
    selectedColor = element.style.backgroundColor;
    const preview = document.getElementById('avatarPreview');
    preview.style.backgroundColor = selectedColor;
}