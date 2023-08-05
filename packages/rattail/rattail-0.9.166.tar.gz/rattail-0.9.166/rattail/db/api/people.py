# -*- coding: utf-8 -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2017 Lance Edgar
#
#  This file is part of Rattail.
#
#  Rattail is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Rattail is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
#  FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
#  details.
#
#  You should have received a copy of the GNU General Public License along with
#  Rattail.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################
"""
People API
"""

from __future__ import unicode_literals

from sqlalchemy.orm.exc import NoResultFound

from rattail.db import model


__all__ = ['get_employee_by_id']


def get_employee_by_id(session, employee_id):
    """
    Fetch an employee record by ID.
    """

    try:
        return session.query(model.Employee)\
            .filter(model.Employee.id == employee_id)\
            .one()
    except NoResultFound:
        return None
