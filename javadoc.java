/**
 * Représente une tâche au sein d'un projet collaboratif.
 * Une tâche possède un titre, une description, un statut, une date d'échéance,
 * un responsable et un projet parent.
 * 
 * <p>Les statuts possibles sont : "À faire", "En cours", "Terminée".</p>
 * 
 * @author VotreNom
 * @version 1.0
 * @see Projet
 * @see Utilisateur
 */
public class Tache {

    /**
     * Identifiant unique de la tâche.
     */
    private int id;

    /**
     * Titre de la tâche.
     */
    private String titre;

    /**
     * Statut actuel de la tâche.
     */
    private String statut;

    /**
     * Constructeur complet pour créer une nouvelle tâche.
     * 
     * @param id        identifiant unique
     * @param titre     titre de la tâche
     * @param statut    statut initial ("À faire", "En cours", "Terminée")
     * @throws IllegalArgumentException si le statut est invalide
     */
    public Tache(int id, String titre, String statut) {
        if (!statutValide(statut)) {
            throw new IllegalArgumentException("Statut invalide");
        }
        this.id = id;
        this.titre = titre;
        this.statut = statut;
    }

    /**
     * Modifie le statut de la tâche.
     * 
     * @param nouveauStatut nouveau statut à appliquer
     * @return true si le changement a été effectué, false sinon
     * @see #getStatut()
     */
    public boolean changerStatut(String nouveauStatut) {
        // logique
        return true;
    }

    /**
     * Retourne le statut actuel de la tâche.
     * 
     * @return le statut sous forme de chaîne
     */
    public String getStatut() {
        return statut;
    }
}