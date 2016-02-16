# -*- coding: utf-8 -*-
# vim: set sts=4 sw=4 :

from trac.core import Component

MODE = 'quietmode'
LISTEN = 'quietlisten'

class QuietSystem(Component):

    def is_quiet_mode (self, user):
	with self.env.db_query as db:
	    cursor = db.cursor()
	    cursor.execute("""
		    SELECT value
		    FROM session_attribute
		    WHERE sid=%s
		    AND name=%s
		    """, (user, MODE))
	    result = cursor.fetchone()
	    if not result:
	       return False
	    return result[0] == '1'


import re
import email
from trac.notification import SmtpEmailSender
from trac.resource import ResourceNotFound
from trac.ticket.model import Ticket
class QuietSmtpEmailSender (SmtpEmailSender):

    TICKET_URI_RE = re.compile(r'/ticket/(?P<tktid>[0-9]+)'
                               r'(?:#comment:(?P<cnum>[0-9]+))?\Z')

    def send (self, from_addr, recipients, message):
	parsed = email.message_from_string(message)
	link = parsed.get('X-Trac-Ticket-URL')
	if link:
	    match = self.TICKET_URI_RE.search(link)
	    if match:
		tktid = match.group('tktid')
		cnum = match.group('cnum')
		if cnum is not None:
		    cnum = int(cnum)

		try:
		    ticket = Ticket(self.env, tktid)
		except ResourceNotFound:
		    pass

		change = ticket.get_change(cnum)
		if change:
		    author = change.get('author', None)
		    fields = change.get('fields', None)
		    if not author and fields:
			author = fields[0]['author']

		    if author and\
		       QuietSystem(self.env).is_quiet_mode(change['author']):
			return
	
	SmtpEmailSender.send(self, from_addr, recipients, message)
