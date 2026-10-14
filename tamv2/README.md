# ELF Construction — adaptation technique pour Vercel

**État : version de développement, non validée pour une exploitation financière réelle.**

## Point contractuel impératif

**Vercel Hobby gratuit est réservé aux usages personnels non commerciaux.** ELF Construction est une application professionnelle interne : ne pas utiliser le plan Hobby pour l’exploitation réelle de la société. Un abonnement Vercel autorisant l’usage commercial serait nécessaire ; si le budget est strictement 0 DH, choisir un autre hébergement dont les conditions autorisent cet usage.

## Architecture

- Flask/Python, interface responsive d'origine, 5 espaces (Accueil, Recettes, Fournisseurs, Chantiers, Larbi).
- Entrée Vercel `api/index.py`, redirection dans `vercel.json`.
- PostgreSQL **externe** et persistant obligatoire. **Ne pas utiliser SQLite sur Vercel**, son disque est éphémère.
- Sessions Flask signées avec `SECRET_KEY` identique pour toutes les instances.
- Comptes admin / gestionnaire / direction ; données partagées via PostgreSQL.
- Justificatifs actuellement enregistrés en base, limite **3 Mo par fichier** et limite globale 4 Mo de requête.
- Import Excel : prévisualisation et validation manuelle ; le format du fichier doit être adapté aux colonnes requises.

## Configuration (Hakim)

1. Créer une base PostgreSQL persistante externe compatible avec les besoins de sécurité et sauvegarde ; vérifier son plan et ses conditions.
2. Renseigner dans l'environnement du projet `DATABASE_URL`, `SECRET_KEY`, `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `COOKIE_SECURE=1`. Ne jamais les committer dans GitHub.
3. Initialiser la base **une seule fois depuis un environnement de confiance** : `python init_db.py` avec les mêmes variables, avant le premier accès. Sur Vercel le schéma n'est volontairement pas créé automatiquement à chaque requête.
4. Déployer depuis le dépôt GitHub (root = dossier contenant `app.py`, `api/`, `templates/`, `static/`, `vercel.json`).
5. Tester `/health`, connexion, création d'un compte Mustapha, droits lecture seule, opérations, import, fichiers, modification simultanée, export, restauration et sauvegardes.
6. Après la première connexion, l'administrateur doit changer son mot de passe temporaire.

## Limites et risques à corriger avant production

- Pas de sauvegarde indépendante ni restauration automatisée dans ce paquet.
- Pas de système de migrations versionnées de base de données.
- Import Excel non universel (format strict, 3000 lignes max, fichier 4 Mo max), dédoublonnage limité à la provenance.
- Pas de verrouillage de concurrence par version ; risque d'écrasement si deux personnes éditent la même opération.
- Pièces jointes stockées dans PostgreSQL ; vérifier quotas et volume, privilégier un stockage d'objets sécurisé ensuite.
- Pas de test de charge ni audit de sécurité complet.
- Les agrégations ne remplacent pas une comptabilité vérifiée : paiements non rattachés à une commande/devis peuvent créer des incohérences.

**N'importer aucune donnée financière réelle avant validation des tests, sauvegardes et règles de rapprochement.**
