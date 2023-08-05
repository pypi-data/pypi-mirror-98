# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2020 Lance Edgar
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
Report Handlers
"""

from __future__ import unicode_literals, absolute_import

import datetime
import decimal

import six

from rattail.db import model
from rattail.util import load_entry_points, load_object
from rattail.mail import send_email
from rattail.time import localtime


class ReportHandler(object):
    """
    Base class for all report handlers.  Also provides default implementation,
    which is assumed to be sufficient for most needs.
    """
    entry_point_section = 'rattail.reports'

    def __init__(self, config=None, **kwargs):
        self.config = config
        self.enum = config.get_enum() if config else None
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_reports(self):
        """
        Returns a dict of available reports, which are registered via setuptools
        entry points.
        """
        return load_entry_points(self.entry_point_section)

    def get_report(self, key):
        """
        Fetch a report by key.  If the report can be located, this will return an
        instance thereof; otherwise returns ``None``.
        """
        report = self.get_reports().get(key)
        if report:
            return report(self.config)

    def generate_output(self, session, report, params, user, progress=None, **kwargs):
        """
        Generate and return output for the given report and params.
        """
        data = report.make_data(session, params, progress=progress, **kwargs)

        output = model.ReportOutput()
        output.report_name = report.make_report_name(session, params, data, **kwargs)
        output.report_type = report.type_key
        output.params = self.safe_params(**params)
        output.filename = report.make_filename(session, params, data, **kwargs)
        output.created_by = user
        session.add(output)
        session.flush()

        path = output.filepath(self.config, makedirs=True)
        report.write_file(session, params, data, path, progress=progress, **kwargs)
        return output

    def safe_params(self, **kwargs):
        params = {}
        for key, value in six.iteritems(kwargs):
            if isinstance(value, datetime.date):
                value = six.text_type(value)
            elif isinstance(value, decimal.Decimal):
                value = float(value)
            params[key] = value
        return params

    def email_output(self, report, output, mailkey,
                     fallback_mailkey='common_report', extra_data={}, **kwargs):
        """
        Send an email (using the given :paramref:`mailkey`) with the report
        output as an attachment.

        :param report: The relevant :class:`Report` instance.
        :param output: The relevant :class:`ReportOutput` instance.
        :param mailkey: Config key which identifies the type of email to be
           sent.
        :param fallback_mailkey: Config key to be used as fallback, should the
           :paramref:`mailkey` not point to a valid email config.
        :param extra_data: Additional context data to be passed along to the
           email template.
        :param kwargs: Additional kwargs to be passed directly to
           :func:`~rattail.mail.send_email()`.
        """
        if 'attachments' not in kwargs:
            path = output.filepath(self.config)
            kwargs['attachments'] = [path]

        data = {
            'config': self.config,
            'handler': self,
            'report': report,
            'output': output,
            'localtime': localtime,
        }

        if extra_data:
            data.update(extra_data)

        if 'params' not in data:
            data['params'] = output.params

        send_email(self.config, mailkey, data, fallback_key=fallback_mailkey,
                   **kwargs)


def get_report_handler(config, **kwargs):
    """
    Create and return the configured :class:`ReportHandler` instance.
    """
    spec = config.get('rattail.reports', 'handler')
    if spec:
        return load_object(spec)(config)
    return ReportHandler(config)
