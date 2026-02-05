from odoo import models, fields, api, _
from math import ceil



class DbmRequest(models.Model):
    _inherit = "dbm.request"

    request_type = fields.Selection(
        selection_add=[("dev", "Development")],
        ondelete={"dev": "cascade"},
        default='dev',
    )

    line_ids = fields.One2many(
        "dbm.request.line",
        "request_id",
        string="Development Lines",
    )
    model_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'model')])
    logic_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'logic')])
    view_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'view')])
    security_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'security')])
    report_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'report')])
    owl_line_ids = fields.One2many("dbm.request.line", "request_id", copy=False, domain=[('line_type', '=', 'owl')])

    # Totaux par catégorie
    time_model = fields.Float(compute="_compute_times", store=False)
    time_logic = fields.Float(compute="_compute_times", store=False)
    time_view = fields.Float(compute="_compute_times", store=False)
    time_security = fields.Float(compute="_compute_times", store=False)
    time_report = fields.Float(compute="_compute_times", store=False)
    time_owl = fields.Float(compute="_compute_times", store=False)
    time_total = fields.Float(
        string="Total Estimated Time",
        compute="_compute_totals",
        store=True,
    )
    time_min = fields.Float(
        string="Estimated Min Time",
        compute="_compute_totals",
        store=True,
    )
    time_max = fields.Float(
        string="Estimated Max Time",
        compute="_compute_totals",
        store=True,
    )
    maintenance_loc_min = fields.Integer(
        string="Min LoC Maintenance",
        compute="_compute_totals",
        store=True,
    )
    maintenance_loc_max = fields.Integer(
        string="Max LoC Maintenance",
        compute="_compute_totals",
        store=True,
    )

    reliability = fields.Float(
        string="Reliability",
        default=0.9,
        help="Confidence factor (e.g. 0.9 = ±10%)",
    )

    estimation_report_html = fields.Html(
        string="Estimation Summary",
        compute="_compute_estimation_report",
        sanitize=False,
    )


    @api.depends("line_ids.time_estimated", "line_ids.line_type")
    def _compute_times(self):
        for request in self:
            totals = {
                "model": 0.0,
                "logic": 0.0,
                "view": 0.0,
                "security": 0.0,
                "report": 0.0,
                "owl": 0.0,
            }
            for line in request.line_ids:
                totals[line.line_type] += line.time_estimated

            request.time_model = totals["model"]
            request.time_logic = totals["logic"]
            request.time_view = totals["view"]
            request.time_security = totals["security"]
            request.time_report = totals["report"]
            request.time_owl = totals["owl"]



    @api.depends("line_ids.time_estimated", "reliability")
    def _compute_totals(self):
        for rec in self:
            total = sum(rec.line_ids.mapped("time_estimated"))
            reliability = rec.reliability or 1.0

            # écart (ex: 0.9 => 10%)
            delta = total * (1 - reliability)

            # arrondi à la demi-heure
            def round_half_hour(value):
                return round(value * 2) / 2

            rec.time_total = round_half_hour(total)
            rec.time_min = round_half_hour(max(total - delta, 0))
            rec.time_max = round_half_hour(total + delta)

            # maintenance : 20 LoC / heure
            rec.maintenance_loc_min = int(round(rec.time_min * 20))
            rec.maintenance_loc_max = int(ceil(rec.time_max * 20))

    @api.depends(
        "time_total",
        "time_min",
        "time_max",
        "reliability",
        "maintenance_loc_min",
        "maintenance_loc_max",
        "line_ids.time_estimated",
    )
    def _compute_estimation_report(self):
        TYPE_LABELS = {
            "model": _("Data Model"),
            "logic": _("Business Logic"),
            "view": _("Views"),
            "security": _("Security"),
            "report": _("Reports"),
            "owl": _("OWL / JS"),
        }

        for rec in self:
            lines_by_type = {}
            for line in rec.line_ids:
                lines_by_type.setdefault(line.line_type, 0.0)
                lines_by_type[line.line_type] += line.time_estimated or 0.0

            rows_html = ""
            for line_type, label in TYPE_LABELS.items():
                hours = lines_by_type.get(line_type, 0.0)
                if not hours:
                    continue
                rows_html += f"""
                    <tr>
                        <td>{label}</td>
                        <td align="right">{hours:.1f} h</td>
                    </tr>
                """

            reliability_pct = int((rec.reliability or 0) * 100)
            rec.estimation_report_html = f"""
            <div style="max-width:800px;">
                <h3>Development Estimation Summary</h3>
                <div><strong>Name: </strong>{rec.name}</div>
                <table style="width:100%; border-collapse:collapse; margin-top:5px;" border="1" cellpadding="8">

                    {rows_html}

                    <tr style="border-top: 1px solid black;">
                        <td>Total Estimated Time</td>
                        <td align="right">~{rec.time_total:.1f} h</td>
                    </tr>
                    <tr>
                        <td>Reliability</td>
                        <td align="right">{reliability_pct} %</td>
                    </tr>
                    <tr>
                        <td><strong>Estimated Range</strong></td>
                        <td align="right"><strong>{rec.time_min:.1f} h – {rec.time_max:.1f} h</strong></td>
                    </tr>
                    <tr>
                        <td>Estimated Maintenance</td>
                        <td align="right">{rec.maintenance_loc_min}-{rec.maintenance_loc_max} LoC</td>
                    </tr>

                </table>
            </div>
            """

