from fastapi import FastAPI
from connection import con_engine
import pandas as pd
from objects import Emprestimo

app = FastAPI()
engine = con_engine()

@app.get('/emprestimos/atual')
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

@app.get('/emprestimos')
async def busca():
    try:
        df:pd.DataFrame = pd.read_sql_query('''select * from vw_emprestimos''', con=engine)
        tabela = df.to_dict(orient='records')
        return tabela
    except Exception as e:
        print(e)
        return {f'[ERRO]':e}
@app.post('/emprestimos')
async def cria(emprestimo:Emprestimo):
    try:
        with engine.connect() as con:
            con.execute('''INSERT INTO ''')
    except Exception as e:
        print(e)
        return {f'[ERRO]':e}

# @app.patch('/devolucoes')
# @app.get('/')

