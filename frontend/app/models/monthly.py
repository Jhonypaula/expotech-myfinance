from dataclasses import dataclass


@dataclass
class MonthlyTotal:
    """Resumo mensal usado nos gráficos."""
    ano: int
    mes: int
    total_entradas: float
    total_saidas: float

    @property
    def net(self) -> float:
        return self.total_entradas - self.total_saidas