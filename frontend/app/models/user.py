from dataclasses import dataclass


@dataclass
class User:
    """Usuário autenticado."""
    id_usuarios: int
    nome_usuarios: str
    email_usuarios: str
    # A senha nunca é mantida no frontend depois da autenticação.