# Plan B : registre local (a la place de GHCR)
    docker run -d -p 5000:5000 --name registre registry:2
    docker tag ma-classe:1.0 localhost:5000/ma-classe:1.0
    docker push localhost:5000/ma-classe:1.0
    curl http://localhost:5000/v2/_catalog
Hors-ligne : l'image registry:2 se precharge avec `docker save registry:2 -o registry2.tar` puis `docker load -i registry2.tar`.
