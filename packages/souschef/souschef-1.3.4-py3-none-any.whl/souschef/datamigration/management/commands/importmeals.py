import csv

from django.core.management.base import BaseCommand
from souschef.member.models import Client, Member
from souschef.member.models import Option, Client_option


class Command(BaseCommand):
    help = 'Data: import clients relationships from given csv file.'

    ROW_MID = 0
    ROW_MON = 1
    ROW_TUE = 2
    ROW_WED = 3
    ROW_THU = 4
    ROW_FRI = 5
    ROW_SAT = 6
    ROW_FOOD_PREP_PUREE = 7
    ROW_FOOD_PREP_CUT = 8
    ROW_MLABEL = 9
    ROW_ING_BEEF = 10

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            default=False,
            help='Import mock data instead of actual data',
        )

    def handle(self, *args, **options):
        if options['file']:
            file = 'mock_meals.csv'
        else:
            file = 'clients_meals.csv'

        food_prep_puree = Option.objects.get(
            name='Puree all'
        )
        food_prep_cut = Option.objects.get(
            name='Cut up meat'
        )

        with open(file) as f:
            reader = csv.reader(f, delimiter=';')
            for row in reader:
                try:
                    member = Member.objects.get(mid=row[self.ROW_MID])
                    client = Client.objects.get(member=member)
                    days = [
                        self.ROW_MON,
                        self.ROW_TUE,
                        self.ROW_WED,
                        self.ROW_THU,
                        self.ROW_FRI,
                        self.ROW_SAT
                    ]
                    meals_schedule = []
                    prefs = {}

                    for day in days:
                        if row[day] != "":
                            meals_schedule.append(row[day])
                            delivery_day = day - 1
                            # Hack: there is no column Thursday in the csv file
                            if delivery_day > 3:
                                delivery_day -= 1

                            prefs['size_' + row[day]] = \
                                row[11 + (delivery_day * 10) + 1]
                            prefs['main_dish_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 0])
                            prefs['dessert_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 5])
                            prefs['fruit_salad_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 2])
                            prefs['green_salad_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 3])
                            prefs['pudding_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 6])
                            prefs['diabetic_' + row[day] + '_quantity'] = \
                                int(row[11 + (delivery_day * 10) + 4])

                    client.set_simple_meals_schedule(meals_schedule)
                    client.meal_default_week = prefs
                    client.save()

                    # Food preparation
                    if row[self.ROW_FOOD_PREP_CUT] == '1':
                        Client_option.objects.create(
                            client=client,
                            option=food_prep_cut
                        )
                    if row[self.ROW_FOOD_PREP_PUREE] == '1':
                        Client_option.objects.create(
                            client=client,
                            option=food_prep_puree
                        )

                except Member.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING('Non existing member'))
                except Client.DoesNotExist:
                    self.stdout.write(
                        self.style.WARNING('Non existing client'))
