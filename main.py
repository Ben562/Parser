from time import perf_counter
from src.Parser import Parser
from src.Utils import Utils
import traceback
import shutil
import sys
import os

if __name__ == '__main__':
    try:
        t1 = perf_counter()

        if len(sys.argv) != 3:
            raise ValueError("Erreur nombre argument")

        argv = sys.argv[1]
        pathToFile = sys.argv[2]

        if argv != "-t" and argv != "-x":
            raise ValueError("Erreur argument rentré")

        if not os.path.exists(pathToFile):
            raise FileNotFoundError("Le fichier ou dossier fourni n'existe pas.")

        # Check si dossier ou fichier
        if os.path.isdir(pathToFile):
            # Check si / à la fin
            if pathToFile[-1] != "/":
                pathToFile += "/"

            # Chemin du dossier de sortie
            nomDossier = pathToFile + "analyse_pdf/"

            # Si existence du dossier → on le supprime
            if os.path.exists(nomDossier):
                try:
                    os.rmdir(nomDossier)

                except OSError:
                    try:
                        shutil.rmtree(nomDossier)

                    except Exception:
                        message = (
                            "\nImpossible de supprimer le dossier analyse_pdf\nCe dossier est nécessaire pour la "
                            "bonne exécution du programme")

                        raise Exception(message)

            # Création du dossier
            os.makedirs(nomDossier)

            for element in os.listdir(pathToFile):
                if Utils.is_pdf_file(pathToFile + element):
                    Parser(pathToFile, element, nomDossier).pdf_to_file(argv)
                    print(f"Analyse effectué sur : {element}")

        else:
            last_slash = pathToFile.rfind("/")

            chemin_fichier = pathToFile[:last_slash + 1]
            nom_fichier = pathToFile[last_slash + 1:]

            parser = Parser(chemin_fichier, nom_fichier)

            parser.pdf_to_file(argv)

            print(f"Analyse effectué sur : {nom_fichier}")

        t2 = perf_counter()

        print(f"\nTemps d'exécution : {round(t2 - t1, 2)} secondes")

    except Exception as e:
        print(traceback.format_exc())

        if type(e) is ValueError:
            print("Impossible d'analyser ce pdf.")
            print("Les causes possibles sont un mauvais encoder utilisé pour créer le pdf.\n")

        print("main.py -outputfile [/path/to/the/file.pdf, /path/to/the/dir/]")
        print("outputfile : -t text")
        print("             -x xml")
