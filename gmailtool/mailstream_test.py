# -*- coding: utf-8 -*-
"""Testing the mailstream python module
"""

from gmailtool import mailstream

import apiclient.http
import json
import os
import unittest


def get_gmail_api_descovery_json():
    this_dir = os.path.dirname(__file__)
    json_path = os.path.join(this_dir, 'mock_gmail_discovery.json')
    fin = open(json_path, 'r')
    data = fin.read()
    return data


def generate_mock_message(message_id,
                          sender='sender@example.adamandpaul.biz',
                          recipient='recipient@example.adamandpaul.biz'):
    """Generate a mock gmail message structure for testing purposes in the raw format

    Implements many of the fields from the api reference:
    https://developers.google.com/gmail/api/v1/reference/users/messages

    Args:
        message_id (str): The ID of the message. The subject line will be set to this
        sender (str): The sender email address
        recipient (str): The recipient email address

    Returns:
        dict: Dictionary structure of a gmail api message
    """
    email_template = 'From: {sender}\n' \
                     'To: {recipient}\n' \
                     'Subject: {message_id}\n' \
                     '\n' \
                     'Content of mock email {message_id}\n' \
                     '\n'
    raw_email = email_template.format(**locals())
    raw_email_encoded = raw_email.encode('base64')
    message = {
        'id': message_id,
        'payload': {
            'headers': [
                {'name': 'from', 'value': sender},
                {'name': 'to', 'value': recipient},
                {'name': 'subject', 'value': message_id},
            ]
        },
        'raw': raw_email_encoded,
    }
    return message


class TestInitializing(unittest.TestCase):
    """Testing initializing GmailMailStream object with/without setting the mail stream cursor"""

    def test_new_stream_should_start_cursor_at_latest_history_from_gmail_user_profile(self):
        http = apiclient.http.HttpMockSequence([
            ({'status': '200'}, get_gmail_api_descovery_json()),
            ({'status': '200'}, '{"historyId": 12345}'),
            ({'status': '403'}, 'Should never be requested'),
        ])
        inbox = mailstream.GmailMailStream(http, 'email@example.adamandpaul.biz')
        self.assertIn('12345', inbox.cursor, 'expected history id of 12345 to be contained in cursor value')

    def test_new_stream_should_init_with_pre_saved_history_id(self):
        http = apiclient.http.HttpMockSequence([
            ({'status': '200'}, get_gmail_api_descovery_json()),
            ({'status': '403'}, 'Should never be requested'),
        ])
        inbox = mailstream.GmailMailStream(http, 'email@example.adamandpaul.biz', cursor='{"last_history_id":7474}')
        self.assertIn('7474', inbox.cursor, 'expected history id of 7474 not contained in cursor value')


class TestNewEmailInInbox(unittest.TestCase):
    """Testing the case of a single new email appearing in the inbox 
    """

    def setUp(self):
        self.test_message_id = 'test1234'
        self.test_message = generate_mock_message(self.test_message_id)
        http = apiclient.http.HttpMockSequence([
            ({'status': '200'}, get_gmail_api_descovery_json()),
            (
                {'status': '200'},
                json.dumps({
                    'history': [
                        {
                            'id': 2,
                            'messagesAdded': [
                                {'message': self.test_message},
                            ]
                        },
                    ]
                })
            ),
            ({'status': '200'}, json.dumps(self.test_message)),
            ({'status': '403'}, 'Should never be requested'),
        ])
        self.inbox = mailstream.GmailMailStream(http,
                                                'recipient@example.adamandpaul.biz',
                                                cursor='{"last_history_id": 1}')

    def test_read_stream_should_return_newly_arrived_message(self):
        inbox = self.inbox
        messages = inbox.read()
        self.assertEqual(len(messages), 1, 'expected exactly one email')
        message = messages[0]
        self.assertEqual(message['subject'], self.test_message_id, 'expected email with subject ' + self.test_message_id)
        self.assertIn('2', inbox.cursor, 'expected cursor to incriment to 2')


class TestNoNewEmail(unittest.TestCase):
    """Testing the case of no new email after the cursor in current inbox
    """

    def setUp(self):
        self.test_message_id = 'test1234'
        self.test_message = generate_mock_message(self.test_message_id)
        http = apiclient.http.HttpMockSequence([
            ({'status': '200'}, get_gmail_api_descovery_json()),
            (
                {'status': '200'},
                json.dumps({
                    'history': []
                })
            ),
            ({'status': '403'}, 'Should never be requested'),
        ])
        self.inbox = mailstream.GmailMailStream(http,
                                                'recipient@example.adamandpaul.biz',
                                                cursor='{"last_history_id": 1}')

    def test_read_should_return_none_when_inbox_has_no_new_messages(self):
        inbox = self.inbox
        messages = inbox.read()
        self.assertIsNone(messages, 'No more messages in inbox, read should return None')
        self.assertIn('1', inbox.cursor, 'Expected cursor to remain at 1')


class TestMultipleEmailsInSingleHistory(unittest.TestCase):
    """Testing the case of a single new email appearing in the inbox 
    """

    def setUp(self):
        self.test_message_1_id = 'test1234'
        self.test_message_1 = generate_mock_message(self.test_message_1_id)
        self.test_message_2_id = 'test5432'
        self.test_message_2 = generate_mock_message(self.test_message_2_id)
        http = apiclient.http.HttpMockSequence([
            ({'status': '200'}, get_gmail_api_descovery_json()),
            (
                {'status': '200'},
                json.dumps({
                    'history': [
                        {
                            'id': 2,
                            'messagesAdded': [
                                {'message': self.test_message_1},
                                {'message': self.test_message_2},
                            ]
                        },
                    ]
                })
            ),
            ({'status': '200'}, json.dumps(self.test_message_1)),
            ({'status': '200'}, json.dumps(self.test_message_2)),
            ({'status': '403'}, 'Should never be requested'),
        ])
        self.inbox = mailstream.GmailMailStream(http,
                                                'recipient@example.adamandpaul.biz',
                                                cursor='{"last_history_id": 1}')

    def test_read_stream_should_return_newly_arrived_message(self):
        inbox = self.inbox
        messages = inbox.read()
        self.assertEqual(len(messages), 2, 'expected exactly two emails')
        message_1 = messages[0]
        self.assertEqual(message_1['subject'],
                         self.test_message_1_id,
                         'expected email with subject ' + self.test_message_1_id)
        message_2 = messages[1]
        self.assertEqual(message_2['subject'],
                         self.test_message_2_id,
                         'expected email with subject ' + self.test_message_2_id)
        self.assertIn('2', inbox.cursor, 'expected cursor to incriment to 2')
