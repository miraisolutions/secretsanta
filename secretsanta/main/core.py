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
        # https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
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

    def send(self, subject, from_address, message, mailserver, test=False):
        """
        send method

        :param subject: subject for email
        :param from_address: sender email address
        :param message: customizable part of email body (message), which is prepended to ``self.person``
        :param mailserver: SMTP server object (initialized via :func:`smtplib.SMTP`)
        :param test: boolean to switch on extra subject and message text, indicating the email is sent for test purposes
        :return: send-status of email
        """
        message = 'Hi there!\n\n%s %s.\n\nHo Ho Ho,\n\nSanta\n\n' % (message, self.person) + \
                  'This is an automated message. Please do not reply!'

        if test:
            message = 'THIS IS JUST A TEST, NOT THE FINAL SECRET SANTA ASSIGNMENT!\n\n' + message
            subject += ' - THIS IS JUST A TEST!'

        msg = MIMEMultipart("alternative")
        # https://mail.python.org/pipermail//bangpypers/2012-October/008356.html
        sender = 'santa@mirai-solutions.com'
        msg.add_header('reply-to', sender)
        msg["From"] = sender + ' <' + from_address + '>'
        msg["Subject"] = subject
        # ternary operator: https://en.wikipedia.org/wiki/%3F:#Python
        msg["To"] = ','.join(self.email) if isinstance(self.email, list) and len(self.email) > 1 else self.email
        msg.attach(MIMEText(message, 'plain'))

        res = mailserver.sendmail(from_address, self.email, msg.as_string())
        return res
