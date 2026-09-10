/**
 * AlgoBench — Main application controller.
 */
(() => {
    'use strict';

    let currentArray = [];
    let algorithms = [];
    let sortResult = null;
    let limits = { max_array_size: 150 };

    const $ = (sel) => document.querySelector(sel);

    function showToast(message, isError = false) {
        const toast = $('#toast');
        toast.textContent = message;
        toast.classList.toggle('error', isError);
        toast.classList.remove('hidden');
        clearTimeout(showToast._timer);
        showToast._timer = setTimeout(() => toast.classList.add('hidden'), 3200);
    }

    function setLoading(loading, label = 'Processing...') {
        const overlay = $('#loading-overlay');
        if (overlay) {
            overlay.classList.toggle('hidden', !loading);
            overlay.querySelector('.loading-text').textContent = label;
        }
        ['btn-generate', 'btn-sort', 'btn-benchmark', 'btn-reset'].forEach((id) => {
            const btn = $(`#${id}`);
            if (btn) btn.disabled = loading;
        });
    }

    function updateStats({ step = 0, total = 0, comparisons = 0, swaps = 0, time = 0 } = {}) {
        $('#stat-step').textContent = `${step} / ${total}`;
        $('#stat-comparisons').textContent = comparisons.toLocaleString();
        $('#stat-swaps').textContent = swaps.toLocaleString();
        $('#stat-time').textContent = `${(time * 1000).toFixed(2)} ms`;
    }

    function updateComplexity(cx) {
        if (!cx) return;
        $('#cx-best').textContent = cx.best_case;
        $('#cx-average').textContent = cx.average_case;
        $('#cx-worst').textContent = cx.worst_case;
        $('#cx-space').textContent = cx.space_complexity;
        $('#algo-description').textContent = cx.description || 'Select an algorithm to view details.';

        const stableEl = $('#cx-stable');
        stableEl.textContent = cx.stable ? 'Yes' : 'No';
        stableEl.className = `value badge${cx.stable ? '' : ' no'}`;

        const inplaceEl = $('#cx-inplace');
        inplaceEl.textContent = cx.in_place ? 'Yes' : 'No';
        inplaceEl.className = `value badge${cx.in_place ? '' : ' no'}`;
    }

    function setAnimationControls(playing, paused = false) {
        $('#btn-pause').disabled = !playing || paused;
        $('#btn-resume').disabled = !playing || !paused;
        $('#btn-prev').disabled = !sortResult?.steps?.length;
        $('#btn-next').disabled = !sortResult?.steps?.length;
        $('#btn-sort').disabled = playing && !paused;
    }

    async function fetchAlgorithms() {
        try {
            const data = await ApiClient.get('/api/algorithms');
            algorithms = data.algorithms;
            limits = data.limits || limits;

            const sizeInput = $('#size-input');
            sizeInput.max = limits.max_array_size;

            $('#algorithm-select').innerHTML = algorithms.map((a) =>
                `<option value="${a.name}">${a.name}</option>`).join('');

            $('#type-select').innerHTML = data.array_types.map((t) =>
                `<option value="${t.key}">${t.label}</option>`).join('');

            if (algorithms.length) updateComplexity(algorithms[0]);
        } catch (err) {
            showToast(err.message || 'Failed to load algorithms.', true);
        }
    }

    async function generateArray() {
        const size = parseInt($('#size-input').value, 10);
        const arrayType = $('#type-select').value;

        setLoading(true, 'Generating array...');
        SortAnimator.stop();
        SortAnimator.reset();

        try {
            const data = await ApiClient.post('/generate', { size, array_type: arrayType });
            currentArray = data.array;
            sortResult = null;
            SortAnimator.init(currentArray);
            updateStats();
            $('#array-info').textContent = `${data.array_type} · ${currentArray.length} elements`;
            setAnimationControls(false);
            showToast('Array generated successfully.');
        } catch (err) {
            showToast(err.message, true);
        } finally {
            setLoading(false);
        }
    }

    async function sortArray() {
        if (!currentArray.length) {
            showToast('Generate an array first.', true);
            return;
        }

        const algorithm = $('#algorithm-select').value;
        setLoading(true, `Running ${algorithm}...`);
        SortAnimator.stop();

        try {
            const data = await ApiClient.post('/sort', { algorithm, array: currentArray });
            sortResult = data.result;
            updateComplexity(data.complexity);

            const totalSteps = sortResult.steps?.length || 0;
            updateStats({
                step: 0,
                total: totalSteps,
                comparisons: sortResult.comparisons,
                swaps: sortResult.swaps,
                time: sortResult.execution_time,
            });

            if (sortResult.steps_recorded && sortResult.steps_recorded > totalSteps) {
                showToast(`Showing ${totalSteps} sampled frames of ${sortResult.steps_recorded} operations.`);
            }

            SortAnimator.load(sortResult.steps, {
                onStep: (step, total) => {
                    updateStats({
                        step, total,
                        comparisons: sortResult.comparisons,
                        swaps: sortResult.swaps,
                        time: sortResult.execution_time,
                    });
                },
                onComplete: () => {
                    setAnimationControls(false);
                    showToast(`${algorithm} completed.`);
                },
            });

            setAnimationControls(true, false);
            SortAnimator.play();
        } catch (err) {
            showToast(err.message, true);
        } finally {
            setLoading(false);
        }
    }

    async function runBenchmark() {
        if (!currentArray.length) {
            showToast('Generate an array first.', true);
            return;
        }

        setLoading(true, 'Benchmarking all algorithms...');

        try {
            const data = await ApiClient.post('/benchmark', { array: currentArray });
            switchView('benchmark');
            BenchmarkCharts.render(data.benchmark.results);
            $('#benchmark-subtitle').textContent =
                `Benchmarked ${data.benchmark.array_size} elements across ${data.benchmark.results.length} algorithms`;
            showToast('Benchmark complete.');
        } catch (err) {
            showToast(err.message, true);
        } finally {
            setLoading(false);
        }
    }

    function switchView(viewName) {
        document.querySelectorAll('.nav-link').forEach((link) => {
            link.classList.toggle('active', link.dataset.view === viewName);
            link.setAttribute('aria-selected', link.dataset.view === viewName);
        });
        document.querySelectorAll('.view').forEach((view) => {
            view.classList.toggle('active', view.id === `view-${viewName}`);
        });
    }

    function resetAll() {
        SortAnimator.stop();
        SortAnimator.reset();
        currentArray = [];
        sortResult = null;
        updateStats();
        $('#array-info').textContent = 'Generate an array to begin';
        setAnimationControls(false);
        BenchmarkCharts.clear();
        showToast('Reset complete.');
    }

    function bindEvents() {
        $('#size-input').addEventListener('input', (e) => {
            $('#size-value').textContent = e.target.value;
        });

        $('#speed-input').addEventListener('input', (e) => {
            const val = parseInt(e.target.value, 10);
            $('#speed-value').textContent = val;
            SortAnimator.setSpeed(val);
        });

        $('#algorithm-select').addEventListener('change', (e) => {
            const algo = algorithms.find((a) => a.name === e.target.value);
            if (algo) updateComplexity(algo);
        });

        document.querySelectorAll('.nav-link').forEach((link) => {
            link.addEventListener('click', () => switchView(link.dataset.view));
        });

        $('#btn-generate').addEventListener('click', generateArray);
        $('#btn-sort').addEventListener('click', sortArray);
        $('#btn-benchmark').addEventListener('click', runBenchmark);
        $('#btn-pause').addEventListener('click', () => {
            SortAnimator.pause();
            setAnimationControls(true, true);
        });
        $('#btn-resume').addEventListener('click', () => {
            SortAnimator.resume();
            setAnimationControls(true, false);
        });
        $('#btn-prev').addEventListener('click', () => {
            SortAnimator.stepBackward();
            setAnimationControls(true, true);
        });
        $('#btn-next').addEventListener('click', () => {
            SortAnimator.stepForward();
            setAnimationControls(true, true);
        });
        $('#btn-reset').addEventListener('click', resetAll);
        $('#btn-export-csv').addEventListener('click', () => {
            if (BenchmarkCharts.downloadCsv()) showToast('CSV exported.');
            else showToast('Run a benchmark first.', true);
        });
        $('#btn-export-chart').addEventListener('click', () => {
            if (BenchmarkCharts.exportChartPng('chart-time', 'algobench-time.png')) {
                showToast('Chart exported as PNG.');
            } else {
                showToast('Run a benchmark first.', true);
            }
        });
    }

    document.addEventListener('DOMContentLoaded', () => {
        bindEvents();
        fetchAlgorithms();
        SortAnimator.setSpeed(parseInt($('#speed-input').value, 10));
        setAnimationControls(false);
    });
})();
