// Scripts para o AIEngine
// src/assets/js/aiengine-scripts.js

document.addEventListener('DOMContentLoaded', function() {

  // Inicialização do gráfico de métricas com dados dinâmicos
  if (document.querySelector("#metrics-chart")) {
      const performanceData = JSON.parse(document.getElementById('performanceData').textContent);
      const performanceDates = JSON.parse(document.getElementById('performanceDates').textContent);

      const chartOptions = {
          chart: { type: 'line', height: 300 },
          series: [{ name: 'Performance', data: performanceData }],
          xaxis: { categories: performanceDates },
          colors: ['#3498db'],
          markers: { size: 4 },
          stroke: { width: 2 },
          dataLabels: { enabled: false },
          tooltip: { theme: 'dark' }
      };

      const chart = new ApexCharts(document.querySelector("#metrics-chart"), chartOptions);
      chart.render();
  }

  // Tabela dinâmica para os logs
  if (document.querySelector("#logs-table")) {
      $('#logs-table').DataTable({
          responsive: true,
          searching: true,
          paging: true,
          info: true,
          autoWidth: false,
          language: {
              search: "Pesquisar:",
              paginate: { next: "Próximo", previous: "Anterior" },
              lengthMenu: "Mostrar _MENU_ logs por página"
          }
      });
  }

  // Tabela para gerenciar módulos
  if (document.querySelector("#models-table")) {
      $('#models-table').DataTable({
          responsive: true,
          searching: true,
          paging: true,
          info: true,
          autoWidth: false
      });
  }

  // Função para abrir modal de adição de novos modelos
  window.openAddModelModal = function() {
      const modal = document.getElementById('addModelModal');
      if (modal) {
          modal.style.display = 'block';
      }
  }

  // Função para fechar modais
  document.querySelectorAll('.modal-close').forEach(btn => {
      btn.addEventListener('click', function() {
          this.closest('.modal').style.display = 'none';
      });
  });

  // Animação e efeito de hover nos botões
  document.querySelectorAll('.btn-primary').forEach(button => {
      button.addEventListener('mouseover', function() {
          this.style.transition = '0.3s';
          this.style.transform = 'scale(1.05)';
      });
      button.addEventListener('mouseout', function() {
          this.style.transform = 'scale(1)';
      });
  });

  // Atualização de status de contêiner em tempo real
  if (document.querySelector("#container-status-table")) {
      setInterval(() => {
          fetch('/app/aiengine/container-status/')
              .then(response => response.json())
              .then(data => {
                  // Atualiza o status de cada contêiner na tabela
                  const tableBody = document.querySelector("#container-status-table tbody");
                  tableBody.innerHTML = ""; // Limpa a tabela
                  data.containers.forEach(container => {
                      const row = `<tr>
                          <td>${container.name}</td>
                          <td>${container.status}</td>
                          <td>${container.image}</td>
                      </tr>`;
                      tableBody.insertAdjacentHTML('beforeend', row);
                  });
              })
              .catch(error => console.error('Erro ao atualizar status dos contêineres:', error));
      }, 10000); // Atualiza a cada 10 segundos
  }

});
