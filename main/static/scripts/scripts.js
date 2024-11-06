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
                updateMonths(data[0].year);
                updateChart(data[0].year, 1); // Inicializa com o primeiro mês do primeiro ano disponível
            }
        })
        .catch(error => console.error('Erro ao buscar anos disponíveis:', error));

    document.getElementById('year').addEventListener('change', function() {
        const year = this.value;
        updateMonths(year);
    });

    document.getElementById('updateChart').addEventListener('click', function() {
        const month = document.getElementById('month').value;
        const year = document.getElementById('year').value;
        updateChart(year, month);
    });
};

function updateMonths(year) {
    fetch(`/available_months?year=${year}`)
        .then(response => response.json())
        .then(data => {
            const monthSelect = document.getElementById('month');
            monthSelect.innerHTML = ''; // Limpa as opções anteriores

            data.forEach(item => {
                const option = document.createElement('option');
                option.value = item.month;
                option.textContent = new Date(0, item.month - 1).toLocaleString('pt-BR', { month: 'long' });
                monthSelect.appendChild(option);
            });

            // Inicializa o gráfico com o primeiro mês disponível para o ano selecionado
            if (data.length > 0) {
                updateChart(year, data[0].month);
            }
        })
        .catch(error => console.error('Erro ao buscar meses disponíveis:', error));
}

function updateChart(year, month) {
    fetch(`/data?month=${month}&year=${year}`)
        .then(response => response.json())
        .then(data => {
            console.log('Dados recebidos:', data); // Adicione este log para verificar os dados recebidos

            const labels = data.map(item => item.type);
            const counts = data.map(item => item.count);

            const ctx = document.getElementById('myChart').getContext('2d');

            // Destruir o gráfico existente antes de criar um novo
            if (myChart) {
                myChart.destroy();
            }

            myChart = new Chart(ctx, {
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
}

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