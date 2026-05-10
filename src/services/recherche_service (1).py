from typing import List, Optional, Dict, Callable
from datetime import datetime
from enum import Enum


class FiltrerPar(Enum):
    """Critères de filtrage disponibles."""
    STATUT = "statut"
    RESPONSABLE = "responsable"
    PROJET = "projet"
    EN_RETARD = "en_retard"
    ECHANCE_AVANT = "echeance_avant"
    ECHANCE_APRES = "echeance_apres"


class RechercheService:
    """
    Service permettant de filtrer et rechercher des tâches.
    
    Ce service implémente le pattern Strategy pour appliquer différents
    filtres de manière interchangeable.
    
    Attributes:
        _filtres (Dict[FiltrerPar, Callable]): Mapping des filtres disponibles
    
    Author:
        Équipe TaskFlow
    """
    
    def __init__(self):
        """Initialise le service avec tous les filtres disponibles."""
        self._filtres: Dict[FiltrerPar, Callable] = {
            FiltrerPar.STATUT: self._filtre_par_statut,
            FiltrerPar.RESPONSABLE: self._filtre_par_responsable,
            FiltrerPar.PROJET: self._filtre_par_projet,
            FiltrerPar.EN_RETARD: self._filtre_par_retard,
            FiltrerPar.ECHANCE_AVANT: self._filtre_par_echeance_avant,
            FiltrerPar.ECHANCE_APRES: self._filtre_par_echeance_apres,
        }
    
    def filtrer_taches(self, taches: List, criteres: Dict[FiltrerPar, any]) -> List:
        """
        Applique plusieurs filtres sur une liste de tâches.
        
        Args:
            taches (List[Tache]): Liste des tâches à filtrer
            criteres (Dict[FiltrerPar, any]): Dictionnaire des critères de filtrage
        
        Returns:
            List[Tache]: Liste des tâches répondant à tous les critères
        
        Example:
            >>> service = RechercheService()
            >>> criteres = {
            ...     FiltrerPar.STATUT: StatutTache.EN_COURS,
            ...     FiltrerPar.RESPONSABLE: 42
            ... }
            >>> resultats = service.filtrer_taches(toutes_les_taches, criteres)
        """
        resultats = taches
        
        for critere, valeur in criteres.items():
            if critere in self._filtres:
                resultats = self._filtres[critere](resultats, valeur)
        
        return resultats
    
    def _filtre_par_statut(self, taches: List, statut) -> List:
        """
        Filtre les tâches par statut.
        
        Args:
            taches (List[Tache]): Liste des tâches
            statut (StatutTache): Statut à filtrer
        
        Returns:
            List[Tache]: Tâches avec le statut demandé
        """
        return [t for t in taches if t.statut == statut]
    
    def _filtre_par_responsable(self, taches: List, responsable_id: int) -> List:
        """
        Filtre les tâches par responsable.
        
        Args:
            taches (List[Tache]): Liste des tâches
            responsable_id (int): ID du responsable
        
        Returns:
            List[Tache]: Tâches assignées à ce responsable
        """
        return [t for t in taches if t.responsable_id == responsable_id]
    
    def _filtre_par_projet(self, taches: List, projet_id: int) -> List:
        """
        Filtre les tâches par projet.
        
        Args:
            taches (List[Tache]): Liste des tâches
            projet_id (int): ID du projet
        
        Returns:
            List[Tache]: Tâches appartenant à ce projet
        """
        return [t for t in taches if t.projet_id == projet_id]
    
    def _filtre_par_retard(self, taches: List, en_retard: bool = True) -> List:
        """
        Filtre les tâches en retard / à l'heure.
        
        Args:
            taches (List[Tache]): Liste des tâches
            en_retard (bool): True pour les tâches en retard, False pour les autres
        
        Returns:
            List[Tache]: Tâches correspondant au critère
        """
        return [t for t in taches if t.est_en_retard() == en_retard]
    
    def _filtre_par_echeance_avant(self, taches: List, date_limite: datetime) -> List:
        """
        Filtre les tâches avec échéance avant une date donnée.
        
        Args:
            taches (List[Tache]): Liste des tâches
            date_limite (datetime): Date limite
        
        Returns:
            List[Tache]: Tâches avec échéance <= date_limite
        """
        return [t for t in taches if t.date_echeance and t.date_echeance <= date_limite]
    
    def _filtre_par_echeance_apres(self, taches: List, date_limite: datetime) -> List:
        """
        Filtre les tâches avec échéance après une date donnée.
        
        Args:
            taches (List[Tache]): Liste des tâches
            date_limite (datetime): Date limite
        
        Returns:
            List[Tache]: Tâches avec échéance >= date_limite
        """
        return [t for t in taches if t.date_echeance and t.date_echeance >= date_limite]
    
    def rechercher_par_titre(self, taches: List, mot_cle: str) -> List:
        """
        Recherche des tâches dont le titre contient un mot-clé.
        
        Args:
            taches (List[Tache]): Liste des tâches
            mot_cle (str): Mot-clé à rechercher
        
        Returns:
            List[Tache]: Tâches dont le titre contient le mot-clé
        """
        mot_cle = mot_cle.lower()
        return [t for t in taches if mot_cle in t.titre.lower()]
    
    def rechercher_par_description(self, taches: List, mot_cle: str) -> List:
        """
        Recherche des tâches dont la description contient un mot-clé.
        
        Args:
            taches (List[Tache]): Liste des tâches
            mot_cle (str): Mot-clé à rechercher
        
        Returns:
            List[Tache]: Tâches dont la description contient le mot-clé
        """
        mot_cle = mot_cle.lower()
        return [t for t in taches if mot_cle in t.description.lower()]
    
    def get_statistiques_taches(self, taches: List) -> Dict:
        """
        Calcule des statistiques sur une liste de tâches.
        
        Args:
            taches (List[Tache]): Liste des tâches
        
        Returns:
            Dict: Dictionnaire contenant les statistiques
        
        Example:
            >>> service = RechercheService()
            >>> stats = service.get_statistiques_taches(taches)
            >>> print(stats['nb_terminees'])
            5
        """
        from .tache_service import StatutTache
        
        total = len(taches)
        if total == 0:
            return {
                "total": 0,
                "a_faire": 0,
                "en_cours": 0,
                "terminees": 0,
                "en_retard": 0,
                "sans_responsable": 0
            }
        
        a_faire = sum(1 for t in taches if t.statut == StatutTache.A_FAIRE)
        en_cours = sum(1 for t in taches if t.statut == StatutTache.EN_COURS)
        terminees = sum(1 for t in taches if t.statut == StatutTache.TERMINEE)
        en_retard = sum(1 for t in taches if t.est_en_retard())
        sans_responsable = sum(1 for t in taches if t.responsable_id is None)
        
        return {
            "total": total,
            "a_faire": a_faire,
            "en_cours": en_cours,
            "terminees": terminees,
            "en_retard": en_retard,
            "sans_responsable": sans_responsable,
            "taux_completion": round(terminees / total * 100, 2) if total > 0 else 0
        }
    
    def filtrer_multi_criteres(self, taches: List, **kwargs) -> List:
        """
        Version simplifiée du filtrage avec paramètres nommés.
        
        Args:
            taches (List[Tache]): Liste des tâches
            **kwargs: Paramètres de filtrage (statut, responsable_id, projet_id, etc.)
        
        Returns:
            List[Tache]: Tâches filtrées
        
        Example:
            >>> service = RechercheService()
            >>> resultats = service.filtrer_multi_criteres(
            ...     taches,
            ...     statut=StatutTache.A_FAIRE,
            ...     responsable_id=42
            ... )
        """
        resultats = taches
        
        if 'statut' in kwargs:
            resultats = self._filtre_par_statut(resultats, kwargs['statut'])
        
        if 'responsable_id' in kwargs:
            resultats = self._filtre_par_responsable(resultats, kwargs['responsable_id'])
        
        if 'projet_id' in kwargs:
            resultats = self._filtre_par_projet(resultats, kwargs['projet_id'])
        
        if 'en_retard' in kwargs:
            resultats = self._filtre_par_retard(resultats, kwargs['en_retard'])
        
        return resultats