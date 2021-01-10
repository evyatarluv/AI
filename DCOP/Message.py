from typing import Any


class Message:

    """
    Class for representing messages.

    You can use the `title` attribute to define the message type in order you run
    the algorithm with different threads.


    """
    # todo: add class docstrings

    def __init__(self, sender, recipient, content, title='message'):

        self.sender: int = sender
        self.recipient: int = recipient
        self.content: Any = content
        self.title: str = title

    def __str__(self):

        return 'Title: {} From: {}, To: {}, Content: {}'.format(self.title, self.sender,
                                                                self.recipient, self.content)
