from typing import List, Dict, Set
import random
import json


class Game:
    def __init__(self, name: str = None, installed: bool = False, completed: bool = False, tags: Set[str] = None, *,
                 jList=None):
        if jList is None:
            self.name = name
            self.install = installed
            self.completed = completed
            self.tags = tags
        else:
            self.name = str(jList[0])
            self.install = bool(jList[1])
            self.completed = bool(jList[2])
            self.tags = set(jList[3])

    def __str__(self):
        return f'{self.name}: i:{self.install}, c:{self.completed}, tags:{self.tags}'

    def removeTag(self, tag: str):
        try:
            self.tags.remove(tag)
        except KeyError:
            pass


class Library:
    def __init__(self, games: List[Game]):
        self.tags = set()
        self.lib: Dict[str, Game] = {}
        for x in games:
            self.lib[x.name] = x
            for t in x.tags:
                if t not in self.tags:
                    self.tags.add(t)

    def __contains__(self, item: Game) -> bool:
        return item.name in self.lib

    def __len__(self) -> int:
        return len(self.lib)

    def __setitem__(self, key, value):
        self.lib[key] = value

    def __getitem__(self, key) -> Game:
        return self.lib[key]

    def __delitem__(self, key):
        del self.lib[key]

    def __iter__(self):
        return LibIter(self)

    def selectRandGame(self) -> Game:
        random.seed()
        key = random.choice(list(self.lib.keys()))
        return self[key]

    def getNames(self) -> List[str]:
        return list(self.lib.keys())

    def getTags(self) -> List[str]:
        return list(self.tags)

    def addTag(self, tag: str):
        if tag not in self.tags:
            self.tags.add(tag)

    def removeTag(self, tag: str):
        try:
            self.tags.remove(tag)
            for g in self:
                g.removeTag(tag)
        except KeyError:
            pass


class LibIter:
    def __init__(self, lib: Library):
        self.lib = lib
        self.keys = list(self.lib.getNames())
        self.idx = -1
        self.len = len(self.keys)

    def __next__(self) -> Game:
        self.idx += 1
        if self.idx < self.len:
            return self.lib[self.keys[self.idx]]
        else:
            raise StopIteration


def sortByTag(tag: str, lib: Library) -> Library:
    out = []
    for x in lib:
        if tag in x.tags:
            out.append(x)
    return Library(out)


def writeLibrary(lib: Library, file: str) -> None:
    with open(file, mode='w') as f:
        for x in lib:
            name = x.name
            tags = list(x.tags)
            i = x.install
            c = x.completed
            f.write(json.dumps([name, i, c, tags]) + '\n')


def readLibrary(file: str) -> Library:
    libList = []

    if file is not None:
        try:
            with open(file, mode='r') as f:
                for x in f:
                    libList.append(Game(jList=json.loads(x)))

        except FileNotFoundError:
            pass

    return Library(libList)
