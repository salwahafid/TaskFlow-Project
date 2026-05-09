class Utilisateur:
    def afficher_role(self):
        pass


class Admin(Utilisateur):
    def afficher_role(self):
        print("Je suis un Administrateur")


class Membre(Utilisateur):
    def afficher_role(self):
        print("Je suis un Membre")


class FactoryUtilisateur:
    @staticmethod
    def creer_utilisateur(type_user):
        if type_user == "admin":
            return Admin()
        elif type_user == "membre":
            return Membre()
        else:
            raise ValueError("Type d'utilisateur invalide")


user1 = FactoryUtilisateur.creer_utilisateur("admin")
user2 = FactoryUtilisateur.creer_utilisateur("membre")

user1.afficher_role()
user2.afficher_role()