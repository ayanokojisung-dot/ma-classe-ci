import json
import tempfile
import unittest

from serveur import compter_visite, construire_reponse


class TestServeur(unittest.TestCase):
    def test_api_moyenne(self):
        code, type_contenu, corps = construire_reponse("/api/moyenne")
        donnees = json.loads(corps)
        self.assertEqual(code, 200)
        self.assertEqual(donnees["moyenne"], 13.69)
        self.assertEqual(donnees["mention"], "Assez bien")

    def test_page_inconnue(self):
        code, _, _ = construire_reponse("/nimporte-quoi")
        self.assertEqual(code, 404)

    def test_compteur_de_visites(self):
        with tempfile.TemporaryDirectory() as dossier:
            self.assertEqual(compter_visite(dossier), 1)
            self.assertEqual(compter_visite(dossier), 2)


if __name__ == "__main__":
    unittest.main()
