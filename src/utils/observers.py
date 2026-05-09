class Membre:
    def __init__(self, nom):
        self.nom = nom

    def update(self, message):
        print(f"{self.nom} reçoit : {message}")


class Tache:
    def __init__(self, titre):
        self.titre = titre
        self.observers = []

    def ajouter_observer(self, observer):
        self.observers.append(observer)

    def notifier(self, message):
        for observer in self.observers:
            observer.update(message)


m1 = Membre("Sara")
m2 = Membre("Soumaya")

tache = Tache("Créer UML")
tache.ajouter_observer(m1)
tache.ajouter_observer(m2)

tache.notifier("Une nouvelle tâche vous a été assignée")