from django.test import TestCase

from rest_framework import status

from unittest.mock import Mock, patch

from api.v1.auth_app.views import SignUpView

from ..services import AuthAppService

class Request():
	def __init__(self):
		self.data = 'some test data'

class Serializer():
	def __init__(self):
		self.validated_data = 'some validated data'

	def is_valid(self, raise_exception=False):
		pass

class UserMock():
	def __init__(self):
		self.full_name = 'test full name'
		self.email = 'test email'
		self.id = 'test id'

class ResponseMock:
	def __init__(self, data=None, status=None):
		self.data = data
		self.status = status

@patch('api.v1.auth_app.views.Response', new=ResponseMock)
@patch('api.v1.auth_app.views.send_information_email')
class ViewsTestCase(TestCase):
	def setUp(self):
		self.AuthAppService_patcher = patch('api.v1.auth_app.views.AuthAppService')
		mock_service_class = self.AuthAppService_patcher.start()

		self.serviceInstance = mock_service_class.return_value
		self.serviceInstance.create_user.return_value = UserMock()
		self.serviceInstance.get_confrim_url.return_value = 'some confirm url'

		self.view = SignUpView()
		self.mockSerializer = Serializer()
		self.view.get_serializer = Mock(return_value=self.mockSerializer)

		self.request = Request()

	def tearDown(self):
		self.AuthAppService_patcher.stop()

	def test_should_call_get_serializer_with_request_data(self, send_information_email):
		self.view.post(self.request)

		self.view.get_serializer.assert_called_once_with(data='some test data')

	def test_should_call_create_user_with_validated_data(self, send_information_email):
		self.view.post(self.request)

		self.serviceInstance.create_user.assert_called_with('some validated data')

	def test_should_call_confirm_url_with_user_id(self, send_information_email):
		self.view.post(self.request)

		self.serviceInstance.get_confrim_url.assert_called_once_with('test id')

	def test_should_send_email(self, send_information_email):
		self.view.post(self.request)

		send_information_email.assert_called_with(
			subject='Confirm your email',
			template_name='emails/confirmation.html',
			context={ 'name': 'test full name', 'confirm_url': 'some confirm url' },
			to_email='test email'
		)

	def test_should_return_response_with_201_status(self, send_information_email):
		response = self.view.post(self.request)

		self.assertEqual(response.status, status.HTTP_201_CREATED)

	def test_should_through_exception_when_is_valid_wrong(self, send_information_email):
		self.mockSerializer.is_valid = Mock(side_effect = Exception('data is not valid'))

		with self.assertRaises(Exception) as cm:
			self.view.post(self.request)

		the_exception = cm.exception

		self.assertEqual(the_exception.args[0], 'data is not valid')
		self.serviceInstance.create_user.assert_not_called()
		send_information_email.assert_not_called()
