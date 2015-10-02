# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import api, fields, models, _


class PurchaseRequisition(models.Model):
    _inherit = "purchase.requisition"

    @api.model
    def _purchase_request_confirm_message_content(
        self, pr, request, request_dict
    ):
        if not request_dict:
            request_dict = {}
        title = _('Bid confirmation %s for your Request %s') % (
            pr.name, request.name
        )
        message = '<h3>%s</h3><ul>' % title
        message += _('The following requested items from Purchase Request %s '
                     'have now being sent to Suppliers using Purchase Bid '
                     '%s:') % (
            request.name, pr.name
        )

        for line in request_dict.values():
            message += _(
                '<li><b>%s</b>: Total bid quantity %s %s</li>'
            ) % (line['name'],
                 line['product_qty'],
                 line['product_uom_id'],
                 )
        message += '</ul>'
        return message

    @api.multi
    def _purchase_request_confirm_message(self):
        request_obj = self.env['purchase.request']
        for pr in self:
            requests_dict = {}
            for line in pr.line_ids:
                for request_line in line.purchase_request_lines:
                    request_id = request_line.request_id.id
                    if request_id not in requests_dict:
                        requests_dict[request_id] = {}
                    data = {
                        'name': request_line.name,
                        'product_qty': line.product_qty,
                        'product_uom_id': line.product_uom_id.name,
                    }
                    requests_dict[request_id][request_line.id] = data
            for request_id in requests_dict.keys():
                request = request_obj.browse(request_id)
                message = self._purchase_request_confirm_message_content(
                    pr, request, requests_dict[request_id])
                request.message_post(body=message)
        return True

    @api.multi
    def tender_in_progress(self):
        res = super(PurchaseRequisition, self).tender_in_progress()
        self._purchase_request_confirm_message()
        return res

    @api.model
    def _prepare_purchase_order_line(
        self, requisition, requisition_line,
        purchase_id, supplier
    ):
        vals = super(PurchaseRequisition, self)._prepare_purchase_order_line(
            requisition, requisition_line, purchase_id, supplier
        )
        vals.update(
            {
                'purchase_request_lines':
                [
                    (4, line.id) for line
                    in requisition_line.purchase_request_lines
                ],
            }
        )
        return vals


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    @api.one
    def _has_purchase_request_lines(self):
        if self.purchase_request_lines:
            self.has_purchase_request_lines = True
        else:
            self.has_purchase_request_lines = False

    purchase_request_lines = fields.Many2many(
        'purchase.request.line',
        'purchase_request_purchase_requisition_line_rel',
        'purchase_requisition_line_id',
        'purchase_request_line_id',
        string='Purchase Request Lines', readonly=True
    )
    has_purchase_request_lines = fields.Boolean(
        compute="_has_purchase_request_lines",
        string="Has Purchase Request Lines"
    )

    @api.one
    def copy(self, default=None):
        if default is None:
            default = {}
        default.update({
            'purchase_request_lines': [],
        })
        return super(PurchaseRequisitionLine, self).copy(default)

    @api.multi
    def action_openRequestLineTreeView(self):
        """
        :return dict: dictionary value for created view
        """
        request_line_ids = []
        for line in self:
            request_line_ids = [
                request_line.id for request_line
                in line.purchase_request_lines
            ]
        domain = [('id', 'in', request_line_ids)]

        return {'name': _('Purchase Request Lines'),
                'type': 'ir.actions.act_window',
                'res_model': 'purchase.request.line',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'domain': domain}
