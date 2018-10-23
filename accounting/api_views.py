from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import Customers, Accounts, Transactions, Transfers
from .serializers import WebhookSerializer
from accounting import serializers
from accounting import models
from django.utils import timezone
from django.http import JsonResponse




class Scheme_API(APIView):

    def post(self, request):

        #Check recieved data for consistency 
        serializer = serializers.WebhookSerializer(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):

                #Check to make an authorisation or presentment
                if serializer.data.get('type') == 'authorisation':
                    response = self.authorisation(serializer.data)

                else:
                    response = self.presentment(serializer.data)

            else:
                print(serializer.errors)
                raise KeyError

        except ObjectDoesNotExist:
            response = Response(
                data={
                    'error': True,
                    'message': 'Webhook on non-existent data',
                    'data': serializer.errors
                },
                status=status.HTTP_403_FORBIDDEN
            )

        except KeyError:
            response = Response(
                data={
                    'error': True,
                    'message': 'Bad request data',
                    'data': serializer.errors
                },
                status=status.HTTP_403_FORBIDDEN
            )

        except ValueError:
            response = Response(
                data={
                    'error': True,
                    'message': 'Not enough funds in the account'
                },
                status=status.HTTP_403_FORBIDDEN
            )

        return response

    def authorisation(self, data):

        #Fetch required account
        account = models.Accounts.objects.get(card_id=data.get('card_id'))

        #Check if we have the required funds in the account
        if not float(account.total_balance) >= float(data.get('billing_amount')):
            raise ValueError

        #Reserve the amount requested
        account.reserved_amount = float(data.get('billing_amount'))

        #Deduct the value from the account so that it is no longer available for other transactions
        account.available_balance = float(
            account.total_balance) - float(account.reserved_amount)

        #Make a new transaction for authorisation
        transaction = models.Transactions(
            transaction_id=data.get('transaction_id'),
            type='authorisation',
            card_id=account,
            billing_amount=data.get('billing_amount'),
            billing_currency=data.get('billing_currency'),
            merchant_name=data.get('merchant_name'),
            merchant_country=data.get('merchant_country'),
            merchant_mcc=data.get('merchant_mcc'),
            transaction_amount=data.get('transaction_amount'),
            transaction_currency=data.get('transaction_currency')
        )

        #Save account and transaction data into the database
        account.save()
        transaction.save()

        return Response(
            data={
                'error': False,
                'message': f'AUTHORIZATION SUCCESSFUL for card_id:{data.get("card_id")} with transaction id:{data.get("transaction_id")}'
            },
            status=status.HTTP_200_OK
        )

    def presentment(self, data):

        #Fetch required account
        account = models.Accounts.objects.get(card_id=data.get('card_id'))

        #Fetch required transaction
        transaction = models.Transactions.objects.get(
            transaction_id=data.get('transaction_id'))

        #Fetch required customer
        customer = models.Customers.objects.get(card_id=data.get('card_id'))

        #Check if billing amount and reserved amount(from authorisation) are different due to volatile currency exchange rates 
        if not float(data.get('billing_amount')) == account.reserved_amount:
            #Equate reserved amount and billing amount and make changes to available balance respectively
            account.reserved_amount = float(
                data.get('billing_amount'))
            account.available_balance = float(
                account.total_balance) - float(account.reserved_amount)
            account.save()


        #Deduct funds from cardholders account by making total_balance as available_balance
        account.total_balance = float(account.available_balance)
        customer.total_balance = float(account.total_balance)
        account.reserved_amount = 00.00

        # Update transaction with the presentment data
        transaction.type = 'presentment'
        transaction.merchant_city = data.get('merchant_city')
        transaction.billing_amount = data.get('billing_amount')
        transaction.settlement_amount = data.get('settlement_amount')
        transaction.settlement_currency = data.get('settlement_currency')
        transaction.timestamp = timezone.now()

        # Create new debit transfer
        transfer = models.Transfers(
            transfer_type='DBT',
            account=account,
            total_balance=data.get('billing_amount'),
            transaction=transaction
        )

        # Save account, transaction, transfer and customer data into the database
        account.save()
        transaction.save()
        transfer.save()
        customer.save()

        return Response(
            data={
                'error': False,
                'message': f'Presentment {data.get("transaction_id")} successful'
            },
            status=status.HTTP_200_OK
        )


class Transactions_API(APIView):

    def get(self, request):
        #Check recieved data for consistency 
        serializer = serializers.TransactionsSerializer(
            data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):
                #Fetch required accounts
                accounts = models.Accounts.objects.get(
                    card_id=serializer.data.get('cardholder'))

                start_date = serializer.data.get('start_date')
                end_date = serializer.data.get('end_date')


                #Fetch required transactions
                transactions = models.Transactions.objects.filter(
                    type='presentment',
                    card_id=accounts,
                    date__range=(start_date, end_date)
                )
                

                
                # When transactions found process them into usable format
                if transactions:
                    transactions_data = {}

                    for i in transactions:
                        if i.card_id.card_id not in transactions_data:
                            transactions_data[i.card_id.card_id] = []

                        transactions_data[i.card_id.card_id].append({
                            'transaction_id': i.transaction_id,
                            'merchant_name': i.merchant_name,
                            'billing_amount': i.billing_amount,
                            'billing_currency': i.billing_currency,
                            'date': i.timestamp
                        })

                    response = Response(
                        data={
                            'error': False,
                            'message': f'TRANSACTIONS FOUND for cardholder: {serializer.data.get("cardholder")}',
                            'data': transactions_data
                        },
                        status=status.HTTP_200_OK
                    )

                else:
                    response = Response(
                        data={
                            'error': True,
                            'message': f'NO TRANSACTIONS FOUND for cardholder: {serializer.data.get("cardholder")}'
                        },
                        status=status.HTTP_404_NOT_FOUND
                    )
                
            else:
                raise KeyError

        except ObjectDoesNotExist:
            response = Response(
                data={
                    'error': True,
                    'message': f'NO ACCOUNTS FOUND for Cardholder: {serializer.data.get("cardholder")}'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except KeyError:
            response = Response(
                data={
                    'error': True,
                    'message': 'BAD REQUEST',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return response




class Balances_API(APIView):

    def get(self, request):
        #Check recieved data for consistency 
        serializer = serializers.BalancesSerializer(data=request.query_params)

        try:
            if serializer.is_valid(raise_exception=True):
                #Fetch required accounts
                accounts = models.Accounts.objects.filter(
                    card_id=serializer.data.get('cardholder'))

                transactions_data = {}
                
                #Check if ledger balance  
                if serializer.data.get('type') == 'ledger':
                    # Get required transactions for presentments
                    transactions = models.Transactions.objects.filter(
                        type='presentment',
                        card_id=accounts
                    )

                    #When transactions found, process them into more usable format
                    if transactions:
                        for i in transactions:
                            if i.card_id.card_id not in transactions_data:
                                transactions_data[i.card_id.card_id] = {
                                    'authorisation': 0,
                                    'presentment': 0
                                }

                            transactions_data[i.card_id.card_id][i.type] += float(
                                i.billing_amount)

                accounts_data = {}
                # Process the account balances into a more usable format.
                for i in accounts:
                    if i.card_id not in accounts_data:
                        accounts_data[i.card_id] = {
                            'balance': float(i.total_balance),
                            'currency': i.currency
                        }

                    #If any transactions, as well as 'ledger' balance type
                    if transactions_data and\
                            (i.card_id in transactions_data) and\
                            (serializer.data.get('type') == 'ledger'):
                            #We account for authorisation transactions(money reservations), as they are not part of this balance type.
                        accounts_data[i.card_id]['balance'] += transactions_data[i.card_id]['authorisation']

                response = Response(
                    data={
                        'error': False,
                        'message': f'Balances found for cardholder {serializer.data.get("cardholder")}',
                        'data': accounts_data
                    },
                    status=status.HTTP_200_OK
                )

            else:
                raise KeyError

        except ObjectDoesNotExist:
            response = Response(
                data={
                    'error': True,
                    'message': f'No accounts found for Cardholder <{serializer.data.get("cardholder")}>'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        except KeyError:
            response = Response(
                data={
                    'error': True,
                    'message': 'Bad request data',
                    'data': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return response
