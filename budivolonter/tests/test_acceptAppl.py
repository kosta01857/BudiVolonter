import time
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.shortcuts import redirect
from django.test import (Client, LiveServerTestCase, RequestFactory,
                         SimpleTestCase, TestCase)
from django.urls import resolve, reverse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ApplicationUnitTest(TestCase):
    def setUp(self):
        from ..model_funcs import (insertActivity, insertOrganization,
                                  insertVolunteer)
        self.factory:RequestFactory = RequestFactory()
        self.user = insertVolunteer('marko','markovic','1990-01-01','marko@gmail.com', 'Pass1234','') 
        self.org = insertOrganization(ime='TestOrg',pib=88888888,telefon='0616357399',email='org@gmail.com',lozinka='Pass1234')
        self.act = insertActivity(org=self.org,name='testAkt',desc='',spots=1,startD='2024-09-09',endD='2025-02-02',deadline='2025-02-01',reqs='',city='',country='Srbija',categories='') 
