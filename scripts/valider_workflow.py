#!/usr/bin/env python3
"""Verifie hors-ligne la structure d'un fichier workflow GitHub Actions.
Usage : python3 valider_workflow.py fichier.yml [autre.yml ...]
Ce n'est PAS le validateur officiel de GitHub : il attrape les erreurs courantes."""
import sys
try:
    import yaml
except ImportError:
    sys.exit("PyYAML absent : sudo apt install python3-yaml")

def verifier(chemin):
    erreurs = []
    try:
        with open(chemin, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
    except yaml.YAMLError as e:
        return [f"YAML invalide : {e}"]
    if not isinstance(doc, dict):
        return ["Le fichier doit contenir un dictionnaire (name, on, jobs)"]
    # PyYAML lit la cle `on` comme le booleen True (piege classique)
    if "on" not in doc and True not in doc:
        erreurs.append("Cle 'on' absente (declencheur manquant)")
    jobs = doc.get("jobs")
    if not isinstance(jobs, dict) or not jobs:
        return erreurs + ["Cle 'jobs' absente ou vide"]
    for nom, job in jobs.items():
        if not isinstance(job, dict):
            erreurs.append(f"job '{nom}' : vide ou mal indente (cles runs-on/steps placees au mauvais niveau ?)")
            continue
        if "uses" in job:
            continue
        if "runs-on" not in job:
            erreurs.append(f"job '{nom}' : 'runs-on' manquant")
        steps = job.get("steps")
        if steps is None:
            inconnues = [k for k in job if k not in ("runs-on", "needs", "strategy", "permissions", "env", "if", "name")]
            erreurs.append(f"job '{nom}' : 'steps' manquant" + (f" (cle suspecte : {inconnues})" if inconnues else ""))
            continue
        for i, s in enumerate(steps, 1):
            if not isinstance(s, dict) or not ({"uses", "run"} & set(s)):
                erreurs.append(f"job '{nom}', etape {i} : il faut 'uses' ou 'run'")
        mat = (job.get("strategy") or {}).get("matrix", {})
        for cle, valeurs in mat.items():
            if isinstance(valeurs, list):
                for v in valeurs:
                    if isinstance(v, float):
                        erreurs.append(f"job '{nom}' : matrice '{cle}' : {v} est lu comme un nombre ; mettre des guillemets (ex. \"3.10\", sinon 3.10 devient 3.1)")
    return erreurs

code = 0
for chemin in sys.argv[1:] or ["--help"]:
    if chemin == "--help":
        print(__doc__); sys.exit(0)
    errs = verifier(chemin)
    if errs:
        code = 1
        print(f"[ERREUR] {chemin}")
        for e in errs: print("   -", e)
    else:
        print(f"[ OK ] {chemin}")
sys.exit(code)
