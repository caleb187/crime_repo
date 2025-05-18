document.addEventListener('DOMContentLoaded', function() {
    initPriorityChart();
    initCrimeTypesChart();
    initCrimeMap();
});

function initPriorityChart() {
    const ctx = document.getElementById('priorityChart').getContext('2d');
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: priorityData.map(d => `Priority ${d.priority}`),
            datasets: [{
                data: priorityData.map(d => d.count),
                backgroundColor: [
                    '#48cae4',
                    '#00b4d8',
                    '#0096c7',
                    '#0077b6',
                    '#023e8a'
                ]
            }]
        }
    });
}

function initCrimeTypesChart() {
    const ctx = document.getElementById('crimeTypesTrend').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: crimeTypesData.map(d => d.crime_type),
            datasets: [{
                label: 'Number of Cases',
                data: crimeTypesData.map(d => d.count),
                backgroundColor: '#0096c7'
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
}

function initCrimeMap() {
    const map = L.map('crimeMap').setView([0, 0], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
    
    // Add markers for hotspots
    crimeHotspots.forEach(hotspot => {
        L.marker([hotspot.lat, hotspot.lng])
         .bindPopup(`${hotspot.location}: ${hotspot.count} cases`)
         .addTo(map);
    });
}

function updateAnalytics(days) {
    fetch(`/admin/crimes/analytics/?days=${days}`)
        .then(response => response.json())
        .then(data => {
            // Update charts and statistics
            updateCharts(data);
            updateStats(data);
        });
}
