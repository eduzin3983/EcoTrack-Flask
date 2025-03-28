// Função para expandir a imagem
function expandImage(event) {
    const overlay = document.getElementById('overlay');
    const expandedImg = document.getElementById('expanded-img');

    expandedImg.src = event.target.src;

    overlay.style.display = 'flex';
}

// Função para fechar a imagem expandida
function closeImage() {
    const overlay = document.getElementById('overlay');
    overlay.style.display = 'none';
}

document.querySelectorAll('.clickable-img').forEach(img => {
    img.addEventListener('click', expandImage);
});

document.querySelector('.close-btn').addEventListener('click', closeImage);

document.getElementById('overlay').addEventListener('click', (event) => {
    if (event.target === document.getElementById('overlay')) {
        closeImage();
    }
});