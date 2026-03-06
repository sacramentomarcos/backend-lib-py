from fastapi import FastAPI, status, HTTPException
from datetime import date
from connection import con_engine
from sqlalchemy import text
from fastapi.security import OAuth2PasswordBearer
import pandas as pd
from objects import Emprestimo

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

engine = con_engine()

@app.get('/emprestimos/atual', status_code=status.HTTP_200_OK)
async def atual():
    try:
        df:pd.DataFrame = pd.read_sql_query('''select id_emprestimo
                            from emprestimos
                            order by id_emprestimo desc
                            limit 1''', con=engine,
                            dtype={'id_emprestimo': int})
        proximo_emprestimo = {'id': int(df.to_dict(orient="records")[0]['id_emprestimo']) + 1}
        return proximo_emprestimo
    except Exception as e:
        print(e)
        return {f'[ERRO]':e}

@app.get('/emprestimos', status_code=status.HTTP_200_OK)
async def busca_todos_emprestimos():
    try:
        df:pd.DataFrame = pd.read_sql_query('''select * from vw_emprestimos''', con=engine)
        tabela = df.to_dict(orient='records')
        return tabela
    except Exception as e:
        print(e)
        return {f'[ERRO]':e}
@app.post('/emprestimos', status_code=status.HTTP_201_CREATED)
async def cria_emprestimo(emprestimo:Emprestimo):
    try:
        with engine.connect() as con:
            con.execute(text("""
                        INSERT INTO emprestimos
                        (id_livro, id_usuario, data_previsao_devolucao_em, data_realizado_em)
                        VALUES (:id_livro, :id_usuario, :data_previsao_devolucao_em, :data_realizado_em)
                    """),
                    {
                        "id_livro": emprestimo.id_livro,
                        "id_usuario": emprestimo.id_usuario,
                        "data_previsao_devolucao_em": emprestimo.data_previsao_devolucao_em,
                        "data_realizado_em": emprestimo.data_realizado_em
                    })
            con.commit()
        return dict(emprestimo)
    except Exception as e:
        print(e)
        # raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e)
        return {'[ERRO]': e}

@app.patch('/devolucoes', status_code=status.HTTP_202_ACCEPTED)
async def fecha_emprestimo(id_emprestimos:list[int]):
    hoje = date.today()
    try:
        with engine.connect() as con:
            for id in id_emprestimos:
                con.execute(text(f'''
                                UPDATE emprestimos
                                SET status = FALSE,
                                data_devolucao_em = :data_devolucao
                                WHERE id_emprestimo = :id_emprestimo
                                '''),
                                {
                                'data_devolucao': hoje.isoformat(),
                                'id_emprestimo': id
                                })
            con.commit()
        return id_emprestimos
    except Exception as e:
        print(e)
        return {'[ERRO]': e}
# @app.get('/')

