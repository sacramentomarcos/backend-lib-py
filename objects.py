from datetime import datetime, date
from pydantic import BaseModel

class Emprestimo(BaseModel):
    id_livro: int
    id_usuario: str
    data_previsao_devolucao_em: date
    data_realizado_em: date
