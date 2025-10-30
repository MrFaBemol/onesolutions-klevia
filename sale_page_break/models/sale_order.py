from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def group_lines_for_page_break(self):
        grouped = []
        group = []

        for line in self.order_line:
            group.append(line)

            if getattr(line, 'add_page_break_after', False):
                grouped.append(group)
                group = []

        if group:
            grouped.append(group)

        return grouped
