from typing import Any


class Message:

    """
    Class for representing messages.

    You can use the `title` attribute to define the message type in order you run
    the algorithm with different threads.

    The class consist of different types of messages:

        1. Value - message with the value of the sender. the content include an int.

        2. Offer - message with an offer for the sender to the recipient. The content of an offer
                   include a dict as follows: {neighbors_values , constraints, value}.

        3. Response - message with a response to an offer. The content include a dict with
                      the follows structure: {accept, value (of the recipient), gain}. The `value`
                      and `gain` keys will be included only if accept is `True`.


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
