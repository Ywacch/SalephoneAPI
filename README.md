# SalephoneAPI
API for smartphone market data

 
Warning: some tests may fail due to differences in test and production database (being fixed)

Application requires the following environment variables for database functionality. I.E Create an env file (i.e ```.env```) :
- POSTGRES_USER: database user
- POSTGRES_PASSWORD: database password
- db_host: name of the postgres container ```db```
- salephone_dbname: database name
- http_user: username for dashboard access
- http_pass: password for dashboard access
- api_route: name of url for api to route
Passing the environment var file to docker compose ia vthe command ```docker compose --env-file .env up -d```

In ```traefik.toml``` (near the bottom) enter your email in the email field

In ```db_scripts``` create a file called ```subcription.sql``` which creates the subscription to the master databased

run ```docker compose --env-file .env up -d```
