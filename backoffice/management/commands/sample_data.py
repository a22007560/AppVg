from django.core.management.base import BaseCommand

from backoffice.models import Client, Address, Contact


class Command(BaseCommand):
    help = 'Load clients into the database'

    def handle(self, *args, **options):
        client1 = Client.objects.create(client=1, name='Client 1', fiscal_name='Client 1 SA', tax_number='123456789')
        address1 = Address.objects.create(client=client1, street='123 Main St', number='1A', city='New York',
                                          postal_code='10001', coordinate_x=40.7128, coordinate_y=-74.0060)
        address2 = Address.objects.create(client=client1, street='456 Second St', number='2B', city='Los Angeles',
                                          postal_code='90012', coordinate_x=34.0522, coordinate_y=-118.2437)
        contact1 = Contact.objects.create(client=client1, status='phone', contact='555-1234')
        contact2 = Contact.objects.create(client=client1, status='email', contact='client1@example.com')

        # Client 2
        client2 = Client.objects.create(
            client=2,
            name='Client Two',
            fiscal_name='Fiscal Name Two',
            tax_number='123456789',
            notes='Notes for Client Two'
        )

        # Addresses for Client 2
        address2_1 = Address.objects.create(
            client=client2,
            street='Street Two One',
            number='12A',
            city='City Two',
            postal_code='1234-567',
            coordinate_x=41.1496,
            coordinate_y=-8.6109,
            notes='Notes for Address Two One'
        )

        address2_2 = Address.objects.create(
            client=client2,
            street='Street Two Two',
            number='23B',
            city='City Two',
            postal_code='2345-678',
            coordinate_x=41.1552,
            coordinate_y=-8.6301,
            notes='Notes for Address Two Two'
        )

        # Contacts for Client 2
        contact2_1 = Contact.objects.create(
            client=client2,
            status='phone',
            contact='919123456',
            notes='Notes for Phone Contact Two One'
        )

        contact2_2 = Contact.objects.create(
            client=client2,
            status='phone',
            contact='913456789',
            notes='Notes for Phone Contact Two Two'
        )

        contact2_3 = Contact.objects.create(
            client=client2,
            status='email',
            contact='email2@example.com',
            notes='Notes for Email Contact Two One'
        )

        # Client 3
        client3 = Client.objects.create(
            client=3,
            name='Client Three',
            fiscal_name='Fiscal Name Three',
            tax_number='123456789',
            notes='Notes for Client Three'
        )

        # Addresses for Client 3
        address3_1 = Address.objects.create(
            client=client3,
            street='Street Three One',
            number='123',
            city='City Three',
            postal_code='3456-789',
            coordinate_x=41.1629,
            coordinate_y=-8.6468,
            notes='Notes for Address Three One'
        )

        address3_2 = Address.objects.create(
            client=client3,
            street='Street Three Two',
            number='234',
            city='City Three',
            postal_code='4567-890',
            coordinate_x=41.1607,
            coordinate_y=-8.6353,
            notes='Notes for Address Three Two'
        )

        # Contacts for Client 3
        contact3_1 = Contact.objects.create(
            client=client3,
            status='phone',
            contact='915123456',
            notes='Notes for Phone Contact Three One'
        )

        contact3_2 = Contact.objects.create(
            client=client3,
            status='email',
            contact='email3@example.com',
            notes='Notes for Email Contact Three One'
        )
