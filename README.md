# SalephoneAPI
API for Salephone smartphone market data

 
Warning: some tests may fail due to differences in test and production database (being fixed)

Application requires the following environment variables for database functionality. I.E Create an env file (i.e ```.env```) in the main project folder:
- POSTGRES_USER: database user
- POSTGRES_PASSWORD: database password
- db_host: name of the postgres container ```db```
- salephone_dbname: database name
- http_user: username for dashboard access
- http_pass: password for dashboard access
- api_route: name of url for api to route
- REDIS_PASSWORD: password for connecting to redis cache


In ```traefik.toml``` (near the bottom) enter your email in the email field

In ```db_scripts/salephone.sql```  add the `create subscription` code which creates the subscription to the master database

run ```docker compose --env-file .env up -d``` (assuming `.env` is the name of your env file)
