#!/usr/bin/env bash
# Rejoue en local les etapes du pipeline CI (plan B hors-ligne).
# Usage : bash scripts/ci.sh
set -u
OK=0; KO=0
etape() {
  local nom="$1"; shift
  if "$@" >/tmp/ci_etape.log 2>&1; then
    echo "[ OK ] $nom"; OK=$((OK+1))
  else
    echo "[ECHEC] $nom"; sed 's/^/    | /' /tmp/ci_etape.log | tail -15; KO=$((KO+1))
  fi
}
PY=$(command -v python3 || command -v python)
etape "Lint (syntaxe Python)" "$PY" -m py_compile moyenne.py serveur.py
etape "Tests unitaires" "$PY" -m unittest
echo "----"; echo "Resultat : $OK reussie(s), $KO en echec"
[ "$KO" -eq 0 ]
