from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SecretSanta:
    # https://docs.python.org/3/tutorial/classes.html
    """Custom SecretSanta class with send method"""
    # https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html

    # leading underscore indicates this attribute is protected (convention only!)
    _helper = 'roland'

    # getter-only decorator @property, exposing the helper attribute.
    # It is afterwards accessed like any attribute, i.e. without ().
    @property
    def helper(self):
        return self._helper

    # constructor
    def __init__(self, email, person):
        """
        init method

        :param email: email address
        :param person: person
        :return: class instance

        :Example:

        >>> obj = SecretSanta('me@gmail.com', 'you')
        >>> obj.helper
        'roland'
        """
        self.email = email
        self.person = person

    def send(self, subject, from_address, message, mailserver):
        """
        send method

        :param subject:
        :param from_address:
        :param message:
        :param mailserver:
        :return:
        """
        message = 'Hi there!\n\n%s %s\n\nThis is an automated message. Please do not reply!' % (message, self.person)

        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = from_address
        # ternary operator: https://en.wikipedia.org/wiki/%3F:#Python
        msg["To"] = ','.join(self.email) if isinstance(self.email, list) and len(self.email) > 1 else self.email
        msg.attach(MIMEText(message, 'plain'))

        res = mailserver.sendmail(from_address, self.email, msg.as_string())
        return res
