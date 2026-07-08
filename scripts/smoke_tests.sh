#!/usr/bin/env bash
# Smoke tests : verifie que l'application repond apres deploiement.
# Usage : smoke_tests.sh <base_url>   ex: smoke_tests.sh https://localhost:5001
set -u
BASE_URL="$1"

echo "Attente du demarrage de l'application ($BASE_URL)..."
for i in $(seq 1 30); do
  if curl -k -s -f -o /dev/null "$BASE_URL/"; then
    echo "OK - l'application repond (tentative $i)"
    break
  fi
  if [ "$i" = "30" ]; then
    echo "ECHEC - l'application ne repond pas apres 30 tentatives"
    exit 1
  fi
  sleep 5
done

status=$(curl -k -s -o /dev/null -w "%{http_code}" "$BASE_URL/")
if [ "$status" != "200" ]; then
  echo "ECHEC - la page d'accueil renvoie HTTP $status (attendu : 200)"
  exit 1
fi
echo "OK - page d'accueil HTTP 200"

echo "Smoke tests reussis."
