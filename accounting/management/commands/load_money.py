from django.core.management.base import BaseCommand, CommandParser
from django.db.models import ObjectDoesNotExist

from accounting.models import Customers, Accounts, Transfers


class Command(BaseCommand):

    help = 'Credit amount to an account with a currency'

    def add_arguments(self, parser: CommandParser):
        
        parser.add_argument('cardholder', type=int, help='card_id to credit')
        parser.add_argument('amount', type=float, help='Amount to credit(Datatype: float with 2 decimal places)')
        parser.add_argument('currency', type=str, help='Currency to credit')

    def handle(self, *args, **options):
        """Handler for running the management command."""
        print(
            'Crediting account: '
            f'Card ID <{options["cardholder"]}> '
            f'Amount <{options["amount"]}> '
            f'Currency <{options["currency"]}>'
        )

        try:
            # Get required account.
            account = Accounts.objects.get(card_id=options['cardholder'], currency=options['currency'])
            customer = Customers.objects.get(card_id=options['cardholder'])

            # Increase current value by new amount.
            customer.total_balance = float(customer.total_balance) + options['amount']
            account.total_balance = float(account.total_balance) + options['amount']
            account.available_balance = float(account.available_balance) + options['amount']


            # Create a new transfer for this account crediting.
            transfer = Transfers(
                transfer_type='CRT',
                account=account,
                total_balance=options['amount']
            )

            #Save updated amount to Customer, Account and Transfer data into database
            customer.save()
            account.save()
            transfer.save()


  
            self.stdout.write("SUCCESS: Account credited successfully!", ending='')  

        except ObjectDoesNotExist:
            print('ERROR: No matching account has been found. No action has been taken.')
