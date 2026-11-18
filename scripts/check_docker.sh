#!/usr/bin/env bash
# Diagnostic Docker (TP0). Usage : bash scripts/check_docker.sh
ok(){ echo "[ OK ] $1"; }; ko(){ echo "[A FAIRE] $1"; echo "         -> $2"; N=$((N+1)); }
N=0
command -v docker >/dev/null && ok "docker installe : $(docker --version)" || { ko "docker introuvable" "voir le guide d'installation, partie Docker"; }
if docker info >/dev/null 2>&1; then ok "le demon Docker repond"
else
  if docker info 2>&1 | grep -qi "permission denied"; then ko "permission refusee sur le socket" "sudo usermod -aG docker \$USER puis fermer/reouvrir Ubuntu"
  else ko "le demon Docker ne repond pas" "WSL : sudo service docker start (ou systemctl start docker)"; fi
fi
docker compose version >/dev/null 2>&1 && ok "docker compose : $(docker compose version --short 2>/dev/null)" || ko "docker compose absent" "sudo apt install docker-compose-plugin"
docker image inspect hello-world >/dev/null 2>&1 && ok "image hello-world presente (hors-ligne possible)" || echo "[INFO] image hello-world absente : docker run hello-world demande Internet (ou docker load)"
python3 -c "import yaml" 2>/dev/null && ok "PyYAML present (valider_workflow.py)" || echo "[INFO] PyYAML absent : sudo apt install python3-yaml"
if command -v curl >/dev/null && curl -sI --max-time 5 https://github.com >/dev/null 2>&1; then ok "GitHub accessible"; else echo "[INFO] GitHub inaccessible maintenant : prevoir le plan B hors-ligne"; fi
echo; [ $N -eq 0 ] && echo "Poste pret pour l'ECUE 2." || echo "$N point(s) a corriger."
