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
User Views
"""

from __future__ import unicode_literals, absolute_import

import copy

import six
from sqlalchemy import orm

from rattail.db import model
from rattail.db.auth import administrator_role, guest_role, authenticated_role, set_user_password, has_permission

import colander
from deform import widget as dfwidget
from webhelpers2.html import HTML, tags

from tailbone import forms
from tailbone.db import Session
from tailbone.views import MasterView
from tailbone.views.principal import PrincipalMasterView, PermissionsRenderer


class UserView(PrincipalMasterView):
    """
    Master view for the User model.
    """
    model_class = model.User
    has_rows = True
    model_row_class = model.UserEvent
    has_versions = True

    grid_columns = [
        'username',
        'person',
        'active',
        'local_only',
    ]

    form_fields = [
        'username',
        'person',
        'first_name_',
        'last_name_',
        'display_name_',
        'active',
        'active_sticky',
        'set_password',
        'roles',
    ]

    row_grid_columns = [
        'type_code',
        'occurred',
    ]

    mergeable = True
    merge_additive_fields = [
        'sent_message_count',
        'received_message_count',
    ]
    merge_coalesce_fields = [
        'person_uuid',
        'person_name',
        'active',
    ]
    merge_fields = merge_additive_fields + [
        'uuid',
        'username',
        'person_uuid',
        'person_name',
        'role_count',
    ]

    def query(self, session):
        query = super(UserView, self).query(session)

        # bring in the related Person(s)
        query = query.outerjoin(model.Person)\
                     .options(orm.joinedload(model.User.person))

        return query

    def configure_grid(self, g):
        super(UserView, self).configure_grid(g)

        del g.filters['salt']
        g.filters['username'].default_active = True
        g.filters['username'].default_verb = 'contains'
        g.filters['active'].default_active = True
        g.filters['active'].default_verb = 'is_true'
        g.filters['person'] = g.make_filter('person', model.Person.display_name,
                                            default_active=True, default_verb='contains')

        # password
        g.set_filter('password', model.User.password,
                     verbs=['is_null', 'is_not_null'])

        g.set_sorter('person', model.Person.display_name)
        g.set_sorter('first_name', model.Person.first_name)
        g.set_sorter('last_name', model.Person.last_name)
        g.set_sorter('display_name', model.Person.display_name)
        g.set_sort_defaults('username')

        g.set_label('person', "Person's Name")

        g.set_link('username')
        g.set_link('person')
        g.set_link('first_name')
        g.set_link('last_name')
        g.set_link('display_name')

    def editable_instance(self, user):
        """
        If the given user is "protected" then we only allow edit if current
        user is "root".  But if the given user is not protected, this simply
        returns ``True``.
        """
        if self.request.is_root:
            return True
        return not self.user_is_protected(user)

    def deletable_instance(self, user):
        """
        If the given user is "protected" then we only allow delete if current
        user is "root".  But if the given user is not protected, this simply
        returns ``True``.
        """
        if self.request.is_root:
            return True
        return not self.user_is_protected(user)

    def unique_username(self, node, value):
        query = self.Session.query(model.User)\
                            .filter(model.User.username == value)
        if self.editing:
            user = self.get_instance()
            query = query.filter(model.User.uuid != user.uuid)
        if query.count():
            raise colander.Invalid(node, "Username must be unique")

    def configure_form(self, f):
        super(UserView, self).configure_form(f)
        user = f.model_instance

        # username
        f.set_validator('username', self.unique_username)

        # person
        f.set_renderer('person', self.render_person)
        if self.creating or self.editing:
            if 'person' in f.fields:
                f.replace('person', 'person_uuid')
                f.set_node('person_uuid', colander.String(), missing=colander.null)
                person_display = ""
                if self.request.method == 'POST':
                    if self.request.POST.get('person_uuid'):
                        person = self.Session.query(model.Person).get(self.request.POST['person_uuid'])
                        if person:
                            person_display = six.text_type(person)
                elif self.editing:
                    person_display = six.text_type(user.person or '')
                people_url = self.request.route_url('people.autocomplete')
                f.set_widget('person_uuid', forms.widgets.JQueryAutocompleteWidget(
                    field_display=person_display, service_url=people_url))
                f.set_label('person_uuid', "Person")

        # person name(s)
        if self.editing:
            # must explicitly set default, for "custom" field names
            f.set_default('first_name_', user.first_name or "")
            f.set_default('last_name_', user.last_name or "")
            f.set_default('display_name_', user.display_name or "")
        elif not self.creating:
            # must provide custom renderer as well
            f.set_renderer('first_name_', self.render_person_name)
            f.set_renderer('last_name_', self.render_person_name)
            f.set_renderer('display_name_', self.render_person_name)

        # set_password
        f.set_widget('set_password', dfwidget.CheckedPasswordWidget())
        # if self.creating:
        #     f.set_required('password')

        # roles
        f.set_renderer('roles', self.render_roles)
        if self.creating or self.editing:
            if not self.has_perm('edit_roles'):
                f.remove_field('roles')
            else:
                roles = self.get_possible_roles().all()
                role_values = [(s.uuid, six.text_type(s)) for s in roles]
                f.set_node('roles', colander.Set())
                size = len(roles)
                if size < 3:
                    size = 3
                f.set_widget('roles', dfwidget.SelectWidget(multiple=True,
                                                            size=size,
                                                            values=role_values))
                if self.editing:
                    f.set_default('roles', [r.uuid for r in user.roles])
        elif not self.has_perm('view_roles'):
            f.remove_field('roles')

        f.set_label('display_name', "Full Name")

        # # hm this should work according to MDN but doesn't seem to...
        # # https://developer.mozilla.org/en-US/docs/Web/Security/Securing_your_site/Turning_off_form_autocompletion
        # fs.username.attrs(autocomplete='new-password')
        # fs.password.attrs(autocomplete='new-password')
        # fs.confirm_password.attrs(autocomplete='new-password')

        if self.viewing:
            permissions = self.request.registry.settings.get('tailbone_permissions', {})
            f.append('permissions')
            f.set_renderer('permissions', PermissionsRenderer(permissions=permissions,
                                                              include_guest=True,
                                                              include_authenticated=True))

        if self.viewing or self.deleting:
            f.remove('set_password')

    def get_possible_roles(self):

        # some roles should never have users "belong" to them
        excluded = [
            guest_role(self.Session()).uuid,
            authenticated_role(self.Session()).uuid,
        ]

        # only allow "root" user to change admin role membership
        if not self.request.is_root:
            excluded.append(administrator_role(self.Session()).uuid)

        return self.Session.query(model.Role)\
                           .filter(~model.Role.uuid.in_(excluded))\
                           .order_by(model.Role.name)

    def objectify(self, form, data=None):

        # create/update user as per normal
        if data is None:
            data = form.validated
        user = super(UserView, self).objectify(form, data)

        # create/update person as needed
        names = {}
        if 'first_name_' in form and data['first_name_']:
            names['first'] = data['first_name_']
        if 'last_name_' in form and data['last_name_']:
            names['last'] = data['last_name_']
        if 'display_name_' in form and data['display_name_']:
            names['full'] = data['display_name_']
        # we will not have a person reference yet, when creating new user.  if
        # that is the case, go ahead and load it, if specified.
        if self.creating and user.person_uuid:
            self.Session.add(user)
            self.Session.flush()
        # note, do *not* create new person unless name(s) provided
        if not user.person and any([n for n in names.values()]):
            user.person = model.Person()
        if user.person:
            app = self.get_rattail_app()
            handler = app.get_people_handler()
            handler.update_names(user.person, **names)

        # force "local only" flag unless global access granted
        if self.secure_global_objects:
            if not self.has_perm('view_global'):
                user.person.local_only = True

        # maybe set user password
        if data['set_password']:
            set_user_password(user, data['set_password'])

        # update roles for user
        self.update_roles(user, data)

        return user

    def update_roles(self, user, data):
        if not self.has_perm('edit_roles'):
            return
        if 'roles' not in data:
            return

        old_roles = set([r.uuid for r in user.roles])
        new_roles = data['roles']
        admin = administrator_role(self.Session())

        # add any new roles for the user, taking care not to add the admin role
        # unless acting as root
        for uuid in new_roles:
            if uuid not in old_roles:
                if self.request.is_root or uuid != admin.uuid:
                    user._roles.append(model.UserRole(role_uuid=uuid))

        # remove any roles which were *not* specified, although must take care
        # not to remove admin role, unless acting as root
        for uuid in old_roles:
            if uuid not in new_roles:
                if self.request.is_root or uuid != admin.uuid:
                    role = self.Session.query(model.Role).get(uuid)
                    user.roles.remove(role)

    def render_person(self, user, field):
        person = user.person
        if not person:
            return ""
        text = six.text_type(person)
        url = self.request.route_url('people.view', uuid=person.uuid)
        return tags.link_to(person, url)

    def render_person_name(self, user, field):
        if not field.endswith('_'):
            return ""
        name = getattr(user, field[:-1], None)
        if not name:
            return ""
        return six.text_type(name)

    def render_roles(self, user, field):
        roles = user.roles
        items = []
        for role in roles:
            text = role.name
            url = self.request.route_url('roles.view', uuid=role.uuid)
            items.append(HTML.tag('li', c=[tags.link_to(text, url)]))
        return HTML.tag('ul', c=items)

    def get_row_data(self, user):
        return self.Session.query(model.UserEvent)\
                           .filter(model.UserEvent.user == user)

    def configure_row_grid(self, g):
        super(UserView, self).configure_row_grid(g)
        g.width = 'half'
        g.filterable = False
        g.set_sort_defaults('occurred', 'desc')
        g.set_enum('type_code', self.enum.USER_EVENT)
        g.set_label('type_code', "Event Type")
        g.main_actions = []

    def get_version_child_classes(self):
        return [
            (model.UserRole, 'user_uuid'),
        ]

    def find_principals_with_permission(self, session, permission):
        # TODO: this should search Permission table instead, and work backward to User?
        all_users = session.query(model.User)\
                           .filter(model.User.active == True)\
                           .order_by(model.User.username)\
                           .options(orm.joinedload(model.User._roles)\
                                    .joinedload(model.UserRole.role)\
                                    .joinedload(model.Role._permissions))
        users = []
        for user in all_users:
            if has_permission(session, user, permission):
                users.append(user)
        return users

    def get_merge_data(self, user):
        return {
            'uuid': user.uuid,
            'username': user.username,
            'person_uuid': user.person_uuid,
            'person_name': user.person.display_name if user.person else None,
            '_roles': user.roles,
            'role_count': len(user.roles),
            'active': user.active,
            'sent_message_count': len(user.sent_messages),
            'received_message_count': len(user._messages),
        }

    def get_merge_resulting_data(self, remove, keep):
        result = super(UserView, self).get_merge_resulting_data(remove, keep)
        result['role_count'] = len(set(remove['_roles'] + keep['_roles']))
        return result

    def merge_objects(self, removing, keeping):
        # TODO: merge roles, messages
        assert not removing.sent_messages
        assert not removing._messages
        assert not removing._roles
        self.Session.delete(removing)

    @classmethod
    def defaults(cls, config):
        cls._user_defaults(config)
        cls._principal_defaults(config)
        cls._defaults(config)

    @classmethod
    def _user_defaults(cls, config):
        """
        Provide extra default configuration for the User master view.
        """
        permission_prefix = cls.get_permission_prefix()
        model_title = cls.get_model_title()

        # view/edit roles
        config.add_tailbone_permission(permission_prefix, '{}.view_roles'.format(permission_prefix),
                                       "View the Roles to which a {} belongs".format(model_title))
        config.add_tailbone_permission(permission_prefix, '{}.edit_roles'.format(permission_prefix),
                                       "Edit the Roles to which a {} belongs".format(model_title))

# TODO: deprecate / remove this
UsersView = UserView


class UserEventView(MasterView):
    """
    Master view for all user events
    """
    model_class = model.UserEvent
    url_prefix = '/user-events'
    viewable = False
    creatable = False
    editable = False
    deletable = False

    grid_columns = [
        'user',
        'person',
        'type_code',
        'occurred',
    ]

    def get_data(self, session=None):
        query = super(UserEventView, self).get_data(session=session)
        return query.join(model.User)

    def configure_grid(self, g):
        super(UserEventView, self).configure_grid(g)
        g.set_joiner('person', lambda q: q.outerjoin(model.Person))
        g.set_sorter('user', model.User.username)
        g.set_sorter('person', model.Person.display_name)
        g.filters['user'] = g.make_filter('user', model.User.username)
        g.filters['person'] = g.make_filter('person', model.Person.display_name)
        g.set_enum('type_code', self.enum.USER_EVENT)
        g.set_type('occurred', 'datetime')
        g.set_renderer('user', self.render_user)
        g.set_renderer('person', self.render_person)
        g.set_sort_defaults('occurred', 'desc')
        g.set_label('user', "Username")
        g.set_label('type_code', "Event Type")

    def render_user(self, event, column):
        return event.user.username

    def render_person(self, event, column):
        if event.user.person:
            return event.user.person.display_name

# TODO: deprecate / remove this
UserEventsView = UserEventView


def includeme(config):
    UserView.defaults(config)
    UserEventView.defaults(config)
