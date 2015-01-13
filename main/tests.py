from django.test import TestCase
from django.test import RequestFactory
from django.core.urlresolvers import resolve
from django.shortcuts import render_to_response
from .views import index
from payments.models import User
import mock

class MainPageTests(TestCase):

    #### SETUP ####

    @classmethod
    def setUpClass(cls):
        request_factory = RequestFactory()
        cls.request = request_factory.get('/')
        cls.request.session = {}

    ### TEST ROUTES ####

    def test_root_resolves_to_main_view(self):
        main_page = resolve('/')
        self.assertEqual(main_page.func, index)

    def test_returns_appropriate_html_response_code(self):
        resp = index(self.request)
        self.assertEquals(resp.status_code, 200)

    #### TEST TEMPALTES AND VIEWS ####

    def test_returns_exact_html(self):
        resp = index(self.request)
        self.assertEquals(
            resp.content,
            render_to_response("index.html").content
        )

    def test_index_handles_logged_in_user(self):
        # create the user needed for user lookup from index page
        user = User(
            name='jj',
            email='j@j.com',
        )
        
        # create a sessions that appears to have a logged in user
        self.request.session = {"user": "1"}

        with mock.patch('main.views.User') as user_mock:

            # tll the mock what to do when caleed
            config = {'get_by_id.return_value': mock.Mock()}
            user_mock.configure_mock(**config)

            #run the test
            resp = index(self.request)

            # ensure we return the state of the session back to normal
            self.request.session = {}

            expectedHtml = render_to_response(
                'user.html', {'user': user_mock.get_by_id(1)}
            )
            self.assertEquals(resp.content, expectedHtml.content)