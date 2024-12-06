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

document.addEventListener('DOMContentLoaded', function() {
    const editCarModal = document.getElementById('editCarModal');
    editCarModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const chassi = button.getAttribute('data-chassi');
        const modelo = button.getAttribute('data-modelo');
        const ano = button.getAttribute('data-ano');
        const placa = button.getAttribute('data-placa');
        const ultimaTrocaPneus = button.getAttribute('data-ultima_troca_pneus');
        const ultimaTrocaOleo = button.getAttribute('data-ultima_troca_oleo');
        const ultimaRevisao = button.getAttribute('data-ultima_revisao');
        const ultimaTrocaVela = button.getAttribute('data-ultima_troca_vela');
        const ultimaTrocaCaixaCambio = button.getAttribute('data-ultima_troca_caixa_cambio');
        const ultimaTrocaSuspensao = button.getAttribute('data-ultima_troca_suspensao');
        const ultimaTrocaBateria = button.getAttribute('data-ultima_troca_bateria');
        const validadeBateria = button.getAttribute('data-validade_bateria');
        const ultimaTrocaCorreiaDentada = button.getAttribute('data-ultima_troca_correia_dentada');
        const proximaRevisao = button.getAttribute('data-proxima_revisao');

        const editChassiInput = document.getElementById('editChassi');
        const editModeloInput = document.getElementById('editModelo');
        const editAnoInput = document.getElementById('editAno');
        const editPlacaInput = document.getElementById('editPlaca');
        const editUltimaTrocaPneusInput = document.getElementById('editUltimaTrocaPneus');
        const editUltimaTrocaOleoInput = document.getElementById('editUltimaTrocaOleo');
        const editUltimaRevisaoInput = document.getElementById('editUltimaRevisao');
        const editUltimaTrocaVelaInput = document.getElementById('editUltimaTrocaVela');
        const editUltimaTrocaCaixaCambioInput = document.getElementById('editUltimaTrocaCaixaCambio');
        const editUltimaTrocaSuspensaoInput = document.getElementById('editUltimaTrocaSuspensao');
        const editUltimaTrocaBateriaInput = document.getElementById('editUltimaTrocaBateria');
        const editValidadeBateriaInput = document.getElementById('editValidadeBateria');
        const editUltimaTrocaCorreiaDentadaInput = document.getElementById('editUltimaTrocaCorreiaDentada');
        const editProximaRevisaoInput = document.getElementById('editProximaRevisao');

        editChassiInput.value = chassi;
        editModeloInput.value = modelo;
        editAnoInput.value = ano;
        editPlacaInput.value = placa;
        editUltimaTrocaPneusInput.value = ultimaTrocaPneus;
        editUltimaTrocaOleoInput.value = ultimaTrocaOleo;
        editUltimaRevisaoInput.value = ultimaRevisao;
        editUltimaTrocaVelaInput.value = ultimaTrocaVela;
        editUltimaTrocaCaixaCambioInput.value = ultimaTrocaCaixaCambio;
        editUltimaTrocaSuspensaoInput.value = ultimaTrocaSuspensao;
        editUltimaTrocaBateriaInput.value = ultimaTrocaBateria;
        editValidadeBateriaInput.value = validadeBateria;
        editUltimaTrocaCorreiaDentadaInput.value = ultimaTrocaCorreiaDentada;
        editProximaRevisaoInput.value = proximaRevisao;
    });

    const detailsCarModal = document.getElementById('detailsCarModal');
    detailsCarModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const chassi = button.getAttribute('data-chassi');
        const modelo = button.getAttribute('data-modelo');
        const ano = button.getAttribute('data-ano');
        const placa = button.getAttribute('data-placa');
        const ultimaTrocaPneus = button.getAttribute('data-ultima_troca_pneus');
        const ultimaTrocaOleo = button.getAttribute('data-ultima_troca_oleo');
        const ultimaRevisao = button.getAttribute('data-ultima_revisao');
        const ultimaTrocaVela = button.getAttribute('data-ultima_troca_vela');
        const ultimaTrocaCaixaCambio = button.getAttribute('data-ultima_troca_caixa_cambio');
        const ultimaTrocaSuspensao = button.getAttribute('data-ultima_troca_suspensao');
        const ultimaTrocaBateria = button.getAttribute('data-ultima_troca_bateria');
        const validadeBateria = button.getAttribute('data-validade_bateria');
        const ultimaTrocaCorreiaDentada = button.getAttribute('data-ultima_troca_correia_dentada');
        const proximaRevisao = button.getAttribute('data-proxima_revisao');

        const detailsChassi = document.getElementById('detailsChassi');
        const detailsModelo = document.getElementById('detailsModelo');
        const detailsAno = document.getElementById('detailsAno');
        const detailsPlaca = document.getElementById('detailsPlaca');
        const detailsUltimaTrocaPneus = document.getElementById('detailsUltimaTrocaPneus');
        const detailsUltimaTrocaOleo = document.getElementById('detailsUltimaTrocaOleo');
        const detailsUltimaRevisao = document.getElementById('detailsUltimaRevisao');
        const detailsUltimaTrocaVela = document.getElementById('detailsUltimaTrocaVela');
        const detailsUltimaTrocaCaixaCambio = document.getElementById('detailsUltimaTrocaCaixaCambio');
        const detailsUltimaTrocaSuspensao = document.getElementById('detailsUltimaTrocaSuspensao');
        const detailsUltimaTrocaBateria = document.getElementById('detailsUltimaTrocaBateria');
        const detailsValidadeBateria = document.getElementById('detailsValidadeBateria');
        const detailsUltimaTrocaCorreiaDentada = document.getElementById('detailsUltimaTrocaCorreiaDentada');
        const detailsProximaRevisao = document.getElementById('detailsProximaRevisao');

        detailsChassi.textContent = chassi;
        detailsModelo.textContent = modelo;
        detailsAno.textContent = ano;
        detailsPlaca.textContent = placa;
        detailsUltimaTrocaPneus.textContent = ultimaTrocaPneus;
        detailsUltimaTrocaOleo.textContent = ultimaTrocaOleo;
        detailsUltimaRevisao.textContent = ultimaRevisao;
        detailsUltimaTrocaVela.textContent = ultimaTrocaVela;
        detailsUltimaTrocaCaixaCambio.textContent = ultimaTrocaCaixaCambio;
        detailsUltimaTrocaSuspensao.textContent = ultimaTrocaSuspensao;
        detailsUltimaTrocaBateria.textContent = ultimaTrocaBateria;
        detailsValidadeBateria.textContent = validadeBateria;
        detailsUltimaTrocaCorreiaDentada.textContent = ultimaTrocaCorreiaDentada;
        detailsProximaRevisao.textContent = proximaRevisao;
    });
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
