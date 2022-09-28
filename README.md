# SalephoneAPI
API for smartphone market data

 
Warning: some tests may fail due to differences in test and production database (being fixed)

Application requires the following environment variables for database functionality. I.E Create an env file (i.e ```.env```) :
- POSTGRES_USER: database user
- POSTGRES_PASSWORD: database password
- db_host: name of the postgres container ```db```
- salephone_dbname: database name
Passing the environment var file to docker compose via the command ```docker compose --env-file .env up -d``
