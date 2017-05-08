"""The watchgmail library
"""

import apiclient
import email
import json

class WatchGmail(object):
    """Primary interface into the watch gmail library
    """


    def __init__ (self, http, mailbox, cursor=None):
        """Initialize WatchGmail

        Args:
            http (http): An oauthed http object from the google oauth system
            cursor (str): The cursor data to load the current position in the inbox
        """
        self._api = apiclient.discovery.build('gmail', 'v1', http=http)
        self._mailbox = mailbox

        if cursor is None:
            profile = self._api.users().getProfile(userId=mailbox).execute()
            self._cursor_last_history_id = int(profile['historyId'])
        else:
            cursor_dict = json.loads(cursor)
            self._cursor_last_history_id = cursor_dict['last_history_id']

    @property
    def cursor(self):
        """str: JSON representation of the inbox cursor"""
        cursor_data = json.dumps({'last_history_id': self._cursor_last_history_id})
        return cursor_data

    def read(self):
        """Read a bunch of messages from gmail.

        In most cases a single email will be returned and the cursor
        will move forward in time. It is possible for multiple message 
        to be contained in a single page of history

        A ``None`` will be returned if there are no message after the current history

        Returns:
            List of email message: A list of email messasges in the next page of history
            None: We are already at the latest history and can not read any more
        """

        history_list = self._api.users().history().list(userId=self._mailbox,
                                                        historyTypes='messageAdded',
                                                        maxResults=1,
                                                        startHistoryId=self._cursor_last_history_id).execute()
        histories = history_list.get('history', [])
        if len(histories) > 0:
            next_history = histories[0]
            next_history_id = int(next_history['id'])
            messages = []
            for message_info in next_history.get('messagesAdded', []):
                message_id = message_info['message']['id']
                message_info_raw = self._api.users().messages().get(userId=self._mailbox,
                                                                   id=message_id,
                                                                   format='raw').execute()
                message_raw = message_info_raw['raw'].decode('base64')
                message = email.message_from_string(message_raw)
                messages.append(message)
            self._cursor_last_history_id = next_history_id
            return messages
        else:
            return None




