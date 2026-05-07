from datetime import datetime
from typing import Optional
from enum import Enum

# Enum pour les statuts d'une tâche
class TaskStatus(Enum):
    TODO = "À faire"
    IN_PROGRESS = "En cours"
    DONE = "Terminée"
    
    def get_french_name(self) -> str:
        return self.value


class Task:
    """
    La classe Task - représente le travail de base dans le système
    Chaque tâche est liée à un projet et peut être assignée à un membre
    
    @author L'équipe TaskFlow
    @version 1.0
    """
    
    def __init__(self, id: int, title: str, description: str, project):
        """
        Constructeur - pour créer une nouvelle tâche
        """
        self.id = id
        self.title = title
        self.description = description
        self.project = project
        self.status = TaskStatus.TODO
        self.due_date: Optional[datetime] = None
        self.assignee = None  # User
    
    def change_status(self, new_status: TaskStatus) -> None:
        """
        Changer le statut de la tâche
        """
        self.status = new_status
    
    def assign_to(self, user) -> None:
        """
        Assigner une tâche à un membre
        """
        self.assignee = user
    
    def is_overdue(self) -> bool:
        """
        Vérifier si la tâche est en retard
        """
        if self.due_date is None or self.status == TaskStatus.DONE:
            return False
        return datetime.now() > self.due_date
    
    # Getters et setters
    def get_id(self) -> int:
        return self.id
    
    def set_id(self, id: int) -> None:
        self.id = id
    
    def get_title(self) -> str:
        return self.title
    
    def set_title(self, title: str) -> None:
        self.title = title
    
    def get_description(self) -> str:
        return self.description
    
    def set_description(self, description: str) -> None:
        self.description = description
    
    def get_status(self) -> TaskStatus:
        return self.status
    
    def get_due_date(self) -> Optional[datetime]:
        return self.due_date
    
    def set_due_date(self, due_date: datetime) -> None:
        self.due_date = due_date
    
    def get_assignee(self):
        return self.assignee
    
    def get_project(self):
        return self.project
    
    def __str__(self) -> str:
        assignee_name = self.assignee.get_username() if self.assignee else "non assigné"
        return f"Task{{id={self.id}, title='{self.title}', status={self.status.value}, assignee='{assignee_name}'}}"