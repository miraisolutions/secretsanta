from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP  # Note: Required for the type hint to work
from typing import Dict, Tuple, Union, List


class SecretSanta:
    # https://docs.python.org/3/tutorial/classes.html
    """Custom SecretSanta class with send method"""
    # https://thomas-cokelaer.info/tutorials/sphinx/docstring_python.html

    # leading underscore indicates this attribute is protected (convention only!)
    _helper = 'rudolph'

    # getter-only decorator @property, exposing the helper attribute.
    # It is afterwards accessed like any attribute, i.e. without ().
    @property
    def helper(self: "SecretSanta") -> str:
        return self._helper

    # "SecretSanta" string type hint follows Python 3.6 convention, see
    # https://stackoverflow.com/questions/33533148/how-do-i-specify-that-the-return-type-of-a-method-is-the-same-as-the-class-itsel
    # for more modern ways to use a class within its own definition as a type hint

    # constructor
    def __init__(self: "SecretSanta", email: Union[str, List[str]], person: str) -> None:
        # https://stackoverflow.com/questions/5599254/how-to-use-sphinxs-autodoc-to-document-a-classs-init-self-method
        """init method

        Args:
            email: email address(es).
            person: person.

        Returns:
            Class instance.

        Example:
            >>> from secretsanta.main.core import SecretSanta
            >>> obj = SecretSanta('me@gmail.com', 'you')
            >>> obj.helper
            'rudolph'
        """
        self.email = email
        self.person = person

    # Note: Instead of returning a dictionary, it may also raise an error (see SMTP.sendmail documentation)
    def send(self: "SecretSanta", subject: str, from_address: str,
             message: str, mailserver: SMTP, test: bool = False) -> Dict[str, Tuple[int, bytes]]:
        """ Method for sending out emails

        Args:
            subject: subject for email
            from_address: sender email address
            message: customizable part of email body (message), which is prepended to ``self.person``
            mailserver: SMTP server object (initialized via :func:`smtplib.SMTP`)
            test: boolean to switch on extra subject and message text, indicating the email is sent for test purposes
        Returns:
            Send-status of email as returned by :func:`smtplib.sendmail`, empty if all were successful
        """
        message = (
            f'Hi there!\n\n{message} {self.person}.\n\nHo Ho Ho,\n\nSanta\n\n'
            'This is an automated message. Please do not reply!'
        )

        if test:
            message = 'THIS IS JUST A TEST, NOT THE FINAL SECRET SANTA ASSIGNMENT!\n\n' + message
            subject += ' - THIS IS JUST A TEST!'

        msg = MIMEMultipart("alternative")
        # https://mail.python.org/pipermail//bangpypers/2012-October/008356.html
        sender = 'Santa'
        msg.add_header('reply-to', sender)
        msg["From"] = f'{sender} <{from_address}>'
        msg["Subject"] = subject
        # ternary operator: https://en.wikipedia.org/wiki/%3F:#Python
        msg["To"] = ','.join(self.email) if isinstance(self.email, list) else self.email
        msg.attach(MIMEText(message, 'plain'))

        res = mailserver.sendmail(from_address, self.email, msg.as_string())
        return res
