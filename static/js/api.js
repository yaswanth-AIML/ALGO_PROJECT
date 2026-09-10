/**
 * AlgoBench — Fetch wrapper with consistent error handling.
 */
const ApiClient = (() => {
    async function request(url, options = {}) {
        const response = await fetch(url, {
            headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
            ...options,
        });

        let data;
        try {
            data = await response.json();
        } catch {
            throw new Error(`Invalid JSON response (${response.status})`);
        }

        if (!response.ok || data.success === false) {
            throw new Error(data.error || `Request failed (${response.status})`);
        }

        return data;
    }

    return {
        get: (url) => request(url),
        post: (url, body) => request(url, { method: 'POST', body: JSON.stringify(body) }),
    };
})();
