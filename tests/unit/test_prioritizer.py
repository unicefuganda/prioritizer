import json
from unittest import TestCase
from mock import patch, Mock, call
import prioritizer


class TestPrioritizer(TestCase):
    def setUp(self):
        self.app = prioritizer.app.test_client()

    @patch("models.prioritylist.Blacklist.poll_text")
    def test_that_poll_text_is_called_with_poll_text_when_adding_poll_to_blacklist(self, mocked_poll_text_method):
        mocked_form_data = self.mock_request()
        self.app.post("/blacklist/add", data=mocked_form_data)

        expected = [call("345", "sample poll text"), call("345", "sample poll response")]

        self.assertEqual(mocked_poll_text_method.mock_calls, expected)

    @patch("models.prioritylist.Blacklist.delete_poll_text")
    def test_that_the_delete_poll_text_method_is_called_with_poll_text_and_poll_response(self,
                                                                                         mocked_delete_poll_text_method):
        mocked_form_data = self.mock_request()
        self.app.post("/blacklist/delete", data=mocked_form_data)

        expected = [call("345", "sample poll text"), call("345", "sample poll response")]

        self.assertEqual(mocked_delete_poll_text_method.mock_calls, expected)

    @patch("models.prioritylist.Blacklist.poll_contacts")
    def test_that_the_poll_contacts_method_is_called_with_contact_list(self, mocked_poll_contacts_method):
        number_list = [34343434, 3434243432, 2432432432, 342432432]
        json_contact_data = json.dumps(number_list)

        self.app.post("/blacklist/contacts?poll_id=123", data=json_contact_data)

        mocked_poll_contacts_method.assert_called_with(123, number_list)

    def mock_request(self):
        return dict(poll_id="345", poll_text="sample poll text", poll_response="sample poll response")

    def mock_contacts_request(self):
        return dict()