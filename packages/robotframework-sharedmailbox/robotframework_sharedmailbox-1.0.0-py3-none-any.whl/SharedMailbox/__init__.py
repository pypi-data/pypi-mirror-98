from exchangelib import Credentials, Account
from robot.api.deco import keyword, library
import datetime

@library
class SharedMailbox(object):
    ROBOT_LIBRARY_SCOPE = 'TEST CASE'

    @keyword('Get The Last Email')
    def get_last_email(self, user, password, mailbox, subject):
        """
        Get the subject of the last email of the given account.
        | get_last_email | user=email_adress | password=password | mailbox=mailbox | subject=subject
        """
        enter_credentials = Credentials(user, password)
        account = Account(mailbox, credentials=enter_credentials, autodiscover=True)
        account.inbox.filter(subject__contains=subject)
        for item in account.inbox.filter(subject__contains=subject).order_by('-datetime_received')[
                    :1]:
            return str(item.account), item.to_recipients, item.subject, item.datetime_received.strftime("%d-%m-%Y %H:%M:%S")
