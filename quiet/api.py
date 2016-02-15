# -*- coding: utf-8 -*-
# vim: set sts=4:sw=4 :

from trac.core import Component

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
