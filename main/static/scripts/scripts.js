/**
 * Calculate the luminance of a given RGB color.
 * @param {string} color - The RGB color in the format 'rgb(r, g, b)'.
 * @returns {number} The luminance value of the color.
 */
function getLuminance(color) {
    const rgb = color.match(/\d+/g);
    const r = parseInt(rgb[0]), g = parseInt(rgb[1]), b = parseInt(rgb[2]);
    const luminance = 0.2126 * (r / 255) + 0.7152 * (g / 255) + 0.0722 * (b / 255);
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
    // Ensure Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded. Please include the Chart.js library.');
        return;
    }

    const yearSelect = document.getElementById('year');
    const currentYear = new Date().getFullYear();

    // Preencher o select com os anos disponíveis
    fetch('/available_years')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.year;
                option.textContent = item.year;
                yearSelect.appendChild(option);
            });

            // Selecionar o ano atual por padrão
            yearSelect.value = currentYear;
            updateChart(currentYear);
        })
        .catch(error => console.error('Erro ao buscar anos disponíveis:', error));

    yearSelect.addEventListener('change', function() {
        const selectedYear = yearSelect.value;
        updateChart(selectedYear);
    });

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
};

const editCarModal = document.getElementById('editCarModal');
if (editCarModal) {
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
        const scannerInstalado = button.getAttribute('data-scanner_instalado');

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
        const editScannerInstaladoInput = document.getElementById('editScannerInstalado');

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
        editScannerInstaladoInput.value = scannerInstalado;
    });
}

const detailsCarModal = document.getElementById('detailsCarModal');
if (detailsCarModal) {
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

        document.getElementById('detailsChassi').textContent = chassi;
        document.getElementById('detailsModelo').textContent = modelo;
        document.getElementById('detailsAno').textContent = ano;
        document.getElementById('detailsPlaca').textContent = placa;
        document.getElementById('detailsUltimaTrocaPneus').textContent = ultimaTrocaPneus;
        document.getElementById('detailsUltimaTrocaOleo').textContent = ultimaTrocaOleo;
        document.getElementById('detailsUltimaRevisao').textContent = ultimaRevisao;
        document.getElementById('detailsUltimaTrocaVela').textContent = ultimaTrocaVela;
        document.getElementById('detailsUltimaTrocaCaixaCambio').textContent = ultimaTrocaCaixaCambio;
        document.getElementById('detailsUltimaTrocaSuspensao').textContent = ultimaTrocaSuspensao;
        document.getElementById('detailsUltimaTrocaBateria').textContent = ultimaTrocaBateria;
        document.getElementById('detailsValidadeBateria').textContent = validadeBateria;
        document.getElementById('detailsUltimaTrocaCorreiaDentada').textContent = ultimaTrocaCorreiaDentada;
        document.getElementById('detailsProximaRevisao').textContent = proximaRevisao;
    });
}

const supportLink = document.getElementById('support-link');
const supportMessage = document.getElementById('support-message');
if (supportLink && supportMessage) {
    supportLink.addEventListener('click', function(event) {
        event.preventDefault();
        supportMessage.style.display = 'block';
    });
}

const cadastroForm = document.getElementById('cadastroForm');
if (cadastroForm) {
    cadastroForm.addEventListener('submit', function(e) {
        e.preventDefault();
        alert('Veículo cadastrado com sucesso!');
    });
}

const supportLink2 = document.getElementById('support-link');
const supportMessage2 = document.getElementById('support-message');
if (supportLink2 && supportMessage2) {
    supportLink2.addEventListener('click', function(event) {
        event.preventDefault();
        if (supportMessage2.style.display === 'none') {
            supportMessage2.style.display = 'block';
        } else {
            supportMessage2.style.display = 'none';
        }
    });
}

const solicitarModificacaoModal = document.getElementById('solicitarModificacaoModal');
if (solicitarModificacaoModal) {
    solicitarModificacaoModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const chassi = button.getAttribute('data-chassi');
        const modificacaoChassiInput = document.getElementById('modificacaoChassi');
        modificacaoChassiInput.value = chassi;
    });
}

function navegar(url) {
    window.location.href = url;
}

function logout() {
    window.location.href = 'index.html';
}