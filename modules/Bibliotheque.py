#!/bin/env python3
from .Livre import Livre

import os
from pathlib import Path
import json
from ebooklib.utils import debug

import logging

def combiner_paths(path, extensions):
    fichiers = []
    for e in extensions:
        fichiers.extend(Path(path).glob(e))
    return fichiers

class Bibliotheque():
    def __init__(self, dossier_livre, dossier_rapports="rapports"):
        self.dossier_livre = dossier_livre
        self.livres = self._recup_liv(self.dossier_livre)
        if not os.path.isdir(dossier_rapports):
            os.mkdir(dossier_rapports)
        self.dossier_rapports = dossier_rapports


    def initialise(self):
        self.cree_rapp_aut( self._dict_par_aut(self.livres) )
        self.cree_rapp_liv( self.livres )

    def update(self):
        logging.debug("Mise à jour des livres")
        self.rapport_saved = self._new_bibli()
        if self.rapport_saved != None:
            ajoute,retire = self._comparaison(self.rapport_saved, self.livres)
            if len(ajoute) > 0 or len(retire) > 0:
                self.cree_rapp_aut( self._dict_par_aut(self.livres) )
                self.cree_rapp_liv( self.livres )

    def _new_bibli(self):
        with open(f"{self.dossier_rapports}/rapport_livres.txt", "r", encoding="utf-8") as file:
            livres_json = json.load(file)
            livres = []
            for titre in livres_json:
                try:
                    livre = Livre(auteur=livres_json[titre]["auteur"], titre=titre, path=livres_json[titre]["fichier"], langue=livres_json[titre]["langue"])
                    livre.prendr_info()
                    livres.append()
                except ValueError as e:
                    print(e)
                    continue           
            livres = set( livres )
            return livres

    def _recup_liv(self, path):
        paths = combiner_paths(path, ("*.pdf", "*.epub"))
        print(paths)
        res = [Livre(path=path) for path in paths]
        for l in res:
            l.prendr_info()
        livres = set(res)            
        return livres

    def _list_aut(self, livres):
        return set(map(lambda x: getattr(x, "auteur"), livres))
        
    def _dict_par_aut(self, livres):
        auteurs = self._list_aut(livres)
        return {auteur: {livre.titre: str(livre.path) for livre in livres if livre.auteur == auteur} for auteur in auteurs}

    def cree_rapp_aut(self, livres_par_auteur):
        with open(f"{self.dossier_rapports}/rapport_auteurs.txt", "w", encoding="utf-8") as file:
            file.write( json.dumps(livres_par_auteur, indent=4, ensure_ascii=False) )
    
    def cree_rapp_liv(self, livres):
        dict_livres = {l.titre: {"auteur": l.auteur, "fichier": str(l.path), "langue": l.langue} for l in livres }
        with open(f"{self.dossier_rapports}/rapport_livres.txt", "w", encoding="utf-8") as file:
            file.write( json.dumps(dict_livres, indent=4, ensure_ascii=False) )
        
    def _comparaison(self, old, new):
        livres_ajoutes = new.difference(old)
        livres_enleves = old.difference(new)
        print(old, new)
        return livres_ajoutes, livres_enleves