/**
 * AlgoBench — Chart.js benchmark visualization with export support.
 */
const BenchmarkCharts = (() => {
    const chartInstances = {};
    let lastResults = [];
    const chartColors = [
        'rgba(99, 102, 241, 0.85)',
        'rgba(139, 92, 246, 0.85)',
        'rgba(217, 70, 239, 0.85)',
        'rgba(59, 130, 246, 0.85)',
        'rgba(34, 197, 94, 0.85)',
        'rgba(249, 115, 22, 0.85)',
    ];

    function getThemeColors() {
        const style = getComputedStyle(document.documentElement);
        return {
            tick: style.getPropertyValue('--text-secondary').trim() || '#a1a1aa',
            grid: style.getPropertyValue('--chart-grid').trim() || 'rgba(255,255,255,0.06)',
        };
    }

    function baseOptions() {
        const { tick, grid } = getThemeColors();
        return {
            responsive: true,
            maintainAspectRatio: false,
            animation: { duration: 500, easing: 'easeOutQuart' },
            plugins: { legend: { display: false } },
            scales: {
                x: {
                    ticks: { color: tick, font: { family: 'Inter, sans-serif', size: 11 } },
                    grid: { color: grid },
                },
                y: {
                    ticks: { color: tick, font: { family: 'Inter, sans-serif', size: 11 } },
                    grid: { color: grid },
                    beginAtZero: true,
                },
            },
        };
    }

    function destroyChart(id) {
        if (chartInstances[id]) {
            chartInstances[id].destroy();
            delete chartInstances[id];
        }
    }

    function createBarChart(canvasId, label, labels, data) {
        destroyChart(canvasId);
        const canvas = document.getElementById(canvasId);
        if (!canvas) return;

        chartInstances[canvasId] = new Chart(canvas, {
            type: 'bar',
            data: {
                labels,
                datasets: [{
                    label,
                    data,
                    backgroundColor: chartColors,
                    borderColor: chartColors.map((c) => c.replace('0.85', '1')),
                    borderWidth: 1,
                    borderRadius: 8,
                    borderSkipped: false,
                }],
            },
            options: baseOptions(),
        });
    }

    function updateTable(results) {
        const tbody = document.querySelector('#benchmark-table tbody');
        if (!tbody) return;

        tbody.innerHTML = results.map((r) => {
            const timeMs = (r.execution_time * 1000).toFixed(3);
            const status = r.verified ? 'Verified' : 'Check';
            const statusClass = r.verified ? 'status-ok' : 'status-warn';
            return `
                <tr>
                    <td>${r.algorithm}</td>
                    <td>${timeMs}</td>
                    <td>${r.comparisons.toLocaleString()}</td>
                    <td>${r.swaps.toLocaleString()}</td>
                    <td class="${statusClass}">${status}</td>
                </tr>
            `;
        }).join('');
    }

    function exportCsv() {
        if (!lastResults.length) return null;
        const header = 'Algorithm,Time(ms),Comparisons,Swaps,Verified\n';
        const rows = lastResults.map((r) => [
            `"${r.algorithm}"`,
            (r.execution_time * 1000).toFixed(3),
            r.comparisons,
            r.swaps,
            r.verified ? 'true' : 'false',
        ].join(',')).join('\n');
        return header + rows;
    }

    function downloadCsv() {
        const csv = exportCsv();
        if (!csv) return false;
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.download = `algobench-benchmark-${Date.now()}.csv`;
        link.click();
        URL.revokeObjectURL(url);
        return true;
    }

    function exportChartPng(canvasId, filename) {
        const canvas = document.getElementById(canvasId);
        if (!canvas) return false;
        const link = document.createElement('a');
        link.href = canvas.toDataURL('image/png');
        link.download = filename;
        link.click();
        return true;
    }

    return {
        render(results) {
            if (!results?.length) return;
            lastResults = results;

            const labels = results.map((r) => r.algorithm);
            createBarChart('chart-time', 'Execution Time (ms)', labels,
                results.map((r) => +(r.execution_time * 1000).toFixed(3)));
            createBarChart('chart-comparisons', 'Comparisons', labels,
                results.map((r) => r.comparisons));
            createBarChart('chart-swaps', 'Swaps / Writes', labels,
                results.map((r) => r.swaps));
            updateTable(results);
        },

        clear() {
            ['chart-time', 'chart-comparisons', 'chart-swaps'].forEach(destroyChart);
            lastResults = [];
            const tbody = document.querySelector('#benchmark-table tbody');
            if (tbody) tbody.innerHTML = '';
        },

        downloadCsv,
        exportChartPng,
        getLastResults: () => lastResults,
    };
})();
