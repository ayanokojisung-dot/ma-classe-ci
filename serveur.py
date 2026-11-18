"""Mini serveur HTTP de Ma Classe (bibliothèque standard uniquement)."""
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from moyenne import lire_notes, mention, moyenne_ponderee

TITRE = os.environ.get("TITRE", "Ma Classe")
DATA_DIR = os.environ.get("DATA_DIR", "data")
PORT = int(os.environ.get("PORT", "8000"))


def compter_visite(dossier):
    """Incrémente le compteur de visites enregistré dans un fichier et le renvoie."""
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "compteur.txt")
    try:
        with open(chemin, encoding="utf-8") as fichier:
            total = int(fichier.read().strip())
    except (FileNotFoundError, ValueError):
        total = 0
    total += 1
    with open(chemin, "w", encoding="utf-8") as fichier:
        fichier.write(str(total))
    return total


def construire_reponse(chemin, dossier=DATA_DIR):
    """Retourne (code HTTP, type de contenu, corps) pour un chemin donné."""
    if chemin == "/":
        moyenne = moyenne_ponderee(lire_notes("donnees/notes.csv"))
        page = f"<h1>{TITRE}</h1><p>Moyenne : {moyenne} ({mention(moyenne)})</p>"
        return 200, "text/html; charset=utf-8", page
    if chemin == "/api/moyenne":
        moyenne = moyenne_ponderee(lire_notes("donnees/notes.csv"))
        corps = json.dumps({"moyenne": moyenne, "mention": mention(moyenne)})
        return 200, "application/json", corps
    if chemin == "/visites":
        return 200, "application/json", json.dumps({"visites": compter_visite(dossier)})
    return 404, "text/plain; charset=utf-8", "Page introuvable"


class Gestionnaire(BaseHTTPRequestHandler):
    def do_GET(self):
        code, type_contenu, corps = construire_reponse(self.path)
        donnees = corps.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", type_contenu)
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)


if __name__ == "__main__":
    print(f"{TITRE} : écoute sur le port {PORT}", flush=True)
    HTTPServer(("0.0.0.0", PORT), Gestionnaire).serve_forever()
