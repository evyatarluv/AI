

class Message:

    def __init__(self, sender, recipient, content):

        self.sender = sender
        self.recipient = recipient
        self.content = content

        # todo: title to messages? maybe can help to debug later...

    def __str__(self):

        return 'From: {}, To: {}, Content: {}'.format(self.sender, self.recipient, self.content)
