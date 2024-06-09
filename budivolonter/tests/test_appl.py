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

# Create your tests here.

class ApplicationUnitTest(TestCase):
    def setUp(self):
        from ..model_funcs import (insertActivity, insertOrganization,
                                  insertVolunteer)
        self.factory:RequestFactory = RequestFactory()
        self.user = insertVolunteer('marko','markovic','1990-01-01','marko@gmail.com', 'Pass1234','') 
        self.org = insertOrganization(ime='TestOrg',pib=88888888,telefon='0616357399',email='org@gmail.com',lozinka='Pass1234')
        self.act = insertActivity(org=self.org,name='testAkt',desc='',spots=1,startD='2024-09-09',endD='2025-02-02',deadline='2025-02-01',reqs='',city='',country='Srbija',categories='') 
    def test_appOK(self):
        from ..views import activity_form
        from ..utils import getNavbar,getFooter
        from ..model_funcs import getActivityById,getUsrById
        request = self.factory.post(reverse('activity_form'),data={'pismo': 'test'})
        request.GET = {
                'id':    self.act.idakt,
                }
        request.user = self.user
        output = activity_form(request)
        aktivnost = getActivityById(self.act.idakt)
        organizacija =getUsrById(aktivnost.idorg_id)
        context = {
            'naziv':            aktivnost.naziv,
            'datumOd':          aktivnost.datumod,
            'datumDo':          aktivnost.datumdo,
            'organizacija_ime': organizacija.ime,

            'navbar':           getNavbar(request),
            'footer':           getFooter()
        }
        context['success'] = 'Uspesno ste se prijavili na aktivnost'
        expected = render(request, 'activity_form.html', context)
        self.assertEqual (output.content , expected.content)

    def test_appBAD(self):
        from ..views import activity_form
        from ..utils import getNavbar,getFooter
        from ..model_funcs import getActivityById,getUsrById
        request = self.factory.post(reverse('activity_form'),data={'pismo': ''})
        request.GET = {
                'id':    self.act.idakt,
                }
        request.user = self.user
        output = activity_form(request)
        aktivnost = getActivityById(self.act.idakt)
        organizacija =getUsrById(aktivnost.idorg_id)
        context = {
            'naziv':            aktivnost.naziv,
            'datumOd':          aktivnost.datumod,
            'datumDo':          aktivnost.datumdo,
            'organizacija_ime': organizacija.ime,

            'navbar':           getNavbar(request),
            'footer':           getFooter()
        }
        context['success'] = 'Uspesno ste se prijavili na aktivnost'
        expected = render(request, 'activity_form.html', context)
        self.assertNotEqual (output.content , expected.content)



class ApplicationWebTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def test_application(self):
        from ..model_funcs import (getAllActivities, getApplicationsForAct,
                                  insertActivity, insertOrganization,
                                  insertVolunteer)
        insertVolunteer('marko','markovic','1990-01-01','marko@gmail.com', 'Pass1234','')        
        org = insertOrganization(ime='TestOrg',pib=88888888,telefon='0616357399',email='org@gmail.com',lozinka='Pass1234')
        act = insertActivity(org=org,name='testAkt',desc='',spots=1,startD='2024-09-09',endD='2025-02-02',deadline='2025-02-01',reqs='',city='',country='Srbija',categories='') 
        assert(len(getAllActivities()) == 1) 
        self.driver.get(f'{self.live_server_url}/budivolonter/login')
        self.driver.maximize_window()
        email_input = self.driver.find_element(By.NAME, 'email')
        password_input = self.driver.find_element(By.NAME, 'password')
        submit_button = self.driver.find_element(By.ID, 'submit')
        email_input.send_keys('marko@gmail.com')
        password_input.send_keys('Pass1234')
        submit_button.click()
        assert (self.driver.current_url.split('?')[0] == f'{self.live_server_url}/budivolonter/profile')
        self.driver.find_element(By.ID, 'searchActBtn').click()
        assert (self.driver.current_url == f'{self.live_server_url}/budivolonter/search_activity')
        self.driver.find_element(By.NAME, 'prijavaBtn').click()
        assert (self.driver.current_url.split('?')[0] == f'{self.live_server_url}/budivolonter/activity_form')
        pismo = self.driver.find_element(By.NAME, 'pismo')
        pismo.send_keys('TEST PISMO')
        submit_button = self.driver.find_element(By.ID, 'submit')
        submit_button.click()
        assert (len(getApplicationsForAct(idakt=act.idakt)) == 1)

    def tearDown(self):
        self.driver.close()
