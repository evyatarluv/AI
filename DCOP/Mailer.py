from .Message import Message
from typing import List, Dict, Any


class Mailer:

    def __init__(self):

        self.mailbox: Dict[int, List[Message]] = dict()
        self.delivered: List[Message] = []

    def get_messages(self, recipient: int) -> List[Message]:
        """
        Method to get all the messages of a given recipient
        :param recipient: recipient id
        :return: list with all the messages
        """

        return self.mailbox.get(recipient, [])

    def deliver_message(self, sender: int, recipient: int, content: Any, title: str):

        """
        The method create a message and append it to delivered messages list.
        :param title: title of the message
        :param recipient: id of the recipient
        :param sender: id of the sender
        :param content: an object with the content of the message
        :return: none
        """

        msg = Message(sender, recipient, content, title)

        self.delivered.append(msg)

    def assign_messages(self):

        """
        Get all messages from the delivered list and assign them according to the message recipient.
        :return:
        """

        # Empty the current mailbox
        self.mailbox = dict()

        for msg in self.delivered:

            recipient = msg.recipient

            # If this recipient already have messages
            try:
                self.mailbox[recipient].append(msg)

            # Except if we don't have any messages for this recipient yet
            except KeyError:

                self.mailbox[recipient] = [msg]

        # Empty delivered messages
        self.delivered = []







