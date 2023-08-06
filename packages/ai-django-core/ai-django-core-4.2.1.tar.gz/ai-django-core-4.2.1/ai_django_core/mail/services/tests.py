from django.core import mail
from django.test import TestCase


class EmailTestService:
    _outbox = None

    def _ensure_outbox_is_loaded(self):
        """
        Ensures that the outbox attribute is set
        """
        if self._outbox is None:
            self.reload()

    def reload(self):
        """
        Loads the current _outbox inside an attribute of this class
        """
        self._outbox = mail.outbox

    def empty(self):
        """
        Empties the current outbox
        :return:
        """
        mail.outbox = []
        self.reload()

    def filter(self, to=None, cc=None, bcc=None, subject=None):
        """
        Searches in the _outbox for emails matching either to and/or subject.
        Returns a list of email objects
        :param to: str
        :param cc: str
        :param bcc: str
        :param subject: str
        :return: EmailTestService
        """
        # Ensure that outbox is up-to-date
        self.reload()

        match_list = []
        for email in self._outbox:
            # Check conditions
            match = True
            if to and to not in email.to:
                match = False
            if cc and cc not in email.cc:
                match = False
            if bcc and bcc not in email.bcc:
                match = False
            if subject and not email.subject == subject:
                match = False
            if not to and not cc and not bcc and not subject:
                raise ValueError('EmailTestService finder called without parameters')

            # Add email if all set conditions are valid
            if match:
                match_list.append(email)

        return EmailTestServiceQuerySet(matching_list=match_list)

    def all(self):
        """
        Loads all mails from the outbox inside the matching list
        :return:
        """
        # Ensure that outbox is up-to-date
        self.reload()

        # Load data to matching list
        match_list = []
        for email in self._outbox:
            match_list.append(email)

        return EmailTestServiceQuerySet(matching_list=match_list)


class EmailTestServiceQuerySet(TestCase):
    _match_list = None

    def __init__(self, matching_list=None):
        super().__init__()
        self._match_list = matching_list

    def _validate_lookup_cache_contains_one_element(self):
        """
        Ensures that in the cached lookup is exactly one element. Needed for full-text-search.
        """
        if self.count() > 1:
            raise RuntimeError('Current lookup has more than one email object and is thus ambiguous.')
        elif self.count() == 0:
            raise RuntimeError('Current lookup has zero matches so lookup does not make sense.')

    def _ensure_matching_list_was_populated(self):
        """
        Make sure that we queried at least once before working with the results
        """
        if self._match_list is None:
            raise RuntimeError('Counting of matches called without previous query. Please call find() or all() first.')

    def _get_html_content(self):
        """
        Ensure we just have found one element and then return HTML part of the email
        :return: str
        """
        # Search for string
        if len(self._match_list[0].alternatives) > 0:
            return self._match_list[0].alternatives[0][0]
        return None

    def _get_txt_content(self):
        """
        Ensure we just have found one element and then return text part of the email
        :return: str
        """
        # Search for string
        return self._match_list[0].body

    def one(self):
        """
        Checks if the previous query returned exactly one element
        :return: bool
        """
        return self.count() == 1

    def count(self):
        """
        Returns the number of matches found by a previous call of `find()`
        :return: int
        """
        # Ensure is was queried before using results
        self._ensure_matching_list_was_populated()

        # Count matches
        return len(self._match_list)

    def first(self):
        """
        Returns the first found element
        :return: EmailMultiAlternatives
        """
        # Ensure is was queried before using results
        self._ensure_matching_list_was_populated()

        return self._match_list[0] if self.count() > 0 else False

    def last(self):
        """
        Returns the last found element
        :return: EmailMultiAlternatives
        """
        # Ensure is was queried before using results
        self._ensure_matching_list_was_populated()

        return self._match_list[self.count() - 1] if self.count() > 0 else False

    def assert_one(self, msg=None):
        """
        Makes an assertion to make sure queried element exists exactly once
        :param msg: str
        :return:
        """
        self.assertEqual(self.one(), True, msg=msg)

    def assert_quantity(self, target_quantity, msg=None):
        """
        Makes an assertion to make sure that amount of queried mails are equal to `target_quantity`
        :param target_quantity: int
        :param msg: str
        :return:
        """
        self.assertEqual(self.count(), target_quantity, msg=msg)

    def assert_subject(self, subject, msg=None):
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        :param subject: str
        :param msg: str
        """
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()

        # Assert expected subject is equal to the generated one
        self.assertEqual(subject, self._match_list[0].subject, msg=msg)

    def assert_body_contains(self, search_str, msg=None):
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        :param search_str: str
        :param msg: str
        """
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()

        # Assert string is contained in TXT part
        self.assertIn(search_str, self._get_txt_content(), msg=msg)
        # Assert string is contained in HTML part (if HTML part is set)
        html_content = self._get_html_content()
        if html_content is not None:
            self.assertIn(search_str, html_content, msg=msg)

    def assert_body_contains_not(self, search_str, msg=None):
        """
        Searches in a given email inside the HTML AND TXT part for a given string
        :param search_str: str
        :param msg: str
        """
        # Ensure we just have found one element
        self._validate_lookup_cache_contains_one_element()

        # Assert string is contained in HTML part
        self.assertNotIn(search_str, self._get_html_content(), msg=msg)
        # Assert string is contained in TXT part
        self.assertNotIn(search_str, self._get_txt_content(), msg=msg)
