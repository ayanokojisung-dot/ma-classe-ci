FROM python:3.12-slim
WORKDIR /app
COPY moyenne.py serveur.py ./
COPY donnees ./donnees
ENV PORT=8000 TITRE="Ma Classe" DATA_DIR=/data
EXPOSE 8000
CMD ["python", "serveur.py"]
