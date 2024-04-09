// Function to create charts
export function createChart(ctx, chartData, chartType) {
    return new Chart(ctx, {
        type: chartType,
        data: chartData,
        options: {
            scales: {
                y: {
                    beginAtZero: true
                    
                }
            }
        }
    });
}
// Function to prepare chart data for food and sustainable categories
function prepareChartData(data) {
    const labels = data.map(item => item.category_name);
    const counts = data.map(item => item.listing_count);
    return {
        labels: labels,
        datasets: [{
            label: 'Number of List',
            data: counts,
            backgroundColor: 'rgba(54, 162, 235, 0.5)',
            borderColor: 'rgba(54, 162, 235, 1)',
            borderWidth: 1
        }]
    };
}

// Function to prepare chart data for user category
function prepareUserData(data) {
    const labels = ['Active Users', 'Banned Users', 'Non-Approved Users'];
    const counts = [data.number_of_active_user, data.number_of_banned_user, data.number_of_non_approved_user];
    return {
        labels: labels,
        datasets: [{
            label: 'User Count',
            data: counts,
            backgroundColor: [
                'rgba(255, 99, 132, 0.5)',
                'rgba(54, 162, 235, 0.5)',
                'rgba(255, 206, 86, 0.5)'
            ],
            borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)'
            ],
            borderWidth: 1
        }]
    };
}
