# Usa uma imagem base leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho
WORKDIR /app

# Copia o conteúdo do projeto
COPY . .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Define variável do Flask
ENV FLASK_APP=run.py
ENV FLASK_ENV=development

# Expõe a porta padrão
EXPOSE 5000

# Roda o Flask
CMD ["flask", "run", "--host=0.0.0.0"]

