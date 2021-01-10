from typing import Any


class Message:

    """
    Class for representing messages.

    Attributes:
    ----------

        sender: (int)
            the id of sender of the message

        recipient: (int)
            the id of the recipient of the message

        content: (Any)
            the content of the messages, can be any content

        title: (str)
            the title of the message, for debug convenient
    """

    def __init__(self, sender, recipient, content, title='message'):

        self.sender: int = sender
        self.recipient: int = recipient
        self.content: Any = content
        self.title: str = title

    def __str__(self):

        return 'Title: {} From: {}, To: {}, Content: {}'.format(self.title, self.sender,
                                                                self.recipient, self.content)

