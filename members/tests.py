from django.test import TestCase
from models import User, Property
from query import *
from Parkings.members.query import *
# import might be changed after setting django.

class UserTestCase(TestCase):
    def setUp(self):
        User.objects.create(id=1, admin= True, email = 'asdf3q@gmail.com', password = 'S!32st')
        User.objects.create(id=2, admin= False, email = 'asdf8q@gmail.com', password = 'Park!ng')
        Property.objects.create(propertyid = 3, ownerid = 1, name = 'Kingsford', price_weekday = 3, price_weekend = 3.5, size_width = 1.6, size_length =3.2, address = 'Rainbow st, Kingsford', IsDeleted = False)
        Property.objects.create(propertyid = 4, ownerid = 2, name = 'Kingsford', price_weekday = 3, price_weekend = 5.2, size_width = 2.6, size_length =3.6, address = 'Irvine st, Kingsford', IsDeleted = True)
    
    def test_User(self):
        
        per1 = checkLogin('asdf3q@gmail.com', 'S!32st')
        per2 = checkLogin('asdf8q@gmail.com', 'Park!ng')
        
        self.assertEqual(per1.admin == True)
        self.assertEqual(per2.admin == False)

        self.assertEqual(per1.vechicleid == '3')
        self.assertEqual(per2.vechicleid == '1')

    def test_getPropertydetail(self):
        Pro1 = Property.getPropertyDetail(1)
        Pro2 = Property.getPropertyDetail(2)

        self.assertEqual(Pro1.propertyid == 3)
        self.assertEqual(Pro1.ownerid == 1)
        self.assertEqual(Pro1.name == 'Kingsford')
        self.assertEqual(Pro1.price_weekday == 3)
        self.assertEqual(Pro1.price_weekend == 3.5)
        self.assertEqual(Pro1.size_width== 1.6)
        self.assertEqual(Pro1.size_length == 3.2)   
        self.assertEqual(Pro1.IsDeleted == False)
        self.assertEqual(Pro1.address == 'Rainbow st, Kingsford')
        
        #tests for deleted property
        self.assertEqual(Pro2.propertyid == 5)
        self.assertEqual(Pro2.ownerid == 2)
        self.assertEqual(Pro2.name == 'Kingsford')
        self.assertEqual(Pro2.price_weekday == 3)
        self.assertEqual(Pro2.price_weekend == 5.2)
        self.assertEqual(Pro1.IsDeleted == False)
        self.assertEqual(Pro1.address == 'Irvine st, Kingsford')

    def test_checkLogin(self):
        user1 = checkLogin('asdf3q@gmail.com', 'S!32st')
        user2 = checkLogin('sdf8q@gmail.com', 'Park!ng')

        self.assertEqual(user1.id == 1)
        self.assertEqual(user1.Admin == True)
        self.assertEqual(user2 == False)

        self.assertNotEqual(user2.id == 2)
        self.assertNotEqual(user2.Admin == False)
   
# # Run all the tests in the query.tests module
# $ ./manage.py test query.tests

# # Run all the tests found within the 'query' package
# $ ./manage.py test query

# # Run just one test case
# $ ./manage.py test query.tests.queryTestCase

# # Run just one test method
# $ ./manage.py test query.tests.queryTestCase.test_query_can_speak