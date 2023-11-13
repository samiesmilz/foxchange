import unittest
from unittest.mock import patch
from app import app, get_currency_list, get_live_rates, make_api_request, session, requests


class TestApp(unittest.TestCase):

    def setUp(self):
        """Set up a test client and context."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Clean up after the test."""
        self.app_context.pop()

    def test_homepage(self):
        """Test the homepage route."""
        with self.app:
            response = self.app.get('/')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                '<h2 id="exchange-rates-title">Live Exchange Rates</h2>', html)

            # Testing session data
            self.assertIn('currencies', session)
            self.assertIn('quotes', session)

    def test_post_data_invalid_amount(self):
        """Test the post_data route with an invalid amount."""
        with self.app:
            response = self.app.post(
                '/convert', data={'amount': 'abc', 'currency-from': 'USD', 'currency-to': 'EUR'})
            self.assertIn(b'Please enter a valid amount!', response.data)

    def test_post_data_valid_amount(self):
        """Test the post_data route with a valid amount."""
        with self.app:
            response = self.app.post(
                '/convert', data={'amount': '100', 'currency-from': 'USD', 'currency-to': 'EUR'})
            self.assertEqual(response.status_code, 200)

    @patch('app.make_api_request')
    def test_get_live_rates(self, mock_make_api_request):
        """Test the get_live_rates view function.
        The function should make an API request, update the session
        with the quotes, and return the quotes.
        """
        app.config["BASE_URL"] = "http://api.exchangerate.host/"
        app.config["API_KEY"] = "5125409f04b854153066e6ee9a41f7c8"
        mock_response = {'quotes': {'USDEUR': 0.85, 'USDGBP': 0.75}}
        mock_make_api_request.return_value = mock_response
        with app.test_request_context('/live?code=USD'):
            result = get_live_rates()

            mock_make_api_request.assert_called_once_with(
                f"{app.config['BASE_URL']}/live", {"access_key": app.config['API_KEY'], "source": 'USD'})

            self.assertIn('quotes', session)
            self.assertEqual(session['quotes'], mock_response['quotes'])
            self.assertEqual(result, mock_response['quotes'])

    @patch('app.requests.get')
    def test_make_api_request_success(self, mock_get):
        """Test make_api_request with a successful request.
        # Define the expected mock response
        # Call the function with mock parameters
        """
        expected_response = {'key': 'value'}
        mock_get.return_value.json.return_value = expected_response
        result = make_api_request(
            'https://example.com/api', {'param': 'value'})
        mock_get.assert_called_once_with(
            'https://example.com/api', params={'param': 'value'})
        self.assertEqual(result, expected_response)

    @patch('app.requests.get')
    def test_make_api_request_failure(self, mock_get):
        """Test make_api_request with a failed request.
        # Simulate an exception during the request
        # Call the function with mock parameters
        """

        mock_get.side_effect = requests.exceptions.RequestException(
            'Connection error')
        result = make_api_request(
            'https://example.com/api', {'param': 'value'})
        mock_get.assert_called_once_with(
            'https://example.com/api', params={'param': 'value'})
        self.assertEqual(
            result, {'error': 'Error making API request: Connection error'})
