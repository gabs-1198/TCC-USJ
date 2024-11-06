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
    elements.forEach(adjustFontColor);  
    
     fetch('/data')
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos:', data); // Adicione este log para verificar os dados recebidos

            const labels = data.map(item => item.type);
            const counts = data.map(item => item.count);

            const ctx = document.getElementById('myChart').getContext('2d');
            const myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Quantidade de Trocas',
                        data: counts,
                        backgroundColor: [
                            'rgba(75, 192, 192, 0.2)',
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 206, 86, 0.2)'
                        ],
                        borderColor: [
                            'rgba(75, 192, 192, 1)',
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 206, 86, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Erro ao buscar dados:', error)); // Adicione este log para verificar erros
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