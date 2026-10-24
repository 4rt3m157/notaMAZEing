# taille
import json

COLUMN = 40  # nevermind, j'étais avec un tableau, pas des murs. c'est le nombre de colonnes a mon tableau, pas au maze
LINES = 18  # pareil mais pour les lignes

CORIDOR = 5  # taille du CORIDOR
WALL = 1  # taille Wall

JOUEUR = 3  # taille du joueur
SPEED = 2  # VITESSSSS du gyro

def lire_config(path="config.json"):
    with open(path) as f:
        return json.load(f)