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

let myChart = null;

window.onload = function() {
    const elements = document.querySelectorAll('.auto-font');
    elements.forEach(adjustFontColor);

    fetch('/available_years')
        .then(response => response.json())
        .then(data => {
            const yearSelect = document.getElementById('year');
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.year;
                option.textContent = item.year;
                yearSelect.appendChild(option);
            });

            // Inicializa o gráfico com o primeiro ano disponível
            if (data.length > 0) {
                updateChart(data[0].year); // Inicializa com o primeiro ano disponível
            }
        })
        .catch(error => console.error('Erro ao buscar anos disponíveis:', error));
    document.getElementById('year').addEventListener('change', function() {
        const year = this.value;
        updateChart(year);
    });
};

function updateChart(year) {
    fetch(`/data?year=${year}`)
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos:', data); // Adicione este log para verificar os dados recebidos

            const labels = data.map(item => new Date(0, item.month - 1).toLocaleString('pt-BR', { month: 'long' }));
            const counts = data.map(item => item.count);

            const ctx = document.getElementById('lineChart').getContext('2d');

            // Destruir o gráfico existente antes de criar um novo
            if (myChart) {
                myChart.destroy();
            }

            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Número de Carros Cadastrados',
                        data: counts,
                        backgroundColor: 'rgba(0, 123, 255, 0.2)',
                        borderColor: 'rgba(0, 123, 255, 1)',
                        borderWidth: 2,
                        pointBackgroundColor: 'rgba(255, 255, 255, 1)',
                        pointBorderColor: 'rgba(0, 123, 255, 1)',
                        pointRadius: 5
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
}

const editCarModal = document.getElementById('editCarModal');
editCarModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const chassi = button.getAttribute('data-chassi');
    const modelo = button.getAttribute('data-modelo');
    const ano = button.getAttribute('data-ano');
    const ultimaTrocaPneus = button.getAttribute('data-ultima_troca_pneus');
    const ultimaTrocaOleo = button.getAttribute('data-ultima_troca_oleo');
    const ultimaRevisao = button.getAttribute('data-ultima_revisao');

    const modalTitle = editCarModal.querySelector('.modal-title');
    const editChassiInput = editCarModal.querySelector('#editChassi');
    const editModeloInput = editCarModal.querySelector('input[name="modelo"]');
    const editAnoInput = editCarModal.querySelector('input[name="ano"]');
    const editUltimaTrocaPneusInput = editCarModal.querySelector('input[name="ultima_troca_pneus"]');
    const editUltimaTrocaOleoInput = editCarModal.querySelector('input[name="ultima_troca_oleo"]');
    const editUltimaRevisaoInput = editCarModal.querySelector('input[name="ultima_revisao"]');

    modalTitle.textContent = 'Editar Carro: ' + modelo;
    editChassiInput.value = chassi;
    editModeloInput.value = modelo;
    editAnoInput.value = ano;
    editUltimaTrocaPneusInput.value = ultimaTrocaPneus;
    editUltimaTrocaOleoInput.value = ultimaTrocaOleo;
    editUltimaRevisaoInput.value = ultimaRevisao;
});

function navegar(url) {
    window.location.href = url;
}

function logout() {
    window.location.href = 'index.html';
}

document.getElementById('cadastroForm')?.addEventListener('submit', function(e) {
    e.preventDefault();
    alert('Veículo cadastrado com sucesso!');
});

document.addEventListener('DOMContentLoaded', function() {
    const supportLink = document.getElementById('support-link');
    const supportMessage = document.getElementById('support-message');
    if (supportLink) {
        supportLink.addEventListener('click', function(event) {
            event.preventDefault();
            if (supportMessage.style.display === 'none') {
                supportMessage.style.display = 'block';
            } else {
                supportMessage.style.display = 'none';
            }
        });
    }
});