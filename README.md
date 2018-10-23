# Fintech - Django Rest API

## Content
- [Overview](#Overview)
- [Tech Stack](#Tech-stack)
- [How to run](#how-to-run)
- [Database Schema](#database-schema)
- [API Requests](#api-requests)



## Overview
When a customer purchases an item using their payment card at a store, several things happen in the background. Below diagram shows the typical entities in the payment card industry with an example transaction from a Cardholder to a Merchant.  

![](/images/overview.png)


`Project:` Build a Database and API's for a fintech company that acts as an Issuer. Fintech opperates with its customers(cardholders) and Scheme

## Tech stack 
- Django application (written in python, following PEP8 and PEP257 conventions)
- Django rest_framework for API's 
- This application is connected to Postgresql 10 database, is scalable and robust for this purpose.


## How to run
Follow the below steps to get the application running:

#### a) Database
Create database in the Postgresql instance. Reccomended to create a database with application name. Eg: `fintech_api`


#### b) Environment Variables
Please note that below environment variables need to be configured in `.bash_profile` before attempting to start the application server and running management commands. 

`FINTECH_SECRET_KEY` - secret key for the application

`DB_NAME` - name of the database in postgresql, usually it is your app name.

`DB_USER` - username of the database in Postgresql

`DB_PASS` - password of the database in Postgresql

`DB_HOST` - 127.0.0.1 for localhost

`DB_PORT` - usually it is 5432 or 5433 depending on what you choose

#### c) install application dependencies
- go to working directory
- create a virtualenv 
- activate virtualenv 
- `pip3 install -r requirements.txt`
this will install needed dependencies in the virtual environment


#### d) Migrate, Create Superuser and add dummy customers in database (Optional)

To migrate models to database tables, Run the following command:
`python manage.py makemigrations`
`python manage.py migrate`


To create superuser, Run the following command:
`python manage.py createsuperuser`
create username and password --> Login to admin --> add 2 Customers in Customer table by providing needed details ---> add Accounts for these 2 Customers in Accounts table matching the details in Customer table. (Note: total_balance and available_balance values should be the same since both values are equal before authorization and presentation)

We added dummy customers inorder to test our API Request.


#### e) Run Server
To start the server, Run the following management command:
`python manage.py runserver`

server will run at: `http://127.0.0.1:8000/`




#### f) Management commands
##### - `load_money` command

This command is to credit amount to cardholder. Run it as follows:

`python manage.py load_money <cardholder_id> <amount> <currency>`

Format to be:

`cardholder_id` - numerical value representing the ID of the cardholder to credit. Eg: 21321

`amount` - float value, with 2 decimal places, representing the amount of money to credit. Eg: 1000.50

`currency` - 3 (capital) letter value, representing the currency of the account to credit. Eg: EUR

Example command:

`python manage.py load_money 21321 1000.50 EUR`


##### - `batch_process` command

This command is used to run the batch process of settling transactions to the Scheme.

`python manage.py batch_process`



## Database Scheme:
4 tables used: Customers, Accounts, Transactions and Transfers. The following Entity Relation diagram illustrates how I intend to implement the database:

![](/images/databases.png)


## API Requests

### Scheme_API `<server>/scheme/`

#### `POST`

This feature is used by the Scheme in order to send authorisation/presentment WebHooks.

For `authorisation` requests, below parameters in form of JSON data need to be available in the request:


```
{
"type": "authorisation", 
"card_id": "21321", 
"transaction_id": "1234ROKKA", 
"merchant_name": "SNEAKERS R US", 
"merchant_country": "US",
"merchant_mcc": "5139", 
"billing_amount": "90.00", 
"billing_currency": "EUR", 
"transaction_amount": "100.00", 
"transaction_currency": "USD"
}
```

For `presentment` requests, below parameters in form of JSON data need to be available in the request:

```
{
"type": "presentment", 
"card_id": "21321", 
"transaction_id": "1234ROKKA", 
"merchant_name": "SNEAKERS R US", 
"merchant_country": "US", 
"merchant_city": "LOS ANGELES", 
"merchant_mcc": "5139", 
"billing_amount": "90.00", 
"billing_currency": "EUR", 
"transaction_amount": "100.00", 
"transaction_currency": "USD", 
"settlement_amount": "89.50", 
"settlement_currency": "EUR"
}

```

### Transactions_API `<server>/transactions/`

#### `GET`

This feature is used by Cardholders to see their presented transactions.

The following query parameters need to be set in order to get data:

`cardholder` - numerical value 

`start_date` - datetime format `%Y-%m-%d %H:%M:%S`

`end_date` - datetime format `%Y-%m-%d %H:%M:%S`

Example request 
```
http://localhost:8000/transactions/?cardholder=21321&start_date=2018-10-21 00:00&end_date=2018-10-22 03:50
```

Returns data is a JSON containing all specific transactions in that timeframe.

### Balances_API `<server>/balances/`

#### `GET`

Functionality here is used by Cardholders, in order to see their current accounts and balances.

The following query parameters need to be set in order to get data:

`cardholder` - numerical value 

`type` - `ledger` or  `available`

Example request 
```
http://localhost:8000/balances/?cardholder=21321&type='ledger'
```

Return data is a JSON containing current balance(presented) or available balance.


