from flask import Flask


def get_caminho():
    caminho = Flask(__name__)
    return caminho.root_path