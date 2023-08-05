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
Views for app upgrades
"""

from __future__ import unicode_literals, absolute_import

import os
import re
import logging

import six
from sqlalchemy import orm

from rattail.core import Object
from rattail.db import model, Session as RattailSession
from rattail.time import make_utc
from rattail.threads import Thread
from rattail.upgrades import get_upgrade_handler

from deform import widget as dfwidget
from webhelpers2.html import tags, HTML

from tailbone.views import MasterView
from tailbone.progress import get_progress_session #, SessionProgress


log = logging.getLogger(__name__)


class UpgradeView(MasterView):
    """
    Master view for all user events
    """
    model_class = model.Upgrade
    downloadable = True
    cloneable = True
    executable = True
    execute_progress_template = '/upgrade.mako'
    execute_progress_initial_msg = "Upgrading"

    labels = {
        'executed_by': "Executed by",
        'status_code': "Status",
        'stdout_file': "STDOUT",
        'stderr_file': "STDERR",
    }

    grid_columns = [
        'created',
        'description',
        # 'not_until',
        'enabled',
        'status_code',
        'executed',
        'executed_by',
    ]

    form_fields = [
        'description',
        # 'not_until',
        # 'requirements',
        'notes',
        'created',
        'created_by',
        'enabled',
        'executing',
        'executed',
        'executed_by',
        'status_code',
        'stdout_file',
        'stderr_file',
        'exit_code',
        'package_diff',
    ]

    def __init__(self, request):
        super(UpgradeView, self).__init__(request)
        self.handler = self.get_handler()

    def get_handler(self):
        """
        Returns the ``UpgradeHandler`` instance for the view.  The handler
        factory for this may be defined by config, e.g.:

        .. code-block:: ini

           [rattail.upgrades]
           handler = myapp.upgrades:CustomUpgradeHandler
        """
        return get_upgrade_handler(self.rattail_config)

    def configure_grid(self, g):
        super(UpgradeView, self).configure_grid(g)
        g.set_joiner('executed_by', lambda q: q.join(model.User, model.User.uuid == model.Upgrade.executed_by_uuid).outerjoin(model.Person))
        g.set_sorter('executed_by', model.Person.display_name)
        g.set_enum('status_code', self.enum.UPGRADE_STATUS)
        g.set_type('created', 'datetime')
        g.set_type('executed', 'datetime')
        g.set_sort_defaults('created', 'desc')
        g.set_link('created')
        g.set_link('description')
        # g.set_link('not_until')
        g.set_link('executed')

    def grid_extra_class(self, upgrade, i):
        if upgrade.status_code == self.enum.UPGRADE_STATUS_FAILED:
            return 'warning'
        if upgrade.status_code == self.enum.UPGRADE_STATUS_EXECUTING:
            return 'notice'

    def template_kwargs_view(self, **kwargs):
        upgrade = kwargs['instance']

        kwargs['show_prev_next'] = True
        kwargs['prev_url'] = None
        kwargs['next_url'] = None

        upgrades = self.Session.query(model.Upgrade)\
                               .filter(model.Upgrade.uuid != upgrade.uuid)
        older = upgrades.filter(model.Upgrade.created <= upgrade.created)\
                        .order_by(model.Upgrade.created.desc())\
                        .first()
        newer = upgrades.filter(model.Upgrade.created >= upgrade.created)\
                        .order_by(model.Upgrade.created)\
                        .first()

        if older:
            kwargs['prev_url'] = self.get_action_url('view', older)
        if newer:
            kwargs['next_url'] = self.get_action_url('view', newer)

        return kwargs

    def configure_form(self, f):
        super(UpgradeView, self).configure_form(f)

        # status_code
        if self.creating:
            f.remove_field('status_code')
        else:
            f.set_enum('status_code', self.enum.UPGRADE_STATUS)
            # f.set_readonly('status_code')

        # executing
        if not self.editing:
            f.remove('executing')

        f.set_type('created', 'datetime')
        f.set_type('enabled', 'boolean')
        f.set_type('executed', 'datetime')
        # f.set_widget('not_until', dfwidget.DateInputWidget())
        f.set_widget('notes', dfwidget.TextAreaWidget(cols=80, rows=8))
        f.set_renderer('stdout_file', self.render_stdout_file)
        f.set_renderer('stderr_file', self.render_stdout_file)
        f.set_renderer('package_diff', self.render_package_diff)
        # f.set_readonly('created')
        # f.set_readonly('created_by')
        f.set_readonly('executed')
        f.set_readonly('executed_by')
        upgrade = f.model_instance
        if self.creating or self.editing:
            f.remove_field('created')
            f.remove_field('created_by')
            f.remove_field('stdout_file')
            f.remove_field('stderr_file')
            if self.creating or not upgrade.executed:
                f.remove_field('executed')
                f.remove_field('executed_by')
            if self.editing and upgrade.executed:
                f.remove_field('enabled')

        elif f.model_instance.executed:
            f.remove_field('enabled')

        else:
            f.remove_field('executed')
            f.remove_field('executed_by')
            f.remove_field('stdout_file')
            f.remove_field('stderr_file')

        if not self.viewing or not upgrade.executed:
            f.remove_field('package_diff')
            f.remove_field('exit_code')

    def configure_clone_form(self, f):
        f.fields = ['description', 'notes', 'enabled']

    def clone_instance(self, original):
        cloned = self.model_class()
        cloned.created = make_utc()
        cloned.created_by = self.request.user
        cloned.description = original.description
        cloned.notes = original.notes
        cloned.status_code = self.enum.UPGRADE_STATUS_PENDING
        cloned.enabled = original.enabled
        self.Session.add(cloned)
        self.Session.flush()
        return cloned

    def render_stdout_file(self, upgrade, fieldname):
        if fieldname.startswith('stderr'):
            filename = 'stderr.log'
        else:
            filename = 'stdout.log'
        path = self.rattail_config.upgrade_filepath(upgrade.uuid, filename=filename)
        if path:
            url = '{}?filename={}'.format(self.get_action_url('download', upgrade), filename)
            return self.render_file_field(path, url, filename=filename)
        return filename

    def render_package_diff(self, upgrade, fieldname):
        use_buefy = self.get_use_buefy()
        try:
            before = self.parse_requirements(upgrade, 'before')
            after = self.parse_requirements(upgrade, 'after')

            kwargs = {}
            if use_buefy:
                kwargs['extra_row_attrs'] = self.get_extra_diff_row_attrs
            diff = self.make_diff(before, after,
                                  columns=["package", "old version", "new version"],
                                  render_field=self.render_diff_field,
                                  render_value=self.render_diff_value,
                                  **kwargs)

            kwargs = {}
            if use_buefy:
                kwargs['@click.prevent'] = "showingPackages = 'all'"
                kwargs[':style'] = "{'font-weight': showingPackages == 'all' ? 'bold' : null}"
            else:
                kwargs['class_'] = 'all'
            all_link = tags.link_to("all", '#', **kwargs)

            kwargs = {}
            if use_buefy:
                kwargs['@click.prevent'] = "showingPackages = 'diffs'"
                kwargs[':style'] = "{'font-weight': showingPackages == 'diffs' ? 'bold' : null}"
            else:
                kwargs['class_'] = 'diffs'
            diffs_link = tags.link_to("diffs only", '#', **kwargs)

            kwargs = {}
            if not use_buefy:
                kwargs['class_'] = 'showing'
            showing = HTML.tag('div', c=["showing: "
                                         + all_link
                                         + " / "
                                         + diffs_link],
                               **kwargs)

            return HTML.tag('div', c=[showing + diff.render_html()])

        except:
            log.debug("failed to render package diff for upgrade: {}".format(upgrade), exc_info=True)
            return HTML.tag('div', c="(not available for this upgrade)")

    def get_extra_diff_row_attrs(self, field, attrs):
        # note, this is only needed/used with Buefy
        extra = {}
        if attrs.get('class') != 'diff':
            extra['v-show'] = "showingPackages == 'all'"
        return extra

    def changelog_link(self, project, url):
        return tags.link_to(project, url, target='_blank')

    commit_hash_pattern = re.compile(r'^.{40}$')

    def get_changelog_projects(self):
        projects = {
            'rattail': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/rattail/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/rattail/files/{new_version}/CHANGES.rst',
            },
            'Tailbone': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone/files/{new_version}/CHANGES.rst',
            },
            'pyCOREPOS': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/pycorepos/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/pycorepos/files/{new_version}/CHANGES.rst',
            },
            'rattail_corepos': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-corepos/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-corepos/files/{new_version}/CHANGES.rst',
            },
            'tailbone_corepos': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone-corepos/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone-corepos/files/{new_version}/CHANGES.rst',
            },
            'onager': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-restricted/onager/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-restricted/onager/files/{new_version}/CHANGES.rst',
            },
            'rattail-onager': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-restricted/rattail-onager/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-restricted/rattail-onager/files/{new_version}/CHANGELOG.md',
            },
            'rattail_tempmon': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-tempmon/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-tempmon/files/{new_version}/CHANGES.rst',
            },
            'tailbone-onager': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-restricted/tailbone-onager/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-restricted/tailbone-onager/files/{new_version}/CHANGELOG.md',
            },
            'rattail_woocommerce': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-woocommerce/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/rattail-woocommerce/files/{new_version}/CHANGES.rst',
            },
            'tailbone_woocommerce': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone-woocommerce/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/tailbone-woocommerce/files/{new_version}/CHANGES.rst',
            },
            'tailbone_theo': {
                'commit_url': 'https://kallithea.rattailproject.org/rattail-project/theo/changelog/{new_version}/?size=10',
                'release_url': 'https://kallithea.rattailproject.org/rattail-project/theo/files/{new_version}/CHANGES.rst',
            },
        }
        return projects

    def get_changelog_url(self, project, old_version, new_version):
        projects = self.get_changelog_projects()

        project_name = project
        if project_name not in projects:
            # cannot generate a changelog URL for unknown project
            return

        project = projects[project_name]

        if self.commit_hash_pattern.match(new_version):
            return project['commit_url'].format(new_version=new_version, old_version=old_version)

        elif re.match(r'^\d+\.\d+\.\d+$', new_version):
            return project['release_url'].format(new_version=new_version, old_version=old_version)

    def render_diff_field(self, field, diff):
        old_version = diff.old_value(field)
        new_version = diff.new_value(field)
        url = self.get_changelog_url(field, old_version, new_version)
        if url:
            return self.changelog_link(field, url)
        return field

    def render_diff_value(self, field, value):
        if value is None:
            return ""
        if value.startswith("u'") and value.endswith("'"):
            return value[2:1]
        return value

    def parse_requirements(self, upgrade, type_):
        packages = {}
        path = self.rattail_config.upgrade_filepath(upgrade.uuid, filename='requirements.{}.txt'.format(type_))
        with open(path, 'rt') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    req = self.parse_requirement(line)
                    if req:
                        packages[req.name] = req.version
                    else:
                        log.warning("could not parse req from line: %s", line)
        return packages

    def parse_requirement(self, line):
        match = re.match(r'^.*@(.*)#egg=(.*)$', line)
        if match:
            return Object(name=match.group(2), version=match.group(1))

        match = re.match(r'^(.*)==(.*)$', line)
        if match:
            return Object(name=match.group(1), version=match.group(2))

    def download_path(self, upgrade, filename):
        return self.rattail_config.upgrade_filepath(upgrade.uuid, filename=filename)

    def download_content_type(self, path, filename):
        return 'text/plain'

    def before_create_flush(self, upgrade, form):
        upgrade.created_by = self.request.user
        upgrade.status_code = self.enum.UPGRADE_STATUS_PENDING

    # TODO: this was an attempt to make the progress bar survive Apache restart,
    # but it didn't work...  need to "fork" instead of waiting for execution?
    # def make_execute_progress(self):
    #     key = '{}.execute'.format(self.get_grid_key())
    #     return SessionProgress(self.request, key, session_type='file')

    def execute_instance(self, upgrade, user, **kwargs):
        session = orm.object_session(upgrade)
        self.handler.mark_executing(upgrade)
        session.commit()
        self.handler.do_execute(upgrade, user, **kwargs)

    def execute_progress(self):
        upgrade = self.get_instance()
        key = '{}.execute'.format(self.get_grid_key())
        session = get_progress_session(self.request, key)
        if session.get('complete'):
            msg = session.get('success_msg')
            if msg:
                self.request.session.flash(msg)
        elif session.get('error'):
            self.request.session.flash(session.get('error_msg', "An unspecified error occurred."), 'error')
        data = dict(session)

        path = self.rattail_config.upgrade_filepath(upgrade.uuid, filename='stdout.log')
        offset = session.get('stdout.offset', 0)
        if os.path.exists(path):
            size = os.path.getsize(path) - offset
            if size > 0:
                with open(path, 'rb') as f:
                    f.seek(offset)
                    chunk = f.read(size)
                    data['stdout'] = chunk.decode('utf8').replace('\n', '<br />')
                session['stdout.offset'] = offset + size
                session.save()

        return data

    def delete_instance(self, upgrade):
        self.handler.delete_files(upgrade)
        super(UpgradeView, self).delete_instance(upgrade)

    @classmethod
    def defaults(cls, config):
        route_prefix = cls.get_route_prefix()
        url_prefix = cls.get_url_prefix()
        permission_prefix = cls.get_permission_prefix()
        model_key = cls.get_model_key()

        # execution progress
        config.add_route('{}.execute_progress'.format(route_prefix), '{}/{{{}}}/execute/progress'.format(url_prefix, model_key))
        config.add_view(cls, attr='execute_progress', route_name='{}.execute_progress'.format(route_prefix),
                        permission='{}.execute'.format(permission_prefix), renderer='json')

        cls._defaults(config)


def includeme(config):
    UpgradeView.defaults(config)
