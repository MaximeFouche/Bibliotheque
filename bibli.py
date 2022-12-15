#!/usr/bin/python
from modules.Bibliotheque import Bibliotheque
import sys
import os
import configparser
import logging


config = configparser.ConfigParser()
with open("bibli.conf", "r") as config_file:
    config.read_file(config_file)

if __name__ == "__main__":
    args = sys.argv

    config_file_path =""
    
    log_file = "log.log"
    dossier_livre = "livres/"
    

    if len(args) == 1:
        print("usage: bibli.py init | pour initialiser la bibliothèque")
        print("usage: bibli.py update | pour mettre à une bibliothèque existente")
        print("options: -c 'config_file' | pour spécifier le fichier de configuration")
    elif len(args) >= 2:
        if "-c" in args:
            pos = args.index("-c")
            try:
                with open(args[pos+1], "r") as config_file:
                    config.read_file(config_file)
                    log_file = config["CONFIG"]["fichier_log"]
                    dossier_livre = config["CONFIG"]["dossier_livres"]

            except:
                raise Exception("Impossible d'ouvrir le fichier de configuration, le fichier existe t'il bien ?")
        logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s',encoding='utf-8', level=logging.DEBUG)

        if args[-1] == "init":
            print("Initialisation de la bibliothèque")
            bibli = Bibliotheque(dossier_livre, config["CONFIG"]["dossier_rapports"])
            bibli.initialise()
        elif args[-1] == "update":
            bibli = Bibliotheque(dossier_livre, config["CONFIG"]["dossier_rapports"])
            bibli.update()
