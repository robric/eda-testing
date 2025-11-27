#!/bin/bash
set -e

EDA_API_URL="https://127.0.0.1:9443"

# 1. Get admin-token from Keycloak
KC_ADMIN_TOKEN=$(curl -sk \
  -X POST "$EDA_API_URL/core/httpproxy/v1/keycloak/realms/master/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "client_id=admin-cli" \
  --data-urlencode "username=admin" \
  --data-urlencode "password=admin" \
  | jq -r '.access_token')

echo "Keycloak admin token: $KC_ADMIN_TOKEN"

# 2. Fetch EDA client secret (for client_id = eda)
CLIENTS_JSON=$(curl -sk \
  -X GET "$EDA_API_URL/core/httpproxy/v1/keycloak/admin/realms/eda/clients" \
  -H "Authorization: Bearer $KC_ADMIN_TOKEN" \
  -H "Content-Type: application/json")

# filter the EDA client
EDA_CLIENT_ID=$(echo "$CLIENTS_JSON" | jq -r '.[] | select(.clientId=="eda") | .id')
echo "EDA client internal ID: $EDA_CLIENT_ID"

EDA_CLIENT_SECRET=$(curl -sk \
  -X GET "$EDA_API_URL/core/httpproxy/v1/keycloak/admin/realms/eda/clients/$EDA_CLIENT_ID/client-secret" \
  -H "Authorization: Bearer $KC_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  | jq -r '.value')

echo "EDA client secret: $EDA_CLIENT_SECRET"

# 3. Get EDA API access token using the client secret
EDA_ACCESS_TOKEN=$(curl -sk \
  -X POST "$EDA_API_URL/core/httpproxy/v1/keycloak/realms/eda/protocol/openid-connect/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data-urlencode "client_id=eda" \
  --data-urlencode "grant_type=password" \
  --data-urlencode "scope=openid" \
  --data-urlencode "username=admin" \
  --data-urlencode "password=admin" \
  --data-urlencode "client_secret=$EDA_CLIENT_SECRET" \
  | jq -r '.access_token')

echo "EDA API access token: $EDA_ACCESS_TOKEN"

# 4. List available OpenAPI specifications (Core + Apps)
curl -sk \
  -X GET "$EDA_API_URL/openapi/v3" \
  -H "Authorization: Bearer $EDA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  | jq .

# 5. Sample: fetch one API spec (example: connect app)
curl -sk \
  -X GET "$EDA_API_URL/openapi/v3/apps/fabrics.eda.nokia.com/v1alpha1" \
  -H "Authorization: Bearer $EDA_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  | jq .

```
