# Pipeline CI/CD — TIWAP

## Vue d'ensemble

Le workflow unique [`.github/workflows/pipeline.yml`](../.github/workflows/pipeline.yml)
implémente toute la chaîne, du commit jusqu'à la production.

```
Lint (Flake8) → Tests unitaires (pytest) → Analyse SonarQube → Build Docker
→ Scan Trivy → Publication GHCR → DEV + smoke tests → STAGING + tests
d'intégration → [validation manuelle] → PROD + vérification
```

Toute étape en échec **arrête immédiatement** la pipeline (`needs:` en chaîne).

## Déclencheurs

| Événement | Ce qui s'exécute |
|---|---|
| `push` sur `feature/**` | CI seule (lint, tests, Sonar, build + scan, sans publication) |
| Pull Request vers `main` | CI complète — bloque la fusion si échec |
| `push` / merge sur `main` | CI + publication GHCR + déploiements DEV → STAGING → PROD |
| tag `v*` (ex. `v1.0.0`) | Release : image taguée à la version + déploiement complet |
| `workflow_dispatch` | Déclenchement manuel |

## Build Once, Deploy Many

L'image est construite **une seule fois** puis publiée dans
`ghcr.io/samp83/tiwap` avec des tags traçables :

- `sha-<commit>` — chaque build de main
- `vX.Y.Z` + `latest` — les releases (tags Git)

Les trois environnements tirent **la même image** depuis GHCR via
[`deploy/docker-compose.deploy.yml`](../deploy/docker-compose.deploy.yml) ;
seuls le port et le nom de projet changent :

| Environnement | Port | Déclenchement | Tests |
|---|---|---|---|
| DEV | 5001 | automatique | smoke tests (`scripts/smoke_tests.sh`) |
| STAGING | 5002 | automatique après DEV | tests d'intégration (`scripts/integration_tests.sh`) |
| PROD | 5003 | **approbation manuelle** (GitHub Environments) | vérification de bon fonctionnement |

Les déploiements s'exécutent sur le runner self-hosted `sami-pc` (Docker requis).

## Qualité et sécurité

- **Flake8** : erreurs bloquantes actives (syntaxe, noms non définis, imports
  inutilisés) ; le style du code hérité est toléré via [.flake8](../.flake8).
- **SonarQube** (SonarCloud) : analyse à chaque exécution ; nécessite le secret
  `SONAR_TOKEN` (organisation `samp83`, projet `Samp83_TIWAP`).
- **Trivy** : scan de l'image ; toute vulnérabilité **CRITICAL corrigeable**
  fait échouer la pipeline avant publication.

## Secrets utilisés

| Secret | Usage |
|---|---|
| `GITHUB_TOKEN` (automatique) | push/pull GHCR |
| `SONAR_TOKEN` (à créer) | analyse SonarCloud |
