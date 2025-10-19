from odoo import fields, models, _
from odoo.exceptions import UserError
from markupsafe import Markup

class CrmLead(models.Model):
    _inherit = "crm.lead"

    sent_to_odoo = fields.Boolean(default=False)
    excel_sheet_url = fields.Char()

    def generate_odoo_table(self):
        self.ensure_one()
        if not self.partner_id or not self.main_contact_id:
            raise UserError("Please select a customer and a contact first !")
        content = self._generate_odoo_table()
        self.description = content + Markup("<br />") + (self.description or Markup(""))

    def _generate_odoo_table(self):
        self.ensure_one()
        header = """<table style="width: 931.5px;" class="table table-bordered"><tbody>"""
        footer = """</tbody></table>"""
        lines = [
            (_("Nom de l'entreprise"), lambda lead: lead.partner_id.name),
            (_("Adresse de l'entreprise"), lambda lead: lead._get_partner_formatted_address()),
            (_("Numéro de TVA"), lambda lead: lead.partner_id.vat or ""),
            (_("Secteur d'activité"), lambda lead: lead.partner_id.industry_id.name or ""),
            (_("Nombre d'employés"), lambda lead: ""),

            (_("Prénom/Nom du point de contact"), lambda lead: lead.main_contact_id.name),
            (_("Rôle"), lambda lead: lead.main_contact_id.function or ""),
            (_("Numéro de téléphone"), lambda lead: lead.main_contact_id.phone_sanitized or ""),
            (_("Adresse mail"), lambda lead: lead.main_contact_id.email or ""),
            (_("Liste noire (newsletter)"), lambda lead: _("Oui")),
        ]

        lines_html = ""
        for line_name, line_fn in lines:
            lines_html += f"""<tr style="height: 46px;"><td style="width: 265.5px;"><strong><span class="o_small-fs">{line_name}</span></strong></td><td style="width: 560px;">{line_fn(self)}</td></tr>"""

        return Markup(header + lines_html + footer)

    def _get_partner_formatted_address(self):
        self.ensure_one()
        str_res = ""
        if self.partner_id.street:
            str_res += self.partner_id.street
        if self.partner_id.street2:
            if str_res:
                str_res += " "
            str_res += self.partner_id.street2
        if str_res:
            str_res += ", "
        if self.partner_id.zip:
            str_res += self.partner_id.zip + " "
        if self.partner_id.city:
            str_res += self.partner_id.city
        return str_res


    def action_send_lead_declaration_mail(self):
        template = self.env.ref("klevia_crm_odoo.lead_declaration_mail_template", raise_if_not_found=False)
        if not template:
            raise UserError("Le modèle d'email 'klevia_crm_odoo.lead_declaration_mail_template' est introuvable.")

        for lead in self:
            template.with_context(mail_post_autofollow=True).send_mail(lead.id, force_send=True)
            lead.sent_to_odoo = True
            lead.message_post(
                body=f"Lead sent to Odoo !",
                message_type="comment",
                subtype_xmlid="mail.mt_note",
            )

        return True