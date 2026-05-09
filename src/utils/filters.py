from typing import List

def filtrer_par_statut(taches: List[dict], statut: str) -> List[dict]:
    return [t for t in taches if t.get("statut") == statut]

def filtrer_par_responsable(taches: List[dict], responsable: str) -> List[dict]:
    return [t for t in taches if t.get("responsable") == responsable]

def filtrer_par_projet(taches: List[dict], projet: str) -> List[dict]:
    return [t for t in taches if t.get("projet") == projet]
if __name__ == "__main__":
    print("Module filters chargé")