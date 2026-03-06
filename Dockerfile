FROM continuumio/miniconda3

# Diretório da aplicação
WORKDIR /app

# Copia apenas o environment primeiro (melhora cache de build)
COPY environment.yml .

# Cria o ambiente
RUN conda env create -f environment.yml

# Ativa automaticamente o ambiente
SHELL ["conda", "run", "-n", "back-py", "/bin/bash", "-c"]

# Copia o restante do código
COPY . .

# Porta padrão do FastAPI
EXPOSE 8000

# Comando para rodar a API
CMD ["conda", "run", "--no-capture-output", "-n", "back-py", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]