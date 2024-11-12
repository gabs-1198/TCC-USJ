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

 
const ctx = document.getElementById('lineChart').getContext('2d');

const lineChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'],
        datasets: [{
            label: 'Detalhes Gerais Mensais',
            data: [120, 150, 180, 200, 170, 160, 210, 230, 220, 190, 180, 250],
            backgroundColor: 'rgba(0, 123, 255, 0.2)',
            borderColor: 'rgba(0, 123, 255, 1)',
            borderWidth: 2,
            pointBackgroundColor: 'rgba(255, 255, 255, 1)',
            pointBorderColor: 'rgba(0, 123, 255, 1)',
            pointRadius: 5
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                labels: {
                    color: 'white'
                }
            },
            tooltip: {
                enabled: true,
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: 'white',
                bodyColor: 'white'
            }
        },
        scales: {
            x: {
                ticks: {
                    color: 'white'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            },
            y: {
                beginAtZero: true,
                ticks: {
                    color: 'white'
                },
                grid: {
                    color: 'rgba(255, 255, 255, 0.1)'
                }
            }
        }
    }
});

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