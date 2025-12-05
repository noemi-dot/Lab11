from dataclasses import dataclass

@dataclass
class Rifugio:
    id : int
    nome : str
    localita : str
    altitudine : int
    capienza : int
    aperto: bool

    def __eq__(self, other):
        return isinstance(other, Rifugio) and self.id == other.id

    def __hash__(self):
        # Rende l'oggetto hashable. Deve restituire un valore costante per oggetti uguali.
        # Poiché l'uguaglianza è definita dall'ID, usiamo l'hash dell'ID.
        return hash(self.id)

    def __str__(self):
        return f"{self.nome}({self.localita})"

    def __repr__(self):
        return f"{self.nome}"
