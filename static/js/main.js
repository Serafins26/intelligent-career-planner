// Main JS for subtle animations and future dashboards
// - Smoothly animate progress bars on load
// - Placeholder for Chart.js dashboards

(function () {
  // Animate all .progress > span widths
  const bars = document.querySelectorAll('.progress > span');
  bars.forEach((bar) => {
    const target = bar.style.width || '0%';
    bar.style.width = '0%';
    requestAnimationFrame(() => {
      bar.style.transition = 'width 700ms ease-out';
      bar.style.width = target;
    });
  });

  // Example Chart.js setup (uncomment when canvas exists)
  // const ctx = document.getElementById('kpiChart');
  // if (ctx) {
  //   new Chart(ctx, {
  //     type: 'bar',
  //     data: { labels: ['Q1','Q2','Q3','Q4'], datasets: [{ label: 'Horas', data: [10, 20, 15, 25], backgroundColor: '#60a5fa' }] },
  //     options: { responsive: true, plugins: { legend: { display: false } } }
  //   });
  // }
  // Close week-dropdown menus when clicking outside
  document.addEventListener('click', function (e) {
    if (!e.target.closest('.week-dropdown')) {
      document.querySelectorAll('.week-menu.show').forEach(function (m) {
        m.classList.remove('show');
      });
    }
  });
})();
