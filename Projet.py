from typing import List, Optional
from datetime import datetime

class Project:
    """
    La classe Project - représente un conteneur pour plusieurs tâches
    Chaque projet a un nom, une description, et contient des tâches
    
    @author L'équipe TaskFlow
    @version 1.0
    """
    
    def __init__(self, id: int, name: str, description: str = "", creator=None):
        """
        Constructeur - pour créer un nouveau projet
        """
        self.id = id
        self.name = name
        self.description = description
        self.creator = creator  # User qui a créé le projet
        self.tasks = []         # Liste des tâches du projet
        self.members = []       # Liste des membres assignés au projet
        self.created_at = datetime.now()
    
    def add_task(self, task) -> None:
        """
        Ajouter une tâche au projet
        """
        self.tasks.append(task)
    
    def remove_task(self, task_id: int) -> bool:
        """
        Supprimer une tâche du projet par son ID
        Retourne True si trouvé et supprimé
        """
        for task in self.tasks:
            if task.get_id() == task_id:
                self.tasks.remove(task)
                return True
        return False
    
    def add_member(self, user) -> None:
        """
        Ajouter un membre au projet
        """
        if user not in self.members:
            self.members.append(user)
    
    def remove_member(self, user) -> bool:
        """
        Supprimer un membre du projet
        """
        if user in self.members:
            self.members.remove(user)
            return True
        return False
    
    def get_tasks_by_status(self, status):
        """
        Obtenir toutes les tâches avec un statut spécifique
        """
        return [task for task in self.tasks if task.get_status() == status]
    
    def get_completed_tasks(self) -> List:
        """
        Obtenir toutes les tâches terminées
        """
        from models.task import TaskStatus
        return self.get_tasks_by_status(TaskStatus.DONE)
    
    def get_progress(self) -> float:
        """
        Calculer le pourcentage d'avancement du projet
        Retourne un nombre entre 0 et 100
        """
        if not self.tasks:
            return 0.0
        
        from models.task import TaskStatus
        completed = len(self.get_completed_tasks())
        return (completed / len(self.tasks)) * 100
    
    # Getters et setters
    def get_id(self) -> int:
        return self.id
    
    def set_id(self, id: int) -> None:
        self.id = id
    
    def get_name(self) -> str:
        return self.name
    
    def set_name(self, name: str) -> None:
        self.name = name
    
    def get_description(self) -> str:
        return self.description
    
    def set_description(self, description: str) -> None:
        self.description = description
    
    def get_creator(self):
        return self.creator
    
    def get_tasks(self) -> List:
        return self.tasks
    
    def get_members(self) -> List:
        return self.members
    
    def get_created_at(self) -> datetime:
        return self.created_at
    
    def __str__(self) -> str:
        creator_name = self.creator.get_username() if self.creator else "inconnu"
        return f"Project{{id={self.id}, name='{self.name}', creator='{creator_name}', tasks={len(self.tasks)}, progress={self.get_progress():.1f}%}}"