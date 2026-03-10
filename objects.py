from datetime import datetime, date
from pydantic import BaseModel

class Emprestimo(BaseModel):
    # id_emprestimo: int | None = None
    id_livro: int
    id_usuario: str
    data_previsao_devolucao_em: datetime
    data_realizado_em: datetime
