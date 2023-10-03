# Temporary readme

# Getting started on the backend project

The project is dockerized and all the necessary configurations for databases are set.

## Running the backend api

USE `docker-compose up --build` to build and run the container
USE `docker-compose up --build -d` to run the program in detach mode
for more info about docker use this video to get upto speed with it

- [Docker video](https://www.youtube.com/watch?v=0H2miBK_gAk&t=1580s)


sudo docker exec -it ems254-mysql-1 mysql -u test_user -p ---- accessing the mysql container

curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer YOUR_JWT_TOKEN" -d '{
  "account_number": "RECEIVER_ACCOUNT_NUMBER",
  "amount": AMOUNT
}' http://localhost:5000/api/v1/views/transactions/transact


curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/api/v1/views/transactions/transactions


curl -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/api/v1/views/transactions/transaction/TRANSACTION_ID


curl -X PATCH -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/api/v1/views/transactions/approve/TRANSACTION_ID

curl -X PATCH -H "Authorization: Bearer YOUR_JWT_TOKEN" http://localhost:5000/api/v1/views/transactions/cancel/TRANSACTION_ID


curl -X POST -H "Content-Type: application/json" -d '{"email": "user@example.com", "password": "secretpassword", "first_name": "john", "last_name": "Doe", "phone_number": "12345678", "location": "london"}' "http://127.0.0.1:5000/api/v1/views/register"

 curl -X POST -H "Content-Type: application/json" -d '{"email": "user5@example.com", "password": "secretpassword" }' "http://127.0.0.1:5000/api/v1/views/login"
