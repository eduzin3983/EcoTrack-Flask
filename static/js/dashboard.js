document.addEventListener('DOMContentLoaded', function () {
  const dataEl = document.getElementById('chart-data');
  const chartData = JSON.parse(dataEl.textContent);
  const ctx = document.getElementById('metricsChart').getContext('2d');
  const metricsChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Água', 'Energia', 'Resíduos'],
      datasets: [{
        label: 'Consumo (últimos 7 dias)',
        data: [
          chartData.agua, 
          chartData.energia, 
          chartData.residuos, 
        ],
        backgroundColor: [
          '#BCDBE5', // Água
          '#E7BC66', // Energia
          '#9BAD87', // Resíduos
        ],
        borderColor: [
          '#BCDBE5',
          '#E7BC66',
          '#9BAD87',
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

  // Código do modal de ajuda
  const helpIcon = document.getElementById('helpIcon');
  const helpModal = document.getElementById('helpModal');
  const closeHelpModal = document.getElementById('closeHelpModal');

  helpIcon.addEventListener('click', () => {
    helpModal.style.display = 'block';
  });

  closeHelpModal.addEventListener('click', () => {
    helpModal.style.display = 'none';
  });

  window.addEventListener('click', (event) => {
    if (event.target === helpModal) {
      helpModal.style.display = 'none';
    }
  });
});
