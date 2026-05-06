from datetime import datetime
from typing import List, Optional

class User:
    """
    La classe User - représente n'importe quelle personne qui utilise TaskFlow
    Un utilisateur peut être soit Admin, soit Membre normal
    
    @author L'équipe TaskFlow
    @version 1.0
    """
    
    def __init__(self, id: int, username: str, password: str, role: str):
        """
        Constructeur - pour créer un nouvel utilisateur
        """
        self.id = id
        self.username = username
        self.password = password
        self.role = role
        self.notifications = []  # Liste des notifications
    
    def login(self, entered_username: str, entered_password: str) -> bool:
        """
        Méthode pour se connecter
        """
        return self.username == entered_username and self.password == entered_password
    
    def add_notification(self, notification) -> None:
        """
        Ajouter une notification à l'utilisateur
        """
        self.notifications.append(notification)
    
    def get_unread_notifications(self) -> List:
        """
        Afficher toutes les notifications non lues
        """
        unread = []
        for notif in self.notifications:
            if not notif.is_read:
                unread.append(notif)
        return unread
    
    def is_admin(self) -> bool:
        """
        Vérifier si l'utilisateur est admin
        """
        return self.role.lower() == "admin"
    
    # Getters et setters
    def get_id(self) -> int:
        return self.id
    
    def set_id(self, id: int) -> None:
        self.id = id
    
    def get_username(self) -> str:
        return self.username
    
    def set_username(self, username: str) -> None:
        self.username = username
    
    def get_password(self) -> str:
        return self.password
    
    def set_password(self, password: str) -> None:
        self.password = password
    
    def get_role(self) -> str:
        return self.role
    
    def set_role(self, role: str) -> None:
        self.role = role
    
    def get_notifications(self) -> List:
        return self.notifications
    
    def __str__(self) -> str:
        return f"User{{id={self.id}, username='{self.username}', role='{self.role}'}}"