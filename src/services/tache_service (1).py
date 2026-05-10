from typing import List, Optional, Dict
from datetime import datetime, date
from enum import Enum


class StatutTache(Enum):
    """Énumération des statuts possibles pour une tâche."""
    A_FAIRE = "À faire"
    EN_COURS = "En cours"
    TERMINEE = "Terminée"
    
    @classmethod
    def from_string(cls, valeur: str):
        """
        Convertit une chaîne en enum StatutTache.
        
        Args:
            valeur (str): La chaîne à convertir
        
        Returns:
            StatutTache: L'enum correspondant
        
        Raises:
            ValueError: Si la valeur n'est pas valide
        """
        for statut in cls:
            if statut.value == valeur:
                return statut
        raise ValueError(f"Statut invalide: {valeur}")


class Tache:
    """
    Représente une tâche au sein d'un projet.
    
    Attributes:
        id (int): Identifiant unique
        titre (str): Titre de la tâche
        description (str): Description détaillée
        statut (StatutTache): Statut actuel
        date_echeance (Optional[datetime]): Date limite
        responsable_id (Optional[int]): ID de l'utilisateur assigné
        projet_id (int): ID du projet parent
        date_creation (datetime): Date de création
    """
    
    def __init__(self, id_tache: int, titre: str, projet_id: int, description: str = ""):
        """
        Initialise une nouvelle tâche.
        
        Args:
            id_tache (int): Identifiant unique
            titre (str): Titre de la tâche
            projet_id (int): ID du projet parent
            description (str, optional): Description. Par défaut ""
        """
        self.id = id_tache
        self.titre = titre
        self.description = description
        self.statut = StatutTache.A_FAIRE
        self.date_echeance: Optional[datetime] = None
        self.responsable_id: Optional[int] = None
        self.projet_id = projet_id
        self.date_creation = datetime.now()
    
    def changer_statut(self, nouveau_statut: StatutTache) -> tuple[bool, str]:
        """
        Modifie le statut de la tâche.
        
        Args:
            nouveau_statut (StatutTache): Nouveau statut à appliquer
        
        Returns:
            tuple[bool, str]: (succès, message)
        """
        ancien_statut = self.statut
        self.statut = nouveau_statut
        return True, f"Statut changé de {ancien_statut.value} à {nouveau_statut.value}"
    
    def assigner(self, utilisateur_id: int) -> None:
        """
        Assigne la tâche à un utilisateur.
        
        Args:
            utilisateur_id (int): ID de l'utilisateur responsable
        """
        self.responsable_id = utilisateur_id
    
    def est_en_retard(self) -> bool:
        """
        Vérifie si la tâche est en retard.
        
        Returns:
            bool: True si la date d'échéance est dépassée et tâche non terminée
        """
        if self.date_echeance is None:
            return False
        return datetime.now() > self.date_echeance and self.statut != StatutTache.TERMINEE
    
    def est_terminee(self) -> bool:
        """
        Vérifie si la tâche est terminée.
        
        Returns:
            bool: True si le statut est TERMINEE
        """
        return self.statut == StatutTache.TERMINEE


class TacheService:
    """
    Service gérant les opérations sur les tâches.
    
    Attributes:
        taches (Dict[int, Tache]): Stockage des tâches par ID
        taches_par_projet (Dict[int, List[int]]): Mapping projet -> liste d'IDs de tâches
        _prochain_id (int): Générateur d'IDs automatique
    """
    
    def __init__(self):
        """Initialise le service avec un stockage vide."""
        self.taches: Dict[int, Tache] = {}
        self.taches_par_projet: Dict[int, List[int]] = {}
        self._prochain_id = 1
    
    def creer_tache(self, titre: str, description: str, projet_id: int,
                    responsable_id: Optional[int] = None,
                    date_echeance: Optional[datetime] = None) -> Tache:
        """
        Crée une nouvelle tâche dans un projet.
        
        Args:
            titre (str): Titre de la tâche
            description (str): Description détaillée
            projet_id (int): ID du projet parent
            responsable_id (Optional[int]): ID de l'utilisateur assigné
            date_echeance (Optional[datetime]): Date limite
        
        Returns:
            Tache: La tâche créée
        
        Raises:
            ValueError: Si le titre est vide
        """
        if not titre or not titre.strip():
            raise ValueError("Le titre de la tâche ne peut pas être vide")
        
        tache = Tache(
            id_tache=self._prochain_id,
            titre=titre.strip(),
            projet_id=projet_id,
            description=description
        )
        
        if responsable_id:
            tache.assigner(responsable_id)
        
        if date_echeance:
            tache.date_echeance = date_echeance
        
        self.taches[tache.id] = tache
        
        # Ajouter à l'index projet -> tâches
        if projet_id not in self.taches_par_projet:
            self.taches_par_projet[projet_id] = []
        self.taches_par_projet[projet_id].append(tache.id)
        
        self._prochain_id += 1
        
        return tache
    
    def modifier_tache(self, tache_id: int, titre: str = None,
                       description: str = None, date_echeance: datetime = None) -> Optional[Tache]:
        """
        Modifie une tâche existante.
        
        Args:
            tache_id (int): Identifiant de la tâche
            titre (str, optional): Nouveau titre
            description (str, optional): Nouvelle description
            date_echeance (datetime, optional): Nouvelle date d'échéance
        
        Returns:
            Optional[Tache]: La tâche modifiée, ou None si non trouvée
        """
        tache = self.taches.get(tache_id)
        if not tache:
            return None
        
        if titre and titre.strip():
            tache.titre = titre.strip()
        
        if description is not None:
            tache.description = description
        
        if date_echeance is not None:
            tache.date_echeance = date_echeance
        
        return tache
    
    def supprimer_tache(self, tache_id: int) -> bool:
        """
        Supprime une tâche.
        
        Args:
            tache_id (int): Identifiant de la tâche
        
        Returns:
            bool: True si la suppression a réussi
        """
        tache = self.taches.get(tache_id)
        if not tache:
            return False
        
        # Retirer de l'index projet -> tâches
        projet_id = tache.projet_id
        if projet_id in self.taches_par_projet:
            if tache_id in self.taches_par_projet[projet_id]:
                self.taches_par_projet[projet_id].remove(tache_id)
        
        del self.taches[tache_id]
        return True
    
    def get_tache(self, tache_id: int) -> Optional[Tache]:
        """
        Récupère une tâche par son ID.
        
        Args:
            tache_id (int): Identifiant de la tâche
        
        Returns:
            Optional[Tache]: La tâche trouvée ou None
        """
        return self.taches.get(tache_id)
    
    def get_taches_par_projet(self, projet_id: int) -> List[Tache]:
        """
        Récupère toutes les tâches d'un projet.
        
        Args:
            projet_id (int): Identifiant du projet
        
        Returns:
            List[Tache]: Liste des tâches du projet
        """
        taches_ids = self.taches_par_projet.get(projet_id, [])
        return [self.taches[t_id] for t_id in taches_ids if t_id in self.taches]
    
    def get_taches_par_responsable(self, responsable_id: int) -> List[Tache]:
        """
        Récupère toutes les tâches assignées à un utilisateur.
        
        Args:
            responsable_id (int): ID de l'utilisateur responsable
        
        Returns:
            List[Tache]: Liste des tâches assignées
        """
        return [tache for tache in self.taches.values() 
                if tache.responsable_id == responsable_id]
    
    def changer_statut_tache(self, tache_id: int, nouveau_statut: StatutTache) -> tuple[bool, str]:
        """
        Change le statut d'une tâche.
        
        Args:
            tache_id (int): Identifiant de la tâche
            nouveau_statut (StatutTache): Nouveau statut
        
        Returns:
            tuple[bool, str]: (succès, message)
        
        Raises:
            ValueError: Si la tâche n'existe pas
        """
        tache = self.taches.get(tache_id)
        if not tache:
            raise ValueError(f"Tâche {tache_id} non trouvée")
        
        return tache.changer_statut(nouveau_statut)
    
    def assigner_tache(self, tache_id: int, utilisateur_id: int) -> bool:
        """
        Assigne une tâche à un utilisateur.
        
        Args:
            tache_id (int): Identifiant de la tâche
            utilisateur_id (int): ID de l'utilisateur
        
        Returns:
            bool: True si l'assignation a réussi
        
        Raises:
            ValueError: Si la tâche n'existe pas
        """
        tache = self.taches.get(tache_id)
        if not tache:
            raise ValueError(f"Tâche {tache_id} non trouvée")
        
        tache.assigner(utilisateur_id)
        return True
