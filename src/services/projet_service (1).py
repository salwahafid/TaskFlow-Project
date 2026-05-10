from typing import List, Optional, Dict
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Projet:
    """
    Représente un projet collaboratif.
    
    Attributes:
        id (int): Identifiant unique
        nom (str): Nom du projet
        description (str): Description détaillée
        proprietaire_id (int): ID du créateur du projet
        date_creation (datetime): Date de création
        membres_ids (List[int]): IDs des membres du projet
    """
    id: int
    nom: str
    description: str
    proprietaire_id: int
    date_creation: datetime
    membres_ids: List[int] = None
    
    def __post_init__(self):
        """Initialise la liste des membres après l'instanciation."""
        if self.membres_ids is None:
            self.membres_ids = []
    
    def ajouter_membre(self, utilisateur_id: int) -> bool:
        """
        Ajoute un membre au projet.
        
        Args:
            utilisateur_id (int): ID de l'utilisateur à ajouter
        
        Returns:
            bool: True si l'ajout a réussi
        """
        if utilisateur_id not in self.membres_ids:
            self.membres_ids.append(utilisateur_id)
            return True
        return False
    
    def retirer_membre(self, utilisateur_id: int) -> bool:
        """
        Retire un membre du projet.
        
        Args:
            utilisateur_id (int): ID de l'utilisateur à retirer
        
        Returns:
            bool: True si le retrait a réussi
        """
        if utilisateur_id in self.membres_ids:
            self.membres_ids.remove(utilisateur_id)
            return True
        return False
    
    def est_membre(self, utilisateur_id: int) -> bool:
        """
        Vérifie si un utilisateur est membre du projet.
        
        Args:
            utilisateur_id (int): ID de l'utilisateur
        
        Returns:
            bool: True si l'utilisateur est membre
        """
        return utilisateur_id in self.membres_ids


class ProjetService:
    """
    Service gérant les opérations sur les projets.
    
    Attributes:
        projets (Dict[int, Projet]): Stockage des projets par ID
        _prochain_id (int): Générateur d'IDs automatique
    """
    
    def __init__(self):
        """Initialise le service avec un stockage vide."""
        self.projets: Dict[int, Projet] = {}
        self._prochain_id = 1
    
    def creer_projet(self, nom: str, description: str, proprietaire_id: int) -> Projet:
        """
        Crée un nouveau projet.
        
        Args:
            nom (str): Nom du projet
            description (str): Description détaillée
            proprietaire_id (int): ID du créateur/propriétaire
        
        Returns:
            Projet: Le projet créé
        
        Raises:
            ValueError: Si le nom est vide
        """
        if not nom or not nom.strip():
            raise ValueError("Le nom du projet ne peut pas être vide")
        
        projet = Projet(
            id=self._prochain_id,
            nom=nom.strip(),
            description=description,
            proprietaire_id=proprietaire_id,
            date_creation=datetime.now()
        )
        
        # Ajouter le propriétaire comme membre
        projet.ajouter_membre(proprietaire_id)
        
        self.projets[projet.id] = projet
        self._prochain_id += 1
        
        return projet
    
    def modifier_projet(self, projet_id: int, nouveau_nom: str = None, 
                        nouvelle_description: str = None) -> Optional[Projet]:
        """
        Modifie un projet existant.
        
        Args:
            projet_id (int): Identifiant du projet
            nouveau_nom (str, optional): Nouveau nom
            nouvelle_description (str, optional): Nouvelle description
        
        Returns:
            Optional[Projet]: Le projet modifié, ou None si non trouvé
        """
        projet = self.projets.get(projet_id)
        if not projet:
            return None
        
        if nouveau_nom and nouveau_nom.strip():
            projet.nom = nouveau_nom.strip()
        
        if nouvelle_description is not None:
            projet.description = nouvelle_description
        
        return projet
    
    def supprimer_projet(self, projet_id: int, utilisateur_id: int) -> bool:
        """
        Supprime un projet (seul le propriétaire peut le faire).
        
        Args:
            projet_id (int): Identifiant du projet
            utilisateur_id (int): ID de l'utilisateur demandant la suppression
        
        Returns:
            bool: True si la suppression a réussi
        
        Raises:
            PermissionError: Si l'utilisateur n'est pas le propriétaire
            ValueError: Si le projet n'existe pas
        """
        projet = self.projets.get(projet_id)
        if not projet:
            raise ValueError(f"Projet {projet_id} non trouvé")
        
        if projet.proprietaire_id != utilisateur_id:
            raise PermissionError("Seul le propriétaire peut supprimer le projet")
        
        del self.projets[projet_id]
        return True
    
    def get_projet(self, projet_id: int) -> Optional[Projet]:
        """
        Récupère un projet par son ID.
        
        Args:
            projet_id (int): Identifiant du projet
        
        Returns:
            Optional[Projet]: Le projet trouvé ou None
        """
        return self.projets.get(projet_id)
    
    def lister_projets_utilisateur(self, utilisateur_id: int) -> List[Projet]:
        """
        Liste tous les projets dont un utilisateur est membre.
        
        Args:
            utilisateur_id (int): ID de l'utilisateur
        
        Returns:
            List[Projet]: Liste des projets de l'utilisateur
        """
        resultats = []
        for projet in self.projets.values():
            if projet.est_membre(utilisateur_id):
                resultats.append(projet)
        return resultats
    
    def ajouter_membre_projet(self, projet_id: int, utilisateur_id: int, 
                              demandeur_id: int) -> bool:
        """
        Ajoute un membre à un projet.
        
        Args:
            projet_id (int): Identifiant du projet
            utilisateur_id (int): ID de l'utilisateur à ajouter
            demandeur_id (int): ID de l'utilisateur faisant la demande
        
        Returns:
            bool: True si l'ajout a réussi
        
        Raises:
            PermissionError: Si le demandeur n'est pas propriétaire
            ValueError: Si le projet n'existe pas
        """
        projet = self.projets.get(projet_id)
        if not projet:
            raise ValueError(f"Projet {projet_id} non trouvé")
        
        if projet.proprietaire_id != demandeur_id:
            raise PermissionError("Seul le propriétaire peut ajouter des membres")
        
        return projet.ajouter_membre(utilisateur_id)
    
    def retirer_membre_projet(self, projet_id: int, utilisateur_id: int,
                              demandeur_id: int) -> bool:
        """
        Retire un membre d'un projet.
        
        Args:
            projet_id (int): Identifiant du projet
            utilisateur_id (int): ID de l'utilisateur à retirer
            demandeur_id (int): ID de l'utilisateur faisant la demande
        
        Returns:
            bool: True si le retrait a réussi
        
        Raises:
            PermissionError: Si le demandeur n'est pas propriétaire
            ValueError: Si le projet n'existe pas
        """
        projet = self.projets.get(projet_id)
        if not projet:
            raise ValueError(f"Projet {projet_id} non trouvé")
        
        # Le propriétaire ne peut pas se retirer lui-même
        if utilisateur_id == projet.proprietaire_id:
            raise PermissionError("Le propriétaire ne peut pas se retirer du projet")
        
        if projet.proprietaire_id != demandeur_id:
            raise PermissionError("Seul le propriétaire peut retirer des membres")
        
        return projet.retirer_membre(utilisateur_id)
    
    def get_membres_projet(self, projet_id: int) -> List[int]:
        """
        Récupère la liste des membres d'un projet.
        
        Args:
            projet_id (int): Identifiant du projet
        
        Returns:
            List[int]: Liste des IDs des membres
        
        Raises:
            ValueError: Si le projet n'existe pas
        """
        projet = self.projets.get(projet_id)
        if not projet:
            raise ValueError(f"Projet {projet_id} non trouvé")
        return projet.membres_ids.copy()
