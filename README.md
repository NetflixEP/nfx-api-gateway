## nfx-api-gateway
Service for checking the JWT and forwarding requests further


# In .config:

secret_key *secret_key*


# In .urls:


location_from_nginx1 *forwarding_url1*;

location_from_nginx2 *forwarding_url2*;

location_from_nginx3 *forwarding_url3*;
