# -*- coding: utf-8; -*-
################################################################################
#
#  Rattail -- Retail Software Framework
#  Copyright © 2010-2021 Lance Edgar
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
Various common views
"""

from __future__ import unicode_literals, absolute_import

import six

import rattail
from rattail.db import model
from rattail.batch import consume_batch_id
from rattail.mail import send_email
from rattail.util import OrderedDict
from rattail.files import resource_path

from pyramid import httpexceptions
from pyramid.response import Response

import tailbone
from tailbone import forms
from tailbone.forms.common import Feedback
from tailbone.db import Session
from tailbone.views import View
from tailbone.util import set_app_theme
from tailbone.config import global_help_url


class CommonView(View):
    """
    Base class for common views; override as needed.
    """
    project_title = "Tailbone"
    project_version = tailbone.__version__
    robots_txt_path = resource_path('tailbone.static:robots.txt')

    def home(self, **kwargs):
        """
        Home page view.
        """
        if not self.request.user:
            if self.rattail_config.getbool('tailbone', 'login_is_home', default=True):
                raise self.redirect(self.request.route_url('login'))

        image_url = self.rattail_config.get(
            'tailbone', 'main_image_url',
            default=self.request.static_url('tailbone:static/img/home_logo.png'))

        use_buefy = self.get_use_buefy()
        context = {
            'image_url': image_url,
            'use_buefy': use_buefy,
            'help_url': global_help_url(self.rattail_config),
        }
        if use_buefy:
            context['index_title'] = self.rattail_config.node_title()

        if self.expose_quickie_search:
            context['quickie'] = self.get_quickie_context()

        return context

    def robots_txt(self):
        """
        Returns a basic 'robots.txt' response
        """
        with open(self.robots_txt_path, 'rt') as f:
            content = f.read()
        response = self.request.response
        if six.PY3:
            response.text = content
            response.content_type = 'text/plain'
        else:
            response.body = content
            response.content_type = b'text/plain'
        return response

    def exception(self):
        """
        Generic exception view
        """
        return {'project_title': self.project_title}

    def about(self):
        """
        Generic view to show "about project" info page.
        """
        use_buefy = self.get_use_buefy()
        context = {
            'project_title': self.project_title,
            'project_version': self.project_version,
            'packages': self.get_packages(),
            'use_buefy': use_buefy,
        }
        if use_buefy:
            context['index_title'] = self.rattail_config.node_title()
        return context

    def get_packages(self):
        """
        Should return the full set of packages which should be displayed on the
        'about' page.
        """
        return OrderedDict([
            ('rattail', rattail.__version__),
            ('Tailbone', tailbone.__version__),
        ])

    def change_theme(self):
        """
        Simple view which can change user's visible UI theme, then redirect
        user back to referring page.
        """
        theme = self.request.params.get('theme')
        if theme:
            try:
                set_app_theme(self.request, theme, session=Session())
            except Exception as error:
                msg = "Failed to set theme: {}: {}".format(error.__class__.__name__, error)
                self.request.session.flash(msg, 'error')
            else:
                self.request.session.flash("App theme has been changed to: {}".format(theme))
        return self.redirect(self.request.get_referrer())

    def change_db_engine(self):
        """
        Simple view which can change user's "current" database engine, of a
        given type, then redirect back to referring page.
        """
        engine_type = self.request.POST.get('engine_type')
        if engine_type:
            dbkey = self.request.POST.get('dbkey')
            if dbkey:
                self.request.session['tailbone.engines.{}.current'.format(engine_type)] = dbkey
                if self.rattail_config.getbool('tailbone', 'engines.flash_after_change', default=True):
                    self.request.session.flash("Switched '{}' database to: {}".format(engine_type, dbkey))
        return self.redirect(self.request.get_referrer())

    def feedback(self):
        """
        Generic view to handle the user feedback form.
        """
        schema = Feedback().bind(session=Session())
        form = forms.Form(schema=schema, request=self.request)
        if form.validate(newstyle=True):
            data = dict(form.validated)
            if data['user']:
                data['user'] = Session.query(model.User).get(data['user'])
                data['user_url'] = self.request.route_url('users.view', uuid=data['user'].uuid)
            data['client_ip'] = self.request.client_addr
            send_email(self.rattail_config, 'user_feedback', data=data)
            return {'ok': True}
        return {'error': "Form did not validate!"}

    def consume_batch_id(self):
        """
        Consume next batch ID from the PG sequence, and display via flash message.
        """
        batch_id = consume_batch_id(Session())
        self.request.session.flash("Batch ID has been consumed: {:08d}".format(batch_id))
        return self.redirect(self.request.get_referrer())

    def bogus_error(self):
        """
        A special view which simply raises an error, for the sake of testing
        uncaught exception handling.
        """
        raise Exception("Congratulations, you have triggered a bogus error.")

    @classmethod
    def defaults(cls, config):
        cls._defaults(config)

    @classmethod
    def _defaults(cls, config):
        rattail_config = config.registry.settings.get('rattail_config')

        # auto-correct URLs which require trailing slash
        config.add_notfound_view(cls, attr='notfound', append_slash=True)

        # exception
        if rattail_config and rattail_config.production():
            config.add_exception_view(cls, attr='exception', renderer='/exception.mako')

        # permissions
        config.add_tailbone_permission_group('common', "(common)", overwrite=False)

        # home
        config.add_route('home', '/')
        config.add_view(cls, attr='home', route_name='home', renderer='/home.mako')

        # robots.txt
        config.add_route('robots.txt', '/robots.txt')
        config.add_view(cls, attr='robots_txt', route_name='robots.txt')

        # about
        config.add_route('about', '/about')
        config.add_view(cls, attr='about', route_name='about', renderer='/about.mako')

        # change db engine
        config.add_tailbone_permission('common', 'common.change_db_engine',
                                       "Change which Database Engine is active (for user)")
        config.add_route('change_db_engine', '/change-db-engine', request_method='POST')
        config.add_view(cls, attr='change_db_engine', route_name='change_db_engine')

        # change theme
        config.add_tailbone_permission('common', 'common.change_app_theme',
                                       "Change global App Template Theme")
        config.add_route('change_theme', '/change-theme', request_method='POST')
        config.add_view(cls, attr='change_theme', route_name='change_theme')

        # feedback
        config.add_tailbone_permission('common', 'common.feedback',
                                       "Send user feedback (to admins) about the app")
        config.add_route('feedback', '/feedback', request_method='POST')
        config.add_view(cls, attr='feedback', route_name='feedback',
                        renderer='json', permission='common.feedback')

        # consume batch ID
        config.add_tailbone_permission('common', 'common.consume_batch_id',
                                       "Consume new Batch ID")
        config.add_route('consume_batch_id', '/consume-batch-id')
        config.add_view(cls, attr='consume_batch_id', route_name='consume_batch_id')

        # bogus error
        config.add_route('bogus_error', '/bogus-error')
        config.add_view(cls, attr='bogus_error', route_name='bogus_error', permission='errors.bogus')


def includeme(config):
    CommonView.defaults(config)
