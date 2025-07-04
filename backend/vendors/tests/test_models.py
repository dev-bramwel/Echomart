from django.test import TestCase
from django.contrib.auth import get_user_model
from vendors.models import Vendor, VendorBankDetails

User = get_user_model()

class VendorModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendoruser', password='securepass')
        self.vendor = Vendor.objects.create(
            user=self.user,
            business_name='Echomart Groceries',
            business_description='Sells fresh farm produce online.',
            business_address='12 Juja Lane, Nairobi',
            business_phone='0700001111',
            business_email='groceries@echomart.com',
            website='https://echomart.co.ke'
        )

    def test_vendor_str_returns_business_name(self):
        self.assertEqual(str(self.vendor), 'Echomart Groceries')

    def test_vendor_defaults(self):
        self.assertFalse(self.vendor.is_verified)
        self.assertTrue(self.vendor.is_active)
        self.assertIsNotNone(self.vendor.created_at)
        self.assertIsNotNone(self.vendor.updated_at)
    
    def test_vendor_bank_details_str(self):
        bank = VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name="KCB Bank",
            account_name="Tech Hub Ltd",
            account_number="0011223344"
        )
        expected = f"{self.vendor.business_name} - {bank.bank_name}"
        self.assertEqual(str(bank), expected)
        
    def test_duplicate_bank_account_number_rejected(self):
            VendorBankDetails.objects.create(
                vendor=self.vendor,
                bank_name="Equity",
                account_name="Test Name",
                account_number="9999999999"
                )
            with self.assertRaises(Exception):  # Could be IntegrityError or ValidationError
                VendorBankDetails.objects.create(
                    vendor=self.vendor,
                    bank_name="Equity 2",
                    account_name="Test Name 2",
                    account_number="9999999999"  # Same number
                    )

class VendorBankDetailsModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='vendorbank', password='bankpass')
        self.vendor = Vendor.objects.create(
            user=self.user,
            business_name='Fuel Station X',
            business_description='Sells fuel',
            business_address='Mombasa Road, Nairobi',
            business_phone='0711112222',
            business_email='stationx@echomart.com'
        )

        self.bank_details = VendorBankDetails.objects.create(
            vendor=self.vendor,
            bank_name='Equity Bank',
            account_name='Fuel Station X',
            account_number='123456789',
            routing_number='EQT123',
            is_default=True
        )

    def test_bank_details_str_format(self):
        expected_str = f'{self.vendor.business_name} - Equity Bank'
        self.assertEqual(str(self.bank_details), expected_str)

    def test_unique_together_constraint(self):
        with self.assertRaises(Exception):  # Expecting IntegrityError or DatabaseError
            VendorBankDetails.objects.create(
                vendor=self.vendor,
                bank_name='Another Bank',
                account_name='Fuel Station X',
                account_number='123456789',  # same as above
                routing_number='XYZ456',
                is_default=False
            )

    def test_defaults_and_timestamps(self):
        self.assertTrue(self.bank_details.is_default)
        self.assertIsNotNone(self.bank_details.created_at)
        self.assertIsNotNone(self.bank_details.updated_at)
