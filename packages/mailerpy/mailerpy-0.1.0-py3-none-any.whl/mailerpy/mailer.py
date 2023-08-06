import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
from email.utils import make_msgid, formatdate


class Mailer:

    def __init__(self, mail_host, mail_port, mail_address, mail_password):
        self.mail_host = mail_host
        self.mail_port = mail_port
        self.mail_address = mail_address
        self.mail_password = mail_password
        self.msg = MIMEMultipart()

    def send_mail(self, to_address, subject, mail_body, mail_body_args=None, mail_cc=None, mail_bcc=None,
                  attachments=None,
                  file_as_html=None, compression=None, password=None):
        """
        Sends mail with specified details

        :param to_address: Address to which mail has to be sent
        :type to_address: list
        :param subject: Subject of the mail
        :type subject: str
        :param mail_body: Body of mail.Can be plain or parameterized with {KEY}
        :type mail_body: str
        :param mail_body_args: Key-value pair to be replaced on parameterized mail_body
        :type mail_body_args: dict
        :param mail_cc: CC mail addresses for the mail
        :type mail_cc: list
        :param mail_bcc: BCC mail addresses for the mail
        :type mail_bcc: list
        :param attachments: Attachment path for the mail
        :type attachments: list
        :param file_as_html: If excel or csv attachment has to be sent as html
        :type file_as_html: bool
        :param compression: Compression method for files in mail
        :type compression: str
        :param password: Password to open mail attachment
        :type password: str
        :return: Nothing
        """

        # If there are no cc and bcc then assign them as empty list
        # List is easier to operate than None
        mail_cc = [] if mail_cc is None else mail_cc
        mail_bcc = [] if mail_bcc is None else mail_bcc

        # Check if input data are valid for function to work or not
        self.__data_assertion(to_address=to_address, subject=subject, mail_body_args=mail_body_args, mail_cc=mail_cc,
                              mail_bcc=mail_bcc, attachments=attachments)

        # Compose message for mailing with given arguments
        self.msg = MIMEMultipart()
        self.msg['Message-Id'] = make_msgid()
        self.msg['Date'] = formatdate(localtime=True)
        self.msg['From'] = self.mail_address
        self.msg['To'] = ', '.join(to_address)
        self.msg['cc'] = ', '.join(mail_cc)
        self.msg['Subject'] = subject
        self.__compose_body(mail_body=mail_body, mail_body_args=mail_body_args, file_as_html=file_as_html)
        self.__attach_files(attachments)
        self.__deliver_mail(receiver_address=to_address + mail_cc + mail_bcc)
        return

    def __data_assertion(self, to_address, subject, mail_body_args, mail_cc, mail_bcc, attachments):
        """
        Checks if provided arguments are of valid data type and values or not

        :param to_address: Address to which mail has to be sent
        :type to_address: list
        :param subject: Subject of the mail
        :type subject: list
        :param mail_body_args: Key-value pair to be replaced on parameterized mail_body
        :type mail_body_args: dict
        :param mail_cc: CC mail addresses for the mail
        :type mail_cc: list
        :param mail_bcc: BCC mail addresses for the mail
        :type mail_bcc: list
        :param attachments: Attachment path for the mail
        :type attachments: list
        """
        if not isinstance(to_address, list):
            raise TypeError('to_address should be of type list')
        if not isinstance(mail_cc, list):
            raise TypeError('mail_cc should be of type list')
        if not isinstance(mail_bcc, list):
            raise TypeError('mail_cc should be of type list')
        if mail_body_args is not None and not isinstance(mail_body_args, dict):
            raise TypeError('mail_body_args should be of type dictionary')
        if not isinstance(subject, str):
            raise TypeError('subject should be of type string')
        if attachments is not None and not isinstance(attachments, list):
            raise TypeError('attachments should be as type list of attachment file')

    def __compose_body(self, mail_body, mail_body_args, file_as_html):
        """
        Compose body of mail by replacing parameters with actual values

        :param mail_body: Body for mail
        :type mail_body: str
        :param mail_body_args: Key value pair to replace in mail_body
        :type mail_body_args: dict
        :return: Attach body to be sent on mail
        """
        if not file_as_html:
            if mail_body_args is None:
                self.msg.attach(MIMEText(mail_body, 'plain'))
                return

            try:
                self.msg.attach(MIMEText(mail_body.format(**mail_body_args), 'plain'))
            except KeyError as e:
                raise ValueError('Parameter of mail_body not found in mail_body_args')
        else:
            if mail_body_args is None:
                self.msg.attach(MIMEText(mail_body, 'html'))
                return
            try:
                self.msg.attach(MIMEText(mail_body.format(**mail_body_args), 'html'))
            except KeyError as e:
                raise ValueError('Parameter of mail_body not found in mail_body_args')
        return

    def __attach_files(self, attachments):
        """
        Attach given files to the mail

        :param attachments: List of file paths to be attached in mail
        :type attachments: list
        :return: None
        """
        if attachments is None:
            return

        def extract_file_name(path_of_file):
            """
            Extract file name from file path. Useful if absolute path is given

            :return:
            :param path_of_file: list of path of files to be attached in mail
            :type path_of_file: list
            :return: None
            """
            regex_pattern = "[ \w-]+?(?=\.).*$"
            name_of_file = re.findall(regex_pattern, path_of_file)

            # If file name is not found or multiple files are found then path is invalid
            if len(name_of_file) != 1:
                raise ValueError('Invalid file_attachment')
            return ''.join(name_of_file)

        # Extract file names for file path and attach one by one
        attachment_names = list(map(extract_file_name, attachments))
        for attachment_name, attachment_path in zip(attachment_names, attachments):
            payload = MIMEBase('application', 'octet-stream')

            try:
                payload.set_payload(open(attachment_path, "rb").read())
            except FileNotFoundError:
                raise FileNotFoundError("File doesn't exist. Check path or extension")

            encode_base64(payload)
            payload.add_header('Content-Disposition', "attachment; filename= %s" % attachment_name)
            self.msg.attach(payload)
        return

    def __deliver_mail(self, receiver_address):
        """
        Send mail by connection with mail server

        :param receiver_address: Receivers of mail including cc and bcc
        :type receiver_address: list
        :return: Nothing
        """
        with(smtplib.SMTP(self.mail_host, self.mail_port)) as mail_session:
            mail_session.starttls()
            mail_session.login(self.mail_address, self.mail_password)
            mail_as_string = self.msg.as_string()
            mail_session.sendmail(self.mail_address, receiver_address, mail_as_string)
            mail_session.quit()
        return
