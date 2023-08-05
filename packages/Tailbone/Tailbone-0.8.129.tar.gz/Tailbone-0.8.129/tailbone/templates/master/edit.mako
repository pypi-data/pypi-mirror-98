## -*- coding: utf-8; -*-
<%inherit file="/master/form.mako" />

<%def name="title()">Edit: ${instance_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
  <script type="text/javascript">

    $(function() {

        $('form').submit(function() {
            var submit = $(this).find('input[type="submit"]');
            if (submit.length) {
                submit.button('disable').button('option', 'label', "Saving, please wait...");
            }
        });

    });
  </script>
  % endif
</%def>

<%def name="context_menu_items()">
  % if master.viewable and request.has_perm('{}.view'.format(permission_prefix)):
      <li>${h.link_to("View this {}".format(model_title), action_url('view', instance))}</li>
  % endif
  ${self.context_menu_item_delete()}
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
</%def>


${parent.body()}
