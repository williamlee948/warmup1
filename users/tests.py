<<<<<<< HEAD
=======

>>>>>>> Update users/tests.py
'''should be the same as testadditional because everything is in models.py'''

import unittest
import testLib

SUCCESS               =   1  # : a success
ERR_BAD_CREDENTIALS   =  -1  # : (for login only) cannot find the user/password pair in the database
ERR_USER_EXISTS       =  -2  # : (for add only) trying to add a user that already exists
ERR_BAD_USERNAME      =  -3  # : (for add, or login) invalid user name (only empty string is invalid for now)
ERR_BAD_PASSWORD      =  -4

class Tests(testLib.RestTestCase):
    def assertResponse(self, respData, count = -1, errCode = testLib.RestTestCase.SUCCESS):
        """
        Check that the response data dictionary matches the expected values
        """
        expected = { 'errCode' : errCode }
        if count != -1:
            expected['count']  = count
        self.assertDictEqual(expected, respData)

    '''test login with invalid username'''
    def testlogin1(self):
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : '', 'password' : 'password'} )
        self.assertResponse(respData, errCode = ERR_BAD_USERNAME)
        
    '''test login with non existant username'''
    def testlogin2(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : 'password'} )
        self.assertResponse(respData, errCode = ERR_BAD_CREDENTIALS)
        
    ''''test login on empty database'''
    def testlogin3(self):
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, errCode = ERR_BAD_CREDENTIALS)
        
    '''test login with wrong password'''
    def testlogin4(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'passwor'} )
        self.assertResponse(respData, errCode = ERR_BAD_CREDENTIALS)
        
    '''test login'''
    def testlogin5(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 2)

    '''test login multiple times'''
    def testlogin6(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 3)
        
    '''test login with multiple users and multiple times'''
    def testlogin7(self):
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password1'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : 'password2'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user2', 'password' : 'password2'} )
        self.assertResponse(respData, count = 2)
        respData = self.makeRequest("/users/login", method="POST", data = { 'user' : 'user3', 'password' : 'password3'} )
        self.assertResponse(respData, count = 3)
        
    def testAddExists(self):
        """
        Tests that adding a duplicate user name fails
        """
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, errCode = ERR_USER_EXISTS)

    def testAdd2(self):
        """
        Tests that adding two users works
        """
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user1', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : 'user2', 'password' : 'password'} )
        self.assertResponse(respData, count = 1)

    def testAddEmptyUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        respData = self.makeRequest("/users/add", method="POST", data = { 'user' : "", 'password' : 'password'} )
        self.assertResponse(respData, errCode = ERR_BAD_USERNAME)

'''import unittest
import sys
import models

class TestUsers(unittest.TestCase):
    """
    Unittests for the Users model class (a sample, incomplete)
    """
    def setUp(self):
        self.users = models
        models.TESTAPI_resetFixture("")

        
    def testAdd1(self):
        """
        Tests that adding a user works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))

    def testAddExists(self):
        """
        Tests that adding a duplicate user name fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.ERR_USER_EXISTS, self.users.add("user1", "password"))

    def testAdd2(self):
        """
        Tests that adding two users works
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.add("user2", "password"))

    def testAddEmptyUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.add("", "password"))

    def testEmptyLogin(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("hi", "password"))

    def testBadLoginUsername(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_USERNAME, self.users.login("", "password"))

    def testLogin(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.login("user1", "password"))

    def testLogin2(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.login("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.login("user1", "password"))

    def testWrongLogin(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.SUCCESS, self.users.add("user1", "password"))
        self.assertEquals(models.SUCCESS, self.users.login("user1", "password"))
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("user2", "password"))

    def testWrongLogin2(self):
        """
        Tests that adding an user with empty username fails
        """
        self.assertEquals(models.ERR_BAD_CREDENTIALS, self.users.login("user2", "password"))


# If this file is invoked as a Python script, run the tests in this module
if __name__ == "__main__":
    # Add a verbose argument
    sys.argv = [sys.argv[0]] + ["-v"] + sys.argv[1:]
    unittest.main()
'''
