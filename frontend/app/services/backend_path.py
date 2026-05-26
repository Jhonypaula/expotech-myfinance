from __future__ import annotations

import sys
from pathlib import Path


def instalar() -> Path:
    """Coloca o backend no ``sys.path`` e devolve o caminho usado."""
    # Este arquivo fica em frontend/app/services; o backend fica ao lado de frontend.
    backend_root = Path(__file__).resolve().parents[3] / "backend"

    if not backend_root.is_dir():
        raise RuntimeError(
            f"Backend nao encontrado em {backend_root}. "
            "O app desktop precisa que a pasta 'backend/' "
            "esteja ao lado de 'frontend/'."
        )

    backend_str = str(backend_root)
    if backend_str not in sys.path:
        sys.path.insert(0, backend_str)

    return backend_root