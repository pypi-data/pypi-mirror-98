from datetime import date
from django.core.management import call_command
from django.test import TestCase

from souschef.member.models import Member, Client, Address
from souschef.member.models import Option
from souschef.order.models import Order


class ImportMemberTestCase(TestCase):

    """
    Test data importation.
    """

    fixtures = ['routes.json']

    @classmethod
    def setUpTestData(cls):
        """
        Load the mock data files.
        It should import 10 clients.
        """
        call_command('importclients', file='mock_clients.csv')

    def test_import_member_info(self):
        self.assertEquals(10, Client.objects.all().count())
        self.assertEquals(10, Member.objects.all().count())
        dorothy = Client.objects.get(member__mid=94)
        created = dorothy.member.created_at
        self.assertEquals(dorothy.member.firstname, 'Dorothy')
        self.assertEquals(dorothy.member.lastname, 'Davis')
        self.assertEquals(dorothy.status, Client.ACTIVE)
        self.assertEquals(dorothy.birthdate, date(1938, 10, 10))
        self.assertEquals(
            date(created.year, created.month, created.day),
            date(2007, 9, 26))
        self.assertEquals(dorothy.gender, 'F')
        self.assertEquals(dorothy.language, 'EN')
        self.assertEquals(dorothy.delivery_type, 'O')
        self.assertEquals(dorothy.route.name, 'McGill')
        self.assertEquals(dorothy.delivery_note, 'Code entree: 17')
        self.assertEquals(dorothy.alert, 'communicate with her sister')

    def test_import_member_status(self):
        self.assertEquals(Client.active.all().count(), 2)
        self.assertEquals(Client.ongoing.all().count(), 2)
        self.assertEquals(Client.pending.all().count(), 1)
        self.assertEquals(Client.contact.all().count(), 6)

    def test_import_member_routes(self):
        self.assertEquals(
            Client.objects.filter(
                route__name='McGill').count(), 2)
        self.assertEquals(
            Client.objects.filter(
                route__name='Westmount').count(), 2)
        self.assertEquals(
            Client.objects.filter(
                route__name='Notre Dame de Grace').count(), 3)
        self.assertEquals(
            Client.objects.filter(
                route__name='Côte-des-Neiges').count(), 2)
        self.assertEquals(
            Client.objects.filter(
                route__name='Centre-Ville / Downtown').count(), 1)


class ImportMemberAddressesTestCase(TestCase):

    """
    Test data importation.
    """

    fixtures = ['routes.json']

    @classmethod
    def setUpTestData(cls):
        """
        Load the mock data files.
        It should import 10 clients.
        """
        call_command('importclients', file='mock_clients.csv')
        call_command('importaddresses', file='mock_addresses.csv')

    def test_import_member_addresses(self):
        self.assertEquals(Address.objects.all().count(), 10)
        dorothy = Member.objects.get(mid=94)
        self.assertEquals(dorothy.address.street, '2070 De Maisoneuve Ouest')
        self.assertEquals(dorothy.address.apartment, 'Apt.ABC')
        self.assertEquals(dorothy.address.postal_code, 'H3G1K9')
        self.assertEquals(dorothy.address.city, 'Montreal')
        self.assertEquals(dorothy.home_phone, '514-666-6666')
        self.assertEquals(dorothy.email, 'ddavis@example.org')

    def test_ut8_charset(self):
        norma = Member.objects.get(mid=91)
        self.assertEquals(norma.address.city, 'Montréal')
        robin = Member.objects.get(mid=99)
        self.assertEquals(robin.address.street, '29874 Côte-des-Neiges')


class ImportMemberRelationshipsTestCase(TestCase):

    """
    Test data importation.
    """

    fixtures = ['routes.json']

    @classmethod
    def setUpTestData(cls):
        """
        Load the mock data files.
        It should import 10 clients.
        """
        call_command('importclients', file='mock_clients.csv')
        call_command('importrelationships', file='mock_relationships.csv')

    def test_import_relationship(self):
        self.assertEquals(10, Client.objects.all().count())
        self.assertEquals(12, Member.objects.all().count())
        dorothy = Client.objects.get(member__mid=94)
        self.assertEquals(str(dorothy.billing_member), 'Alice Cardona')
        self.assertEquals(dorothy.billing_member.rid, 2884)
        self.assertIn(
            dorothy.billing_member.pk,
            [c.pk for c in dorothy.emergency_contacts.all()]
        )
        self.assertIn(
            'daughter',
            [ce.relationship for ce in dorothy.emergencycontact_set.all()]
        )
        self.assertEquals(dorothy.client_referent.all().count(), 0)
        marie = Client.objects.get(member__mid=93)
        marion = Member.objects.get(rid=865)
        self.assertEquals(marie.client_referent.all().count(), 1)
        referencing = marie.client_referent.first()
        self.assertEquals(referencing.referent, marion)
        self.assertEquals(
            referencing.referent.work_information,
            'CLSC St-Louis du Parc'
        )
        self.assertEquals(referencing.referral_reason, 'Low mobility')


class ImportMemberMealsTestCase(TestCase):

    """
    Test data importation.
    """

    fixtures = ['sample_data.json']

    @classmethod
    def setUpTestData(cls):
        """
        Load the mock data files.
        It should import 10 clients.
        """

        cls.food_preparation_puree = Option.objects.get(name='Puree all')
        cls.food_preparation_cut = Option.objects.get(name='Cut up meat')
        call_command('importclients', file='mock_clients.csv')
        call_command('importmeals', file='mock_meals.csv')

    def test_import_meals_schedule(self):
        dorothy = Client.objects.get(member__mid=94)
        # Dorothy is not registered to receive any meals
        self.assertEquals(
            dorothy.simple_meals_schedule,
            []
        )

        robert = Client.objects.get(member__mid=96)
        # Robert is registered to receive a meal 3 times a week
        self.assertEquals(
            robert.simple_meals_schedule,
            ["wednesday", "friday", "saturday"]
        )

        wednesday = robert.meals_schedule['wednesday']
        self.assertEquals(wednesday.get('fruit_salad'), 0)
        self.assertEquals(wednesday.get('green_salad'), 1)
        self.assertEquals(wednesday.get('main_dish'), 1)
        self.assertEquals(wednesday.get('size'), 'R')
        self.assertEquals(wednesday.get('dessert'), 1)
        self.assertEquals(wednesday.get('compote'), 0)
        self.assertEquals(wednesday.get('pudding'), 0)

    def test_import_meals_default(self):
        robert = Client.objects.get(member__mid=96)
        wednesday = robert.meals_schedule['wednesday']
        self.assertEquals(wednesday.get('fruit_salad'), 0)
        self.assertEquals(wednesday.get('green_salad'), 1)
        self.assertEquals(wednesday.get('main_dish'), 1)
        self.assertEquals(wednesday.get('size'), 'R')
        self.assertEquals(wednesday.get('dessert'), 1)
        self.assertEquals(wednesday.get('compote'), 0)
        self.assertEquals(wednesday.get('pudding'), 0)

    def test_import_food_preparation(self):
        robert = Client.objects.get(member__mid=96)
        self.assertEquals(robert.food_preparation.all().count(), 1)
        self.assertEquals(robert.food_preparation.first(),
                          self.food_preparation_cut)
        dorothy = Client.objects.get(member__mid=94)
        self.assertEquals(dorothy.food_preparation.all().count(), 2)

    def test_import_meal_labels(self):
        marie = Client.objects.get(member__mid=93)
        self.assertEquals(marie.notes.all().count(), 0)


class ImportMemberOrdersTestCase(TestCase):

    """
    Test data importation.
    """

    fixtures = ['sample_data.json']

    @classmethod
    def setUpTestData(cls):
        """
        Load the mock data files.
        It should import 10 clients.
        """

        call_command('importclients', file='mock_clients.csv')
        call_command('importorders', file='mock_orders.csv')

    def test_import_orders(self):
        dorothy = Client.objects.get(member__mid=94)
        orders = Order.objects.get_billable_orders_client(11, 2016, dorothy)
        # Dorothy must have one billable order
        self.assertEquals(
            orders.count(),
            1
        )
        self.assertEqual(orders.first().status, 'D')
        self.assertEqual(orders.first().delivery_date, date(2016, 11, 11))

    def test_import_order_items(self):
        dorothy = Client.objects.get(member__mid=94)
        order = Order.objects.get_billable_orders_client(
            11, 2016, dorothy
        ).first()
        items = order.orders
        main_dish = items.get(component_group='main_dish')
        self.assertEqual(main_dish.total_quantity, 2)
        self.assertEqual(main_dish.size, 'L')
        diabetic_dessert = items.get(component_group='diabetic')
        self.assertEqual(diabetic_dessert.total_quantity, 1)
        dessert = items.get(component_group='dessert')
        self.assertEqual(dessert.total_quantity, 1)
