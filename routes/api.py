"""JSON API routes."""

import logging

from flask import Blueprint, jsonify, request

from services import sort_service
from services.validation import validate_array_size, validate_array_type, validate_sort_array
from utils.array_generator import ARRAY_TYPES

logger = logging.getLogger(__name__)
api_bp = Blueprint("api", __name__)


def _error(message, status=400):
    return jsonify({"success": False, "error": message}), status


@api_bp.route("/health", methods=["GET"])
def health():
    return jsonify({"success": True, "status": "ok", "service": "AlgoBench"})


@api_bp.route("/api/algorithms", methods=["GET"])
def list_algorithms():
    return jsonify({"success": True, **sort_service.list_catalog()})


@api_bp.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}
    try:
        size = validate_array_size(data.get("size", 20))
        array_type = validate_array_type(data.get("array_type", "random"), ARRAY_TYPES)
        seed = data.get("seed")
        if seed is not None:
            seed = int(seed)

        result = sort_service.generate(size, array_type, seed=seed)
        return jsonify({
            "success": True,
            "array_type": result["array_type"],
            "array": result["array"],
            "size": len(result["array"]),
        })
    except ValueError as exc:
        return _error(str(exc), 400)
    except (TypeError, OverflowError):
        return _error("Invalid seed value.", 400)


@api_bp.route("/sort", methods=["POST"])
def sort_array():
    data = request.get_json(silent=True) or {}
    algorithm = data.get("algorithm")

    if not algorithm or not isinstance(algorithm, str):
        return _error("Algorithm name is required.", 400)

    try:
        array = validate_sort_array(data.get("array"))
        payload = sort_service.sort(algorithm, array)
        return jsonify({"success": True, **payload})
    except ValueError as exc:
        return _error(str(exc), 400)
    except KeyError:
        return _error(f"Algorithm '{algorithm}' is not registered.", 404)
    except Exception:
        logger.exception("Sort failed for algorithm=%s", algorithm)
        return _error("An unexpected error occurred while sorting.", 500)


@api_bp.route("/benchmark", methods=["POST"])
def benchmark():
    data = request.get_json(silent=True) or {}
    try:
        array = validate_sort_array(data.get("array"))
        result = sort_service.benchmark(array)
        return jsonify({"success": True, "benchmark": result})
    except ValueError as exc:
        return _error(str(exc), 400)
    except Exception:
        logger.exception("Benchmark failed")
        return _error("An unexpected error occurred during benchmark.", 500)
