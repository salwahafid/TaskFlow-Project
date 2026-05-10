from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum


class TypeNotification(Enum):
    """Énumération des types de notifications possibles."""
    ASSIGNATION_TACHE = "assignation"
    CHANGEMENT_STATUT = "changement_statut"
    ECHANCE_PROCHAIN = "echeance_prochain"
    AJOUT_PROJET = "ajout_projet"


@dataclass
class Notification:
    """
    Représente une notification individuelle.
    
    Attributes:
        id (int): Identifiant unique de la notification
        utilisateur_id (int): Destinataire
        type_notification (TypeNotification): Type de notification
        message (str): Contenu de la notification
        date_creation (datetime): Date d'envoi
        lue (bool): Indique si la notification a été lue
    """
    id: int
    utilisateur_id: int
    type_notification: TypeNotification
    message: str
    date_creation: datetime
    lue: bool = False


class NotificationService:
    """
    Service responsable de la création et de l'envoi des notifications.
    
    Ce service implémente le pattern Observer : il tient une liste
    d'observateurs (les utilisateurs) et les notifie lorsqu'un événement
    se produit.
    
    Attributes:
        _instance (NotificationService): Instance unique (pattern Singleton)
        notifications (List[Notification]): Liste de toutes les notifications
        _prochain_id (int): Générateur d'ID automatique
    
    Author:
        Équipe TaskFlow
    
    Version:
        1.0
    """
    
    _instance = None
    
    def __new__(cls):
        """
        Implémente le pattern Singleton.
        
        Garantit qu'une seule instance du service existe dans l'application.
        
        Returns:
            NotificationService: L'unique instance du service
        """
        if cls._instance is None:
            cls._instance = super(NotificationService, cls).__new__(cls)
            cls._instance._initialiser()
        return cls._instance
    
    def _initialiser(self):
        """Initialise le service avec des valeurs par défaut."""
        self.notifications: List[Notification] = []
        self._prochain_id = 1
    
    def notifier_assignation_tache(self, utilisateur_id: int, tache_titre: str, 
                                   projet_nom: str = "") -> Notification:
        """
        Envoie une notification lorsqu'une tâche est assignée à un utilisateur.
        
        Args:
            utilisateur_id (int): Identifiant de l'utilisateur à notifier
            tache_titre (str): Titre de la tâche assignée
            projet_nom (str, optional): Nom du projet contenant la tâche
        
        Returns:
            Notification: La notification créée
        
        Example:
            >>> service = NotificationService()
            >>> notif = service.notifier_assignation_tache(42, "Créer l'API", "Projet A")
            >>> print(notif.message)
            Vous avez été assigné à la tâche "Créer l'API" dans le projet "Projet A"
        """
        message = f'Vous avez été assigné à la tâche "{tache_titre}"'
        if projet_nom:
            message += f' dans le projet "{projet_nom}"'
        
        notification = Notification(
            id=self._prochain_id,
            utilisateur_id=utilisateur_id,
            type_notification=TypeNotification.ASSIGNATION_TACHE,
            message=message,
            date_creation=datetime.now(),
            lue=False
        )
        
        self.notifications.append(notification)
        self._prochain_id += 1
        
        # Logique d'envoi réel (email, WebSocket, etc.)
        self._envoyer_notification_reelle(notification)
        
        return notification
    
    def notifier_changement_statut(self, utilisateur_id: int, tache_titre: str,
                                   ancien_statut: str, nouveau_statut: str) -> Notification:
        """
        Envoie une notification lorsqu'une tâche change de statut.
        
        Args:
            utilisateur_id (int): Identifiant de l'utilisateur notifié
            tache_titre (str): Titre de la tâche concernée
            ancien_statut (str): Ancien statut de la tâche
            nouveau_statut (str): Nouveau statut de la tâche
        
        Returns:
            Notification: La notification créée
        """
        message = f'La tâche "{tache_titre}" est passée de "{ancien_statut}" à "{nouveau_statut}"'
        
        notification = Notification(
            id=self._prochain_id,
            utilisateur_id=utilisateur_id,
            type_notification=TypeNotification.CHANGEMENT_STATUT,
            message=message,
            date_creation=datetime.now(),
            lue=False
        )
        
        self.notifications.append(notification)
        self._prochain_id += 1
        
        return notification
    
    def _envoyer_notification_reelle(self, notification: Notification) -> bool:
        """
        Méthode interne pour l'envoi réel de la notification.
        
        Dans une version complète, cela enverrait un email, une notification
        push, ou un message WebSocket.
        
        Args:
            notification (Notification): La notification à envoyer
        
        Returns:
            bool: True si l'envoi a réussi
        """
        # Simulation d'envoi
        print(f"[NOTIFICATION] Utilisateur {notification.utilisateur_id}: {notification.message}")
        return True
    
    def get_notifications_utilisateur(self, utilisateur_id: int, 
                                      seulement_non_lues: bool = False) -> List[Notification]:
        """
        Récupère toutes les notifications d'un utilisateur.
        
        Args:
            utilisateur_id (int): Identifiant de l'utilisateur
            seulement_non_lues (bool, optional): Si True, retourne uniquement les non lues
        
        Returns:
            List[Notification]: Liste des notifications de l'utilisateur
        """
        resultats = [n for n in self.notifications if n.utilisateur_id == utilisateur_id]
        
        if seulement_non_lues:
            resultats = [n for n in resultats if not n.lue]
        
        return resultats
    
    def marquer_comme_lue(self, notification_id: int) -> bool:
        """
        Marque une notification comme lue.
        
        Args:
            notification_id (int): Identifiant de la notification
        
        Returns:
            bool: True si la notification a été trouvée et marquée
        
        Raises:
            ValueError: Si la notification n'existe pas
        """
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.lue = True
                return True
        
        raise ValueError(f"Notification {notification_id} non trouvée")
    
    def get_nombre_non_lues(self, utilisateur_id: int) -> int:
        """
        Compte le nombre de notifications non lues pour un utilisateur.
        
        Args:
            utilisateur_id (int): Identifiant de l'utilisateur
        
        Returns:
            int: Nombre de notifications non lues
        """
        return len(self.get_notifications_utilisateur(utilisateur_id, seulement_non_lues=True))