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
Base class for customer order batch views
"""

from __future__ import unicode_literals, absolute_import

import six

from rattail.db import model

import colander

from tailbone import forms
from tailbone.views.batch import BatchMasterView


class CustomerOrderBatchView(BatchMasterView):
    """
    Master view base class, for customer order batches.  The views for the
    various mode/workflow batches will derive from this.
    """
    model_class = model.CustomerOrderBatch
    model_row_class = model.CustomerOrderBatchRow
    default_handler_spec = 'rattail.batch.custorder:CustomerOrderBatchHandler'

    grid_columns = [
        'id',
        'customer',
        'rowcount',
        'total_price',
        'created',
        'created_by',
    ]

    form_fields = [
        'id',
        'customer',
        'person',
        'phone_number',
        'email_address',
        'created',
        'created_by',
        'rowcount',
        'total_price',
    ]

    row_labels = {
        'product_upc': "UPC",
        'product_brand': "Brand",
        'product_description': "Description",
        'product_size': "Size",
        'order_uom': "Order UOM",
    }

    row_grid_columns = [
        'sequence',
        'product_upc',
        'product_brand',
        'product_description',
        'product_size',
        'order_quantity',
        'order_uom',
        'total_price',
        'status_code',
    ]

    def configure_grid(self, g):
        super(CustomerOrderBatchView, self).configure_grid(g)

        g.set_type('total_price', 'currency')

        g.set_link('customer')
        g.set_link('created')
        g.set_link('created_by')

    def configure_form(self, f):
        super(CustomerOrderBatchView, self).configure_form(f)
        order = f.model_instance
        model = self.rattail_config.get_model()

        # readonly fields
        f.set_readonly('rows')
        f.set_readonly('status_code')

        # customer
        if 'customer' in f.fields and self.editing:
            f.replace('customer', 'customer_uuid')
            f.set_node('customer_uuid', colander.String(), missing=colander.null)
            customer_display = ""
            if self.request.method == 'POST':
                if self.request.POST.get('customer_uuid'):
                    customer = self.Session.query(model.Customer)\
                                           .get(self.request.POST['customer_uuid'])
                    if customer:
                        customer_display = six.text_type(customer)
            elif self.editing:
                customer_display = six.text_type(order.customer or "")
            customers_url = self.request.route_url('customers.autocomplete')
            f.set_widget('customer_uuid', forms.widgets.JQueryAutocompleteWidget(
                field_display=customer_display, service_url=customers_url))
            f.set_label('customer_uuid', "Customer")
        else:
            f.set_renderer('customer', self.render_customer)

        # person
        if 'person' in f.fields and self.editing:
            f.replace('person', 'person_uuid')
            f.set_node('person_uuid', colander.String(), missing=colander.null)
            person_display = ""
            if self.request.method == 'POST':
                if self.request.POST.get('person_uuid'):
                    person = self.Session.query(model.Person)\
                                         .get(self.request.POST['person_uuid'])
                    if person:
                        person_display = six.text_type(person)
            elif self.editing:
                person_display = six.text_type(order.person or "")
            people_url = self.request.route_url('people.autocomplete')
            f.set_widget('person_uuid', forms.widgets.JQueryAutocompleteWidget(
                field_display=person_display, service_url=people_url))
            f.set_label('person_uuid', "Person")
        else:
            f.set_renderer('person', self.render_person)

        f.set_type('total_price', 'currency')

    def row_grid_extra_class(self, row, i):
        if row.status_code == row.STATUS_PRODUCT_NOT_FOUND:
            return 'warning'

    def configure_row_grid(self, g):
        super(CustomerOrderBatchView, self).configure_row_grid(g)

        g.set_type('case_quantity', 'quantity')
        g.set_type('cases_ordered', 'quantity')
        g.set_type('units_ordered', 'quantity')
        g.set_type('order_quantity', 'quantity')
        g.set_enum('order_uom', self.enum.UNIT_OF_MEASURE)
        g.set_type('unit_price', 'currency')
        g.set_type('total_price', 'currency')

        g.set_link('product_upc')
        g.set_link('product_description')

    def configure_row_form(self, f):
        super(CustomerOrderBatchView, self).configure_row_form(f)

        f.set_renderer('product', self.render_product)

        f.set_type('case_quantity', 'quantity')
        f.set_type('cases_ordered', 'quantity')
        f.set_type('units_ordered', 'quantity')
        f.set_type('order_quantity', 'quantity')
        f.set_enum('order_uom', self.enum.UNIT_OF_MEASURE)
        f.set_type('unit_price', 'currency')
        f.set_type('total_price', 'currency')
