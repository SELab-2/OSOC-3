class WebhookProcessException(Exception):
    """The Exception raised when encountering an error while processing the Form"""

    def __init__(self, message):
        super().__init__()
        self.message = message
