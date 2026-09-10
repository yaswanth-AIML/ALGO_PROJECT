# AlgoBench

**Production-grade sorting algorithm visualizer and benchmark suite.**

AlgoBench is a full-stack web application for exploring, visualizing, and benchmarking six classic sorting algorithms. Built with Flask and a modern glassmorphism UI, it demonstrates clean architecture, algorithm instrumentation, and performance analysis suitable for portfolio and technical interviews.

---

## Highlights

- **6 sorting algorithms** with step-by-step bar visualization
- **Benchmark suite** with averaged timing, comparison counts, and verification
- **Modular Flask architecture** — blueprints, services, validation, config
- **Optimized animations** — DOM reuse, `requestAnimationFrame`, step thinning
- **Accessible UI** — ARIA live regions, keyboard focus, reduced-motion support
- **Export tools** — CSV results and PNG chart export

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Flask |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js (CDN) |
| Testing | pytest |
| Production | Gunicorn |

---

## Quick Start

```bash
git clone https://github.com/yourusername/AlgoBench.git
cd AlgoBench

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
python app.py
```

Open **http://127.0.0.1:5000**

### Production

```bash
set FLASK_DEBUG=false
gunicorn -w 2 -b 0.0.0.0:5000 app:app
```

---

## Architecture

```
AlgoBench/
├── app.py                 # Application factory
├── config.py              # Environment-driven config
├── errors.py              # Global error handlers
├── routes/                # Blueprints (pages + API)
├── services/              # Business logic + validation
├── algorithms/            # Sort implementations + StepTracker
├── registry/              # Algorithm metadata registry
├── benchmark/             # Timing + complexity helpers
├── utils/                 # Array generation
├── templates/             # Jinja templates
├── static/                # CSS + modular JS
└── tests/                 # Unit + API integration tests
```

---

## API Reference

All endpoints return JSON with a `success` boolean.

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/health` | Health check |
| GET | `/api/algorithms` | Catalog + limits |
| POST | `/generate` | Generate array |
| POST | `/sort` | Sort with animation steps |
| POST | `/benchmark` | Benchmark all algorithms |

### Limits

| Setting | Default | Env Variable |
|---------|---------|--------------|
| Max array size | 150 | `MAX_ARRAY_SIZE` |
| Max animation steps | 2500 | `MAX_ANIMATION_STEPS` |
| Benchmark runs | 3 | `BENCHMARK_TIMED_RUNS` |

### Error format

```json
{ "success": false, "error": "Array size cannot exceed 150." }
```

---

## Metrics Note

**Swaps** counts element exchanges for exchange-based algorithms and **writes/overwrites** for insertion and merge sort. Compare metrics within the same algorithm family, not as identical operations across all sorts.

---

## Testing

```bash
pytest tests/ -v
```

Covers algorithm correctness, generator edge cases, and Flask API integration.

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `FLASK_DEBUG` | Enable debug mode (`true`/`false`) |
| `PORT` | Server port (default `5000`) |
| `MAX_ARRAY_SIZE` | API array size cap |
| `MAX_ANIMATION_STEPS` | Step thinning threshold |
| `SECRET_KEY` | Flask secret key |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Author

Built as a flagship portfolio project demonstrating algorithms, full-stack engineering, and production-minded code organization.
