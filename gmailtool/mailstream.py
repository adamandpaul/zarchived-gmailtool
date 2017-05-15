"""The mailstream module
"""

import apiclient
import email
import json

class GmailMailStream(object):
    """Present the Gmail API as a mail stream which can be sequentially accessed by .read()
    """


    def __init__ (self, http, mailbox, cursor=None):
        """Initialize a Gmail mail stream object

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
        
        Each time read is called it will attempt advance one history at at time.
        If advancing the history was successful then a list of email messages that were
        added to the mailbox will be returned. If we are at the most current history for the
        inbox and thus history was not advanced then None is returned.
        
        It is possible that an empty list is returned signifiying that history was advanced
        but no new emails were added in the new history. Call read() another time to advance
        further.

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




