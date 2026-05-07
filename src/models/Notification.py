from datetime import datetime
from typing import Optional

class Notification:
    """
    La classe Notification - représente une alerte envoyée à l'utilisateur
    Utilisée avec le Pattern Observer pour informer les utilisateurs des changements
    
    @author L'équipe TaskFlow
    @version 1.0
    """
    
    def __init__(self, id: int, message: str, recipient, type_: str):
        """
        Constructeur - pour créer une nouvelle notification
        """
        self.id = id
        self.message = message
        self.recipient = recipient
        self.type = type_
        self.created_at = datetime.now()
        self.is_read = False
    
    def mark_as_read(self) -> None:
        """
        Marquer la notification comme lue
        """
        self.is_read = True
    
    @staticmethod
    def create_assignment_notification(task, assignee):
        """
        Créer une notification pour une nouvelle tâche assignée
        """
        message = f"Vous avez été assigné à une nouvelle tâche : \"{task.get_title()}\" dans le projet {task.get_project().get_name()}"
        return Notification(0, message, assignee, "assignment")
    
    @staticmethod
    def create_status_change_notification(task, old_status: str, new_status: str):
        """
        Créer une notification pour un changement de statut
        """
        message = f"Le statut de la tâche \"{task.get_title()}\" est passé de {old_status} à {new_status}"
        return Notification(0, message, task.get_assignee(), "status_change")
    
    # Getters et setters
    def get_id(self) -> int:
        return self.id
    
    def set_id(self, id: int) -> None:
        self.id = id
    
    def get_message(self) -> str:
        return self.message
    
    def set_message(self, message: str) -> None:
        self.message = message
    
    def get_created_at(self) -> datetime:
        return self.created_at
    
    def is_read(self) -> bool:
        return self.is_read
    
    def set_read(self, read: bool) -> None:
        self.is_read = read
    
    def get_recipient(self):
        return self.recipient
    
    def set_recipient(self, recipient) -> None:
        self.recipient = recipient
    
    def get_type(self) -> str:
        return self.type
    
    def set_type(self, type_: str) -> None:
        self.type = type_
    
    def __str__(self) -> str:
        return f"Notification{{id={self.id}, message='{self.message}', read={self.is_read}}}"