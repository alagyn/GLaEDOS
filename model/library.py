from typing import List
import random
import json


class Game:
    def __init__(self, name: str = None, installed: bool = False, completed: bool = False, tags: List[str] = None, *,
                 jList=None):
        if jList is None:
            self.name = name
            self.install = installed
            self.completed = completed
            self.tags = tags
        else:
            self.name = jList[0]
            self.install = jList[1]
            self.completed = jList[2]
            self.tags = jList[3]


def sortByTag(tag: str, lib: List[Game]) -> List[Game]:
    out = []
    for x in lib:
        if x.tags.__contains__(tag):
            out.append(x)
    return out


def selectRandGame(lib: List[Game]) -> Game:
    random.seed()
    idx = random.randrange(0, len(lib))
    return lib[idx]


def writeLibrary(lib: List[Game], file: str):
    with open(file, mode='w') as f:
        for x in lib:
            name = x.name
            tags = x.tags
            i = x.install
            c = x.completed
            f.write(json.dumps([name, i, c, tags]) + '\n')


def readLibrary(file: str) -> (List[Game], List[str]):
    out = []
    tags = []
    try:
        with open(file, mode='r') as f:
            for x in f:
                g = Game(jList=json.loads(x))
                for tag in g.tags:
                    if not tags.__contains__(tag):
                        tags.append(tag)
    except FileNotFoundError:
        pass
    return out, tags
