from django.core.management.base import BaseCommand

from accounting.models import Transactions


class Command(BaseCommand):

    help = 'Process settlement of presented transactions'

    def handle(self, *args, **options):
        """Handler for running the management command."""
        print('Running batch process')

        # Get required transactions.
        transactions = Transactions.objects.filter(
            type='presentment',
            settled=False
        )

        if transactions:
            # calculating profit and amount to be sent to the Scheme.
            profit = {}
            scheme = {}
            for row in transactions:
                # Save the currency type
                if row.settlement_currency not in profit:
                    profit[row.settlement_currency] = 0
                    scheme[row.settlement_currency] = 0

                profit[row.settlement_currency] += float(row.billing_amount) - float(row.settlement_amount)
                scheme[row.settlement_currency] += float(row.settlement_amount)

            # Update transactions data into the DB, to settle them.
            Transactions.objects.filter(
                type='presentment',
                settled=False
            ).update(settled=True)

            print('SUCCESS: Batch process completed.')
            print('Profit:', profit)
            print('Scheme:', scheme)

        else:
            print('ERROR: No presented & unsettled transactions found')


