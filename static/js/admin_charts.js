document.addEventListener('DOMContentLoaded', function() {
    // Crime Types Chart
    const crimeTypeChart = new Chart(
        document.getElementById('crimeTypeChart').getContext('2d'),
        {
            type: 'doughnut',
            data: {
                labels: chartData.crime_types.map(item => item.crime_type),
                datasets: [{
                    data: chartData.crime_types.map(item => item.count),
                    backgroundColor: [
                        '#48cae4', '#00b4d8', '#0096c7', '#0077b6', '#023e8a'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    );

    // Trend Chart
    const trendChart = new Chart(
        document.getElementById('trendChart').getContext('2d'),
        {
            type: 'line',
            data: {
                labels: chartData.monthly_trends.map(item => 
                    new Date(2024, item.created_at__month - 1).toLocaleString('default', { month: 'short' })
                ),
                datasets: [{
                    label: 'Number of Cases',
                    data: chartData.monthly_trends.map(item => item.count),
                    borderColor: '#0096c7',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false
            }
        }
    );
});
