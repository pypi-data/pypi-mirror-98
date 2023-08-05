## -*- coding: utf-8; -*-
<%inherit file="/master/form.mako" />

<%def name="title()">${index_title} &raquo; ${instance_title}</%def>

<%def name="extra_javascript()">
  ${parent.extra_javascript()}
  % if not use_buefy:
      % if master.deletable and instance_deletable and request.has_perm('{}.delete'.format(permission_prefix)) and master.delete_confirm == 'simple':
          <script type="text/javascript">

            $(function () {

                $('#context-menu a.delete-instance').on('click', function() {
                    if (confirm("Are you sure you wish to delete this ${model_title}?")) {
                        $(this).parents('form').submit();
                    }
                    return false;
                });

            });

          </script>
      % endif
      % if master.has_rows:
          <script type="text/javascript">
            $(function() {
                $('.grid-wrapper').gridwrapper();
            });
          </script>
      % endif
  % endif
</%def>

<%def name="extra_styles()">
  ${parent.extra_styles()}
  % if master.has_rows and not use_buefy:
      <style type="text/css">
        .grid-wrapper {
            margin-top: 10px;
        }
      </style>
  % endif
</%def>

<%def name="content_title()">
  ${instance_title}
</%def>

<%def name="context_menu_items()">
  <li>${h.link_to("Permalink for this {}".format(model_title), action_url('view', instance))}</li>
  % if master.has_versions and request.rattail_config.versioning_enabled() and request.has_perm('{}.versions'.format(permission_prefix)):
      <li>${h.link_to("Version History", action_url('versions', instance))}</li>
  % endif
  % if master.editable and instance_editable and request.has_perm('{}.edit'.format(permission_prefix)):
      <li>${h.link_to("Edit this {}".format(model_title), action_url('edit', instance))}</li>
  % endif
  ${self.context_menu_item_delete()}
  % if master.creatable and master.show_create_link and request.has_perm('{}.create'.format(permission_prefix)):
      % if master.creates_multiple:
          <li>${h.link_to("Create new {}".format(model_title_plural), url('{}.create'.format(route_prefix)))}</li>
      % else:
          <li>${h.link_to("Create a new {}".format(model_title), url('{}.create'.format(route_prefix)))}</li>
      % endif
  % endif
  % if master.cloneable and request.has_perm('{}.clone'.format(permission_prefix)):
      <li>${h.link_to("Clone this as new {}".format(model_title), url('{}.clone'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.touchable and request.has_perm('{}.touch'.format(permission_prefix)):
      <li>${h.link_to("\"Touch\" this {}".format(model_title), url('{}.touch'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.has_rows and master.rows_downloadable_csv and request.has_perm('{}.row_results_csv'.format(permission_prefix)):
      <li>${h.link_to("Download row results as CSV", url('{}.row_results_csv'.format(route_prefix), uuid=instance.uuid))}</li>
  % endif
  % if master.has_rows and master.rows_downloadable_xlsx and master.has_perm('row_results_xlsx'):
      <li>${h.link_to("Download row results as XLSX", master.get_action_url('row_results_xlsx', instance))}</li>
  % endif
</%def>

<%def name="render_row_grid_tools()">
  ${rows_grid_tools}
</%def>

<%def name="render_this_page()">
  ${parent.render_this_page()}
  % if master.has_rows:
      % if use_buefy:
          <br />
          <tailbone-grid></tailbone-grid>
      % else:
          ${rows_grid|n}
      % endif
  % endif
</%def>

<%def name="render_this_page_template()">
  % if master.has_rows:
      ## TODO: stop using |n filter
      ${rows_grid.render_buefy(allow_save_defaults=False, tools=capture(self.render_row_grid_tools))|n}
  % endif
  ${parent.render_this_page_template()}
</%def>

<%def name="make_this_page_component()">
  % if master.has_rows:
  <script type="text/javascript">

    TailboneGrid.data = function() { return TailboneGridData }

    Vue.component('tailbone-grid', TailboneGrid)

  </script>
  % endif
  ${parent.make_this_page_component()}
</%def>


${parent.body()}
