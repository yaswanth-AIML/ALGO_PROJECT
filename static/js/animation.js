/**
 * AlgoBench — High-performance bar animation engine.
 */
const SortAnimator = (() => {
    let steps = [];
    let currentStep = 0;
    let rafId = null;
    let paused = false;
    let speed = 5;
    let onStepCallback = null;
    let onCompleteCallback = null;
    let maxValue = 1;
    let barElements = [];
    let barWidth = 8;
    let lastFrameTime = 0;
    let reduceMotion = false;

    const container = () => document.getElementById('bars-container');

    function computeBarWidth(count) {
        if (count <= 20) return 28;
        if (count <= 50) return 12;
        return 6;
    }

    function ensureBars(count) {
        const el = container();
        if (!el) return;

        if (barElements.length !== count) {
            el.innerHTML = '';
            barElements = [];
            barWidth = computeBarWidth(count);
            for (let i = 0; i < count; i++) {
                const bar = document.createElement('div');
                bar.className = 'bar';
                bar.style.width = `${barWidth}px`;
                bar.setAttribute('role', 'presentation');
                el.appendChild(bar);
                barElements.push(bar);
            }
        }
    }

    function renderStep(step) {
        const array = step.array;
        ensureBars(array.length);
        const isDone = step.action === 'done';
        const compared = new Set(step.compared || []);
        const swapped = new Set(step.swapped || []);

        array.forEach((value, index) => {
            const bar = barElements[index];
            bar.style.height = `${(value / maxValue) * 100}%`;
            bar.className = 'bar';
            if (isDone) bar.classList.add('sorted');
            else {
                if (compared.has(index)) bar.classList.add('compared');
                if (swapped.has(index)) bar.classList.add('swapped');
            }
            bar.title = `Index ${index}: ${value}`;
            bar.setAttribute('aria-label', `Value ${value} at index ${index}`);
        });
    }

    function getDelay() {
        if (reduceMotion) return 0;
        return Math.max(16, 120 - speed * 11);
    }

    function emitStep() {
        if (currentStep >= steps.length) return;
        const step = steps[currentStep];
        renderStep(step);
        if (onStepCallback) onStepCallback(currentStep + 1, steps.length, step);
    }

    function tick(timestamp) {
        if (paused) return;
        if (currentStep >= steps.length) {
            stop();
            if (onCompleteCallback) onCompleteCallback();
            return;
        }

        const delay = getDelay();
        if (delay === 0 || timestamp - lastFrameTime >= delay) {
            emitStep();
            currentStep += 1;
            lastFrameTime = timestamp;
        }

        if (currentStep < steps.length && !paused) {
            rafId = requestAnimationFrame(tick);
        } else if (currentStep >= steps.length) {
            stop();
            if (onCompleteCallback) onCompleteCallback();
        }
    }

    function goToStep(index) {
        if (!steps.length) return;
        currentStep = Math.max(0, Math.min(index, steps.length - 1));
        emitStep();
    }

    return {
        init(array) {
            maxValue = Math.max(...array, 1);
            ensureBars(array.length);
            renderStep({ array, compared: [], swapped: [], action: 'start' });
        },

        load(newSteps, callbacks = {}) {
            steps = newSteps || [];
            currentStep = 0;
            paused = false;
            onStepCallback = callbacks.onStep || null;
            onCompleteCallback = callbacks.onComplete || null;
            if (steps.length) maxValue = Math.max(...steps[0].array, 1);
            reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        },

        play() {
            paused = false;
            if (rafId) cancelAnimationFrame(rafId);
            if (reduceMotion) {
                while (currentStep < steps.length) {
                    emitStep();
                    currentStep += 1;
                }
                stop();
                if (onCompleteCallback) onCompleteCallback();
                return;
            }
            lastFrameTime = performance.now();
            rafId = requestAnimationFrame(tick);
        },

        pause() {
            paused = true;
            if (rafId) {
                cancelAnimationFrame(rafId);
                rafId = null;
            }
        },

        resume() {
            if (!paused) return;
            paused = false;
            lastFrameTime = performance.now();
            rafId = requestAnimationFrame(tick);
        },

        stepForward() {
            this.pause();
            if (currentStep < steps.length) {
                emitStep();
                currentStep += 1;
            }
        },

        stepBackward() {
            this.pause();
            if (currentStep > 0) {
                currentStep -= 1;
                emitStep();
            }
        },

        reset(array) {
            stop();
            steps = [];
            currentStep = 0;
            barElements = [];
            if (array) this.init(array);
            else if (container()) container().innerHTML = '';
        },

        stop() {
            paused = false;
            if (rafId) {
                cancelAnimationFrame(rafId);
                rafId = null;
            }
        },

        setSpeed(value) {
            speed = value;
        },

        isPaused() {
            return paused;
        },

        isPlaying() {
            return rafId !== null && !paused;
        },

        getStepCount() {
            return steps.length;
        },

        getCurrentStep() {
            return currentStep;
        },
    };
})();
