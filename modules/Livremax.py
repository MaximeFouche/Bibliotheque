#!/bin/env python3

import os
from PyPDF2 import PdfFileReader
import epub
from pathlib import Path
import logging

class Livre():
    def __init__(self, auteur=None, titre=None, path=None, langue="fr", open=True) -> None:
        """
            Crée un lire à partir d'un fichier
        """
        self.toc = None
        if path != None:
            self.path = path
            self.file_name = Path(path).name
            self.auteur = auteur
            self.titre = titre
            self.langue = langue
            if open:
                self.prendr_info()
        else:
            self.auteur = auteur
            self.titre = titre
        if self.auteur == None:
            self.auteur = "Sans Auteur"

    def prendr_info(self):
        if self.path.suffix == ".pdf":
            self._open_pdf()
        elif self.path.suffix == ".epub":
            self._open_epub()

    def __repr__(self):
        return f"{self.titre} par {self.auteur}"

    def _open_pdf(self):
        with self.path.open(mode='rb') as f:
            pdf = PdfFileReader(f, strict=False)
            information = pdf.metadata
            self.auteur = information.author
            self.titre = information.title
            self.toc=None

    def _open_epub(self):
        with epub.open_epub(f'{self.path}') as L:
            metadata = L.opf.metadata
            self.auteur= metadata.creators[0][0]
            self.titre= metadata.titles[0][0]
            self.langue = metadata.languages[0]
            self.toc=None #pas résolu

    def __hash__(self):
        return hash((self.auteur, self.titre, self.langue))

    def __eq__(self, __o: object):
        return (self.auteur == __o.auteur and self.titre == __o.titre and self.langue == __o.langue)
