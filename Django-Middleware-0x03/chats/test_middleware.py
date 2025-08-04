import os
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .middleware import RequestLoggingMiddleware
from .models import User

class MiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password', role='guest')

    def tearDown(self):
        if os.path.exists('requests.log'):
            os.remove('requests.log')

    def test_request_logging_middleware_anonymous(self):
        middleware = RequestLoggingMiddleware(lambda req: None)
        request = self.factory.get('/test-path')
        request.user = AnonymousUser()
        middleware(request)
        self.assertTrue(os.path.exists('requests.log'))
        with open('requests.log', 'r') as f:
            log_entry = f.read()
            self.assertIn('User: Anonymous', log_entry)
            self.assertIn('Path: /test-path', log_entry)

    def test_request_logging_middleware_authenticated(self):
        middleware = RequestLoggingMiddleware(lambda req: None)
        request = self.factory.get('/test-path-auth')
        request.user = self.user
        middleware(request)
        self.assertTrue(os.path.exists('requests.log'))
        with open('requests.log', 'r') as f:
            log_entry = f.read()
            self.assertIn(f'User: {self.user}', log_entry)
            self.assertIn('Path: /test-path-auth', log_entry)

    def test_restrict_access_by_time_middleware_allowed(self):
        from .middleware import RestrictAccessByTimeMiddleware
        from unittest.mock import patch
        middleware = RestrictAccessByTimeMiddleware(lambda req: 'allowed')
        request = self.factory.get('/any-path')
        with patch.object(RestrictAccessByTimeMiddleware, 'get_current_time', return_value=__import__('datetime').datetime.strptime('19:00', '%H:%M').time()):
            result = middleware(request)
            self.assertEqual(result, 'allowed')

    def test_restrict_access_by_time_middleware_denied(self):
        from .middleware import RestrictAccessByTimeMiddleware
        from unittest.mock import patch
        middleware = RestrictAccessByTimeMiddleware(lambda req: 'allowed')
        request = self.factory.get('/any-path')
        with patch.object(RestrictAccessByTimeMiddleware, 'get_current_time', return_value=__import__('datetime').datetime.strptime('22:00', '%H:%M').time()):
            result = middleware(request)
            from django.http import HttpResponseForbidden
            self.assertIsInstance(result, HttpResponseForbidden)

    def test_offensive_language_middleware_rate_limit(self):
        from .middleware import OffensiveLanguageMiddleware
        from django.http import HttpRequest
        middleware = OffensiveLanguageMiddleware(lambda req: 'ok')
        request = self.factory.post('/api/messages')
        request.META['REMOTE_ADDR'] = '1.2.3.4'
        # Clear cache for test
        from django.core.cache import cache
        for i in range(5):
            result = middleware(request)
            self.assertEqual(result, 'ok')
        result = middleware(request)
        from django.http import HttpResponseForbidden
        self.assertIsInstance(result, HttpResponseForbidden)

    def test_role_permission_middleware_admin(self):
        from .middleware import RolePermissionMiddleware
        middleware = RolePermissionMiddleware(lambda req: 'ok')
        request = self.factory.get('/api/messages')
        request.user = self.user
        self.user.role = 'admin'
        self.user.save()
        result = middleware(request)
        self.assertEqual(result, 'ok')

    def test_role_permission_middleware_non_admin(self):
        from .middleware import RolePermissionMiddleware
        middleware = RolePermissionMiddleware(lambda req: 'ok')
        request = self.factory.get('/api/messages')
        request.user = self.user
        self.user.role = 'guest'
        self.user.save()
        result = middleware(request)
        from django.http import HttpResponseForbidden
        self.assertIsInstance(result, HttpResponseForbidden)
