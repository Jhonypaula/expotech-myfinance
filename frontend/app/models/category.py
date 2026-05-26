from dataclasses import dataclass, field


@dataclass
class Category:
    """Categoria cadastrada no banco."""
    id_categorias: int
    nome_categorias: str
    descricao_categorias: str = ''