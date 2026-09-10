let statusChart = null;

function initChart() {
    const ctx = document.getElementById('statusChart').getContext('2d');
    statusChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Granted', 'Denied'],
            datasets: [{
                data: [0, 0],
                backgroundColor: ['#4ade80', '#f87171'],
                borderWidth: 0
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: { color: '#c7cee0' }
                }
            }
        }
    });
}

function updateFeed(events) {
    const tbody = document.getElementById('feed-body');
    tbody.innerHTML = '';

    if (events.length === 0) {
        tbody.innerHTML = '<tr><td colspan="3" style="text-align:center; color:#565e70;">No scans yet — walk up to the camera!</td></tr>';
        return;
    }

    events.forEach(ev => {
        const row = document.createElement('tr');
        const statusClass = ev.status === 'GRANTED' ? 'status-granted' : 'status-denied';
        row.innerHTML = `
            <td>${ev.timestamp}</td>
            <td>${ev.name}</td>
            <td class="${statusClass}">${ev.status}</td>
        `;
        tbody.appendChild(row);
    });
}

async function refreshDashboard() {
    try {
        const res = await fetch('/api/events');
        const data = await res.json();

        document.getElementById('stat-total').textContent = data.total;
        document.getElementById('stat-granted').textContent = data.granted;
        document.getElementById('stat-denied').textContent = data.denied;

        statusChart.data.datasets[0].data = [data.granted, data.denied];
        statusChart.update();

        updateFeed(data.recent);
    } catch (err) {
        console.error('Failed to refresh dashboard:', err);
    }
}

window.addEventListener('DOMContentLoaded', () => {
    initChart();
    refreshDashboard();
    setInterval(refreshDashboard, REFRESH_MS);
});
