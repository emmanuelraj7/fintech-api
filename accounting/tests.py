from django.test import TestCase
from accounting.models import Customers, Accounts, Transactions, Transfers
from django.test import RequestFactory
from django.urls import reverse
from model_mommy import mommy
from django.test import Client
from accounting.api_views import Scheme_API



class TestCustomers(TestCase):
    def setUp(self):
        self.models = mommy.make('accounting.Customers')


    def test_str(self):
        self.assertEquals(str(self.models), self.models.customer_name)   

        

class TestAccounts(TestCase):
    def setUp(self):
        self.models = mommy.make('accounting.Accounts')


    def test_str(self):
        self.assertEquals(str(self.models), self.models.card_id)   


class TestTransactions(TestCase):
    def setUp(self):
        self.models = mommy.make('accounting.Transactions') 



class TestSchemeAPIView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.accounts_model = mommy.make('accounting.Accounts')
        self.customers_models = mommy.make('accounting.Customers', account=self.accounts_model, _quantity=3)




class TestSchemeAPIIntegration(TestCase):
     def setUp(self):
         self.client = Client()
         self.account_model = mommy.make('accounting.Accounts')
         self.customers_models = mommy.make('accounting.Customers', account=self.accounts_model, _quantity=3)



