#!/usr/bin/env bash
# Tests d'integration / fonctionnels executes sur STAGING.
# Usage : integration_tests.sh <base_url>   ex: integration_tests.sh https://localhost:5002
set -u
BASE_URL="$1"
FAILED=0

check() {
  local name="$1"; shift
  if "$@"; then
    echo "OK    - $name"
  else
    echo "ECHEC - $name"
    FAILED=1
  fi
}

# 1. La page d'accueil repond en HTTP 200
check "page d'accueil accessible" \
  curl -k -s -f -o /dev/null "$BASE_URL/"

# 2. La page d'accueil contient le formulaire de connexion
body=$(curl -k -s "$BASE_URL/")
check "formulaire de connexion present" \
  bash -c "echo \"\$0\" | grep -qi 'login'" "$body"

# 3. Une connexion invalide est refusee
resp=$(curl -k -s -X POST -d 'username=admin&password=mauvais' "$BASE_URL/login")
check "identifiants invalides refuses" \
  bash -c "echo \"\$0\" | grep -q 'Invalid Credentials'" "$resp"

# 4. Une connexion valide redirige vers le dashboard (HTTP 302)
code=$(curl -k -s -o /dev/null -w "%{http_code}" -X POST -d 'username=admin&password=admin' "$BASE_URL/login")
check "connexion admin redirige (302)" \
  test "$code" = "302"

# 5. Une route inexistante renvoie 404
code=$(curl -k -s -o /dev/null -w "%{http_code}" "$BASE_URL/route-inexistante")
check "route inconnue renvoie 404" \
  test "$code" = "404"

if [ "$FAILED" = "1" ]; then
  echo "Des tests d'integration ont echoue."
  exit 1
fi
echo "Tous les tests d'integration sont passes."
