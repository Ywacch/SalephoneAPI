# SalephoneAPI
API for smartphone market data

<<<<<<< HEAD
Warning: some tests may fail due to differences in test and production database (being fixed)

Application requires the following environment variables for database functionality. These can be set directly in the 
system's environment or in a docker-compose file:
- salephone_user: database user
- salephone_pw: database password
- postgres_host_ip: ip of the host computer (default is 'localhost' which wont work on docker)
- salephone_dbname: database name
=======
Warning: some tests may fail due to differences in test and production database

=======
Application requires the following environment variables for database functionality:
- salephone_user: database user
- salephone_pw: database password
- salephone_host: database host (default is 'localhost')
- salephone_dbname: database name
