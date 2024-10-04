function getLuminance(color) {
    const rgb = color.match(/\d+/g);
    const r = rgb[0], g = rgb[1], b = rgb[2];
    const luminance = 0.2126 * r / 255 + 0.7152 * g / 255 + 0.0722 * b / 255;
    return luminance;
}

function adjustFontColor(element) {
    const bgColor = window.getComputedStyle(element).backgroundColor;
    const luminance = getLuminance(bgColor);
    if (luminance > 0.5) {
        element.style.color = 'black';  // Fundo claro, texto preto
    } else {
        element.style.color = 'white';  // Fundo escuro, texto branco
    }
}

window.onload = function() {
    const elements = document.querySelectorAll('.auto-font');
    elements.forEach(adjustFontColor);  // Chama a função para cada elemento com a classe auto-font
};

var editCarModal = document.getElementById('editCarModal');
editCarModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var chassi = button.getAttribute('data-chassi');
    var modelo = button.getAttribute('data-modelo');
    var ano = button.getAttribute('data-ano');
    var ultimaTrocaPneus = button.getAttribute('data-ultima_troca_pneus');
    var ultimaTrocaOleo = button.getAttribute('data-ultima_troca_oleo');
    var ultimaRevisao = button.getAttribute('data-ultima_revisao');

    var modalTitle = editCarModal.querySelector('.modal-title');
    var editChassiInput = editCarModal.querySelector('#editChassi');
    var editModeloInput = editCarModal.querySelector('input[name="modelo"]');
    var editAnoInput = editCarModal.querySelector('input[name="ano"]');
    var editUltimaTrocaPneusInput = editCarModal.querySelector('input[name="ultima_troca_pneus"]');
    var editUltimaTrocaOleoInput = editCarModal.querySelector('input[name="ultima_troca_oleo"]');
    var editUltimaRevisaoInput = editCarModal.querySelector('input[name="ultima_revisao"]');

    modalTitle.textContent = 'Editar Carro: ' + modelo;
    editChassiInput.value = chassi;
    editModeloInput.value = modelo;
    editAnoInput.value = ano;
    editUltimaTrocaPneusInput.value = ultimaTrocaPneus;
    editUltimaTrocaOleoInput.value = ultimaTrocaOleo;
    editUltimaRevisaoInput.value = ultimaRevisao;
});