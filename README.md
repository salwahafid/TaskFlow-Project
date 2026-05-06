# TaskFlow-Project
# TaskFlow - Application de gestion de tâches collaborative

## Description

**TaskFlow** est une application de gestion de tâches collaborative permettant à plusieurs utilisateurs de créer, organiser et suivre l'avancement de tâches au sein d’un projet.  
Ce projet a été réalisé dans le cadre du module **Conception Logicielle** (Filière CDL, année 2025-2026).

L’objectif principal est de mettre en pratique les principes fondamentaux de l’architecture logicielle :  
- Modélisation UML (cas d’utilisation, classes, séquences, activités)  
- Application des design patterns (Singleton, Observer, Factory)  
- Respect des principes SOLID et KISS  
- Documentation technique et travail collaboratif avec Git/GitHub

---

## Équipe

- Salwa Hafid  
- Sara El ghazine  
- Soumaya Ait elkabir  
- Souad Iaraben  

Encadré par : **Pr. LABBIHI**

---

## Fonctionnalités principales

### Gestion des utilisateurs
- Inscription / connexion simplifiée  
- Rôles : **Administrateur** et **Membre simple**

### Gestion des projets
- Créer, modifier, supprimer un projet  
- Ajouter ou retirer des membres dans un projet

### Gestion des tâches
- Créer, modifier, supprimer une tâche dans un projet  
- Attribuer une tâche à un membre  
- Changer le statut d’une tâche : `À faire` → `En cours` → `Terminée`  
- Ajouter une date d’échéance

### Notifications
- Un membre est notifié automatiquement lorsqu’une tâche lui est assignée

### Recherche et filtres
- Filtrer les tâches par statut, responsable ou projet

---

## Architecture et modélisation

Les diagrammes UML suivants ont été réalisés :

| Diagramme | Description |
|-----------|-------------|
| **Cas d’utilisation** | Interactions entre Admin et Membres |
| **Classes** | Entités : Utilisateur, Projet, Tâche, Notification |
| **Séquence 1** | Création d’une tâche (Factory + Base de données) |
| **Séquence 2** | Assignation d’une tâche + notification (Observer) |
| **Activité** | Cycle de vie d’une tâche (création → validation → notification chef) |

---

## Design patterns utilisés

| Pattern | Application |
|---------|--------------|
| **Singleton** | Gestion centrale du service de notification |
| **Observer** | Notification automatique des membres lors d’assignation/modification de tâche |
| **Factory** | Création flexible des types d’utilisateurs (Admin / Membre) ou des tâches |

---

## Structure du projet
TaskFlow/
├── docs/
│ ├── diagrammes/
│ │ ├── use_case.png
│ │ ├── class_diagram.png
│ │ ├── sequence_creer_tache.png
│ │ └── activite_cycle_tache.png
│ └── rapport_conception.pdf
|──src/
| ├──main
| | ├── main.py                 
| | └── models/                 
| | |   ├── __init__.py         
| | |   ├── user.py
| | |   ├── task.py
| | |   └── notification.py
| | ├── patterns/
│ | ├── services/
│ | └── utils/
│ └── test/               
├── README.md
├── javadoc/
└── swagger.yaml
---

## Livrables attendus (pondération indicative)

| Livrable | Description | Pondération |
|----------|-------------|--------------|
| Dossier de conception | Diagrammes UML + explications | 40% |
| Documentation technique | Javadoc / Swagger | 20% |
| Dépôt Git | Commits réguliers, README, branches | 20% |
| Soutenance orale | Présentation + justification des choix | 20% |

---

## Exigences techniques

- Commentaires Javadoc (ou équivalent) pour chaque classe  
- Swagger pour documenter l’API (si REST)  
- Git :  
  - Minimum 10 commits par étudiant  
  - Messages clairs  
  - Branches dédiées (`main`)

---

## Conclusion

Ce projet nous a permis d’appliquer concrètement les concepts de conception logicielle :  
modélisation UML, design patterns, architecture maintenable, documentation technique et collaboration via Git.  
Il a renforcé nos compétences en analyse, conception et structuration d’applications logicielles.

---

## Références

- [Principes SOLID] 
- [Design Patterns - Gang of Four]  
- [UML - Unified Modeling Language](https://www.uml.org/)
