# Vai buscar uma imagem de python na versao 3
FROM python:3 AS base

# Define onde a pasta que vai ser utilizada dentro do Container
WORKDIR /usr/src/app

# Copia tudo desta pasta para dentro da pasta WORKDIR dentro do Container
COPY Rede-Social .
COPY requirements.txt .

# Corre o comando necessário para atualizar o pip
RUN pip install --upgrade pip 

# Instala todas as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expõem a porta 8000 de dentro do Container para fora
EXPOSE 8000

#RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
#CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
