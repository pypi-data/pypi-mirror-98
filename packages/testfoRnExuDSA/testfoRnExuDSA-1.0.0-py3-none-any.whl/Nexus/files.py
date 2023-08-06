import pandas as pd
import os
from pathlib import Path as pl

def csv(path):
    return pd.read_csv(path)


def fileR(path):
    file = open(path)
    f = file.read()
    return f


def textR(path):
    file = open(path)
    f = file.read()
    return f


def file(path):
    return open(path)


def text(path):
    return open(path)


def excel(path):
    return pd.read_excel(path)


def dataText(p):
    return pd.read_csv(p)


def pd():
    import importlib
    return importlib.import_module("pandas")


def getFilePath(file):
    path = pl(file).parent.absolute()
    return path


def getCfileP():
    p = pl(__file__).parent.absolute()
    return p


def spech():
    print("The function getFilepath() will return the value of the main directory not sub-directory")

