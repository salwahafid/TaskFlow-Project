from typing import Optional, Dict, List
from enum import Enum
from datetime import datetime
import hashlib
import re


class Role(Enum):
    """Énumération des rôles possibles dans l'application."""
    ADMIN = "administrateur"
    MEMBRE = "membre_simple"


class Utilisateur:
    """
    Représente un utilisateur du système.
    
    Attributes:
        id (int): Identifiant unique
        nom (str): Nom complet
        email (str): Adresse email (unique)
        mot_de_passe_hash (str): Hash du mot de passe
        role (Role): Rôle de l'utilisateur
        date_inscription (datetime): Date de création du compte
        projets_ids (List[int]): Liste des projets auxquels il appartient
    """
    
    def __init__(self, id_utilisateur: int, nom: str, email: str, mot_de_passe: str, role: Role = Role.MEMBRE):
        """
        Initialise un nouvel utilisateur.
        
        Args:
            id_utilisateur (int): Identifiant unique
            nom (str): Nom complet
            email (str): Adresse email
            mot_de_passe (str): Mot de passe en clair (sera hashé)
            role (Role, optional): Rôle de l'utilisateur. Par défaut MEMBRE
        """
        self.id = id_utilisateur
        self.nom = nom
        self.email = email.lower()
        self.mot_de_passe_hash = self._hasher_mot_de_passe(mot_de_passe)
        self.role = role
        self.date_inscription = datetime.now()
        self.projets_ids: List[int] = []
        self.taches_assignees_ids: List[int] = []
    
    @staticmethod
    def _hasher_mot_de_passe(mot_de_passe: str) -> str:
        """
        Hash le mot de passe avec SHA-256.
        
        Args:
            mot_de_passe (str): Mot de passe en clair
        
        Returns:
            str: Hash du mot de passe
        """
        return hashlib.sha256(mot_de_passe.encode()).hexdigest()
    
    def verifier_mot_de_passe(self, mot_de_passe: str) -> bool:
        """
        Vérifie si le mot de passe fourni correspond au hash stocké.
        
        Args:
            mot_de_passe (str): Mot de passe à vérifier
        
        Returns:
            bool: True si le mot de passe est correct
        """
        return self.mot_de_passe_hash == self._hasher_mot_de_passe(mot_de_passe)
    
    def est_administrateur(self) -> bool:
        """
        Vérifie si l'utilisateur est administrateur.
        
        Returns:
            bool: True si rôle ADMIN
        """
        return self.role == Role.ADMIN


class AuthentificationService:
    """
    Service gérant l'authentification et les utilisateurs.
    
    Ce service implémente le pattern Factory pour créer différents types
    d'utilisateurs (admin, membre).
    
    Attributes:
        utilisateurs (Dict[int, Utilisateur]): Stockage des utilisateurs par ID
        emails_utilisateurs (Dict[str, int]): Mapping email -> ID
        _prochain_id (int): Générateur d'IDs automatique
        _utilisateur_connecte_id (Optional[int]): ID de l'utilisateur actuellement connecté
    
    Author:
        Équipe TaskFlow
    """
    
    def __init__(self):
        """Initialise le service avec des utilisateurs par défaut."""
        self.utilisateurs: Dict[int, Utilisateur] = {}
        self.emails_utilisateurs: Dict[str, int] = {}
        self._prochain_id = 1
        self._utilisateur_connecte_id: Optional[int] = None
        
        # Création d'un admin par défaut
        self._creer_utilisateur_par_defaut()
    
    def _creer_utilisateur_par_defaut(self):
        """Crée un administrateur par défaut pour le démarrage."""
        self.inscrire("Admin Système", "admin@taskflow.com", "admin123", Role.ADMIN)
    
    def inscrire(self, nom: str, email: str, mot_de_passe: str, role: Role = Role.MEMBRE) -> Utilisateur:
        """
        Inscrit un nouvel utilisateur (pattern Factory).
        
        Args:
            nom (str): Nom complet
            email (str): Adresse email (doit être valide et unique)
            mot_de_passe (str): Mot de passe (minimum 6 caractères)
            role (Role, optional): Rôle de l'utilisateur. Par défaut MEMBRE
        
        Returns:
            Utilisateur: L'utilisateur créé
        
        Raises:
            ValueError: Si l'email est invalide, déjà utilisé, ou mot de passe trop court
        
        Example:
            >>> service = AuthentificationService()
            >>> user = service.inscrire("Jean Dupont", "jean@example.com", "pass123")
        """
        # Validations
        if not self._email_valide(email):
            raise ValueError("Format d'email invalide")
        
        if email.lower() in self.emails_utilisateurs:
            raise ValueError(f"L'email {email} est déjà utilisé")
        
        if len(mot_de_passe) < 6:
            raise ValueError("Le mot de passe doit contenir au moins 6 caractères")
        
        # Factory : création de l'utilisateur avec le rôle approprié
        utilisateur = Utilisateur(
            id_utilisateur=self._prochain_id,
            nom=nom,
            email=email,
            mot_de_passe=mot_de_passe,
            role=role
        )
        
        self.utilisateurs[utilisateur.id] = utilisateur
        self.emails_utilisateurs[email.lower()] = utilisateur.id
        self._prochain_id += 1
        
        return utilisateur
    
    def _email_valide(self, email: str) -> bool:
        """
        Valide le format d'un email.
        
        Args:
            email (str): Email à valider
        
        Returns:
            bool: True si l'email est valide
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def connexion(self, email: str, mot_de_passe: str) -> Optional[Utilisateur]:
        """
        Connecte un utilisateur existant.
        
        Args:
            email (str): Email de l'utilisateur
            mot_de_passe (str): Mot de passe
        
        Returns:
            Optional[Utilisateur]: L'utilisateur connecté, ou None si échec
        
        Example:
            >>> service = AuthentificationService()
            >>> user = service.connexion("jean@example.com", "pass123")
            >>> if user:
            ...     print(f"Bienvenue {user.nom}")
        """
        email = email.lower()
        
        if email not in self.emails_utilisateurs:
            return None
        
        utilisateur = self.utilisateurs[self.emails_utilisateurs[email]]
        
        if utilisateur.verifier_mot_de_passe(mot_de_passe):
            self._utilisateur_connecte_id = utilisateur.id
            return utilisateur
        
        return None
    
    def deconnexion(self) -> None:
        """Déconnecte l'utilisateur actuellement connecté."""
        self._utilisateur_connecte_id = None
    
    def get_utilisateur_connecte(self) -> Optional[Utilisateur]:
        """
        Récupère l'utilisateur actuellement connecté.
        
        Returns:
            Optional[Utilisateur]: L'utilisateur connecté ou None
        """
        if self._utilisateur_connecte_id is None:
            return None
        return self.utilisateurs.get(self._utilisateur_connecte_id)
    
    def est_connecte(self) -> bool:
        """
        Vérifie si un utilisateur est connecté.
        
        Returns:
            bool: True si un utilisateur est connecté
        """
        return self._utilisateur_connecte_id is not None
    
    def get_utilisateur_par_id(self, utilisateur_id: int) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur par son ID.
        
        Args:
            utilisateur_id (int): Identifiant de l'utilisateur
        
        Returns:
            Optional[Utilisateur]: L'utilisateur trouvé ou None
        """
        return self.utilisateurs.get(utilisateur_id)
    
    def get_utilisateur_par_email(self, email: str) -> Optional[Utilisateur]:
        """
        Récupère un utilisateur par son email.
        
        Args:
            email (str): Email de l'utilisateur
        
        Returns:
            Optional[Utilisateur]: L'utilisateur trouvé ou None
        """
        email = email.lower()
        if email not in self.emails_utilisateurs:
            return None
        return self.utilisateurs.get(self.emails_utilisateurs[email])
    
    def lister_tous_les_utilisateurs(self) -> List[Utilisateur]:
        """
        Liste tous les utilisateurs du système.
        
        Returns:
            List[Utilisateur]: Liste de tous les utilisateurs
        """
        return list(self.utilisateurs.values())
    
    def supprimer_utilisateur(self, utilisateur_id: int) -> bool:
        """
        Supprime un utilisateur (admin uniquement).
        
        Args:
            utilisateur_id (int): ID de l'utilisateur à supprimer
        
        Returns:
            bool: True si la suppression a réussi
        
        Raises:
            PermissionError: Si l'utilisateur connecté n'est pas admin
        """
        utilisateur_courant = self.get_utilisateur_connecte()
        
        if not utilisateur_courant or not utilisateur_courant.est_administrateur():
            raise PermissionError("Seul un administrateur peut supprimer des utilisateurs")
        
        utilisateur = self.utilisateurs.get(utilisateur_id)
        if not utilisateur:
            return False
        
        # Supprimer des mappings
        del self.emails_utilisateurs[utilisateur.email]
        del self.utilisateurs[utilisateur_id]
        
        return True