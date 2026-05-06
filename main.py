# main.py
# Point d'entrée principal de l'application TaskFlow

from models.user import User
from models.Task import Task, TaskStatus
from models.Notification import Notification
from datetime import datetime, timedelta

def main():
    """Fonction principale du programme"""
    
    print("=== Bienvenue dans TaskFlow ===\n")
    
    # 1. Créer des utilisateurs
    admin = User(1, "admin", "1234", "admin")
    membre = User(2, "sara", "1234", "membre")
    
    print(f" Utilisateur créé : {membre}")
    
    # 2. Créer un projet (il faudrait la classe Project)
    # Pour l'exemple, on simule un projet simple
    class SimpleProject:
        def __init__(self, id, name):
            self.id = id
            self.name = name
        def get_name(self):
            return self.name
    
    projet = SimpleProject(1, "Site Web TaskFlow")
    
    # 3. Créer une tâche
    tache = Task(1, "Créer l'interface", "Faire le design de la page d'accueil", projet)
    tache.assign_to(membre)
    
    # Ajouter une date limite (dans 7 jours)
    tache.set_due_date(datetime.now() + timedelta(days=7))
    
    print(f"Tâche créée : {tache}")
    
    # 4. Créer une notification
    notif = Notification.create_assignment_notification(tache, membre)
    membre.add_notification(notif)
    
    print(f"Notification envoyée : {notif}")
    
    # 5. Tester la connexion
    print(f"\n--- Test de connexion ---")
    if membre.login("sara", "1234"):
        print(f"{membre.get_username()} connecté avec succès !")
    else:
        print("Échec de connexion")
    
    # 6. Vérifier si l'utilisateur est admin
    print(f"\n--- Vérification des rôles ---")
    print(f"admin est admin ? {admin.is_admin()}")     # True
    print(f"sara est admin ? {membre.is_admin()}")     # False
    
    # 7. Afficher les notifications non lues
    print(f"\n--- Notifications non lues de sara ---")
    unread = membre.get_unread_notifications()
    for n in unread:
        print(f"{n.get_message()}")
    
    # 8. Marquer une notification comme lue
    if unread:
        unread[0].mark_as_read()
        print(f"\n Notification marquée comme lue")
        print(f"Notifications non lues restantes : {len(membre.get_unread_notifications())}")

# Ceci est le point d'entrée standard en Python
if __name__ == "__main__":
    main()
  
