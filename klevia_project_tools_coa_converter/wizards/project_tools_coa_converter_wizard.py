from odoo import fields, models, _
from odoo.exceptions import UserError
from odoo.addons.klevia_project_tools_coa_converter.tools.ChartOfAccounts import ChartOfAccounts

import base64
import pandas as pd
from io import BytesIO

import logging
_logger = logging.getLogger(__name__)


ACCOUNTS_TO_CHECK = [
    '1090',
    '1100',
    '1170',
    '1171',
    '1176',
    '2000',
    '2200',
    '2201',
    '3200',
    '4200',
    '4991',
    '4992',
    '5000',
    '999999',
]
XML_IDS_TO_SETUP = [
    'account_journal_suspense_account_id',
    'cash_journal_default_account',
    'bank_journal_default_account',
    'transfer_account_id'
]
COLUMNS_DTYPE = {
    'code': str,
    'reconcile': str,
    'currency_id': str,
}
TARGET_COLUMNS_MAPPING = {
    'code': "Code",
    'name': "Nom du compte",
    'account_type': "Type",
    'reconcile': "Autoriser le lettrage",
    'currency_id': "Devise",
}

FORCE_RECONCILE_TYPES = [
    'Client',
    'Fournisseur',
]

def _t(c):
    return TARGET_COLUMNS_MAPPING.get(c)


class ProjectToolsCoaConverterWizard(models.TransientModel):
    _name = "project.tools.coa.converter.wizard"
    _description = "project.tools.coa.converter.wizard"

    state = fields.Selection(
        selection=[
            ('0', 'Upload'),
            ('1', 'Accounts List'),
            ('2', 'Special Accounts'),
            ('3', 'Done'),
        ],
        default='0',
    )
    file_from = fields.Binary(required=False)
    file_from_name = fields.Char()
    file_to = fields.Binary(required=False)
    file_to_name = fields.Char()


    line_ids = fields.One2many("project.tools.coa.converter.wizard.line.account", "wizard_id")
    active_line_ids = fields.One2many(  # /!\ invoice_line_ids is just a subset of line_ids.
        'project.tools.coa.converter.wizard.line.account',
        'wizard_id',
        string='Active lines',
        copy=False,
        domain=[('deprecated', '!=', True)],
    )
    show_all_lines = fields.Boolean()


    file_result = fields.Binary(required=False, readonly=True,)
    file_result_name = fields.Char()

    def action_upload_files(self):
        """Lit les deux fichiers et prépare la fusion"""
        if not self.file_from or not self.file_to:
            raise UserError(_("Veuillez charger les deux fichiers Excel."))

        try:
            coa_odoo = self._load_chart(self.file_from, file_type="odoo")
            coa_client = self._load_chart(self.file_to, file_type="client", sheet_name='Plan Comptable')

            _logger.info(f"📘 Chargé {len(coa_odoo)} comptes depuis Odoo.")
            _logger.info(f"📗 Chargé {len(coa_client)} comptes depuis le client.")

            self._prepare_accounts(coa_odoo, coa_client)
            self.state = '1'
            return self.action_close_and_reopen()


        except Exception as e:
            _logger.error(f"Erreur lors de l'import des fichiers COA : {e}")
            raise UserError(str(e))



    def action_validate_accounts(self):
        """Génère le fichier Excel final au format Odoo."""
        if not self.line_ids:
            raise UserError(_("Aucune ligne à exporter."))

        # Préparer les données pour le DataFrame
        data = []
        for line in self.line_ids:
            data.append({
                'id': line.xml_id or '',
                'name': line.name or '',
                'code': line.code or '',
                'account_type': line.account_type or '',
                'currency_id': line.currency_id or '',
                'reconcile': 1 if line.reconcile else  0,
                'deprecated': 1 if line.deprecated else 0,
            })

        # DataFrame avec colonnes EXACTES de Odoo
        df = pd.DataFrame(data, columns=[
            'id', 'name', 'code', 'account_type', 'currency_id', 'reconcile', 'deprecated'
        ])

        def highlight_row(row):
            return ['background-color: lightcoral' if row['deprecated'] == 1 else '' for _ in row]
        try:
            df = df.style.apply(highlight_row, axis=1)
        except:
            pass

        # Export Excel en mémoire
        output = BytesIO()
        df.to_excel(output, index=False, sheet_name="chart_of_accounts")
        output.seek(0)
        file_data = output.read()
        output.close()

        # Sauvegarde dans le wizard
        self.file_result = base64.b64encode(file_data)
        self.file_result_name = "converted_chart_of_accounts.xlsx"

        # Aller directement à l'étape 3 (Done)
        self.state = '3'
        return self.action_close_and_reopen()

    def _load_chart(self, binary_data, file_type=None, sheet_name=None):
        """Charge un fichier Excel Odoo ou client dans ChartOfAccounts"""
        file_content = base64.b64decode(binary_data)
        file_stream = BytesIO(file_content)
        return ChartOfAccounts(excel_file=file_stream, file_type=file_type, sheet_name=sheet_name or 0)




    def _prepare_accounts(self, coa_odoo, coa_client):
        self.line_ids.unlink()
        odoo_codes = set(coa_odoo.keys())
        client_codes = set(coa_client.keys())
        all_codes = sorted(odoo_codes | client_codes)

        line_vals_list = []
        for code in all_codes:
            od = coa_odoo.get(code)
            cl = coa_client.get(code)

            vals = {
                'wizard_id': self.id,
                'xml_id': od.id if od else False,
                'code': code,
                'name': cl.name if cl else (od.name if od else ""),
                'old_name': od.name if od else False,
                'account_type': cl.account_type if cl else (od.account_type if od else ""),
                'currency_id': cl.currency_id if cl else (od.currency_id if od else ""),
                'reconcile': cl.reconcile if cl else (od.reconcile if od else False),
                'deprecated': bool(od and not cl),
                'in_odoo': bool(od),
                'in_client': bool(cl),
            }
            if vals['name'] in FORCE_RECONCILE_TYPES:
                vals['reconcile'] = True

            line_vals_list.append(vals)

        self.env['project.tools.coa.converter.wizard.line.account'].create(line_vals_list)



    def action_close_and_reopen(self):
        return {
            "name": _("Chart of accounts converter"),
            "type": 'ir.actions.act_window',
            "res_model": 'project.tools.coa.converter.wizard',
            'res_id': self.id,
            "views": [[False, "form"]],
            "target": 'new',
            "context": {
                **self.env.context,
            },
        }


class ProjectToolsCoaConverterLineAccount(models.TransientModel):
    _name = "project.tools.coa.converter.wizard.line.account"
    _description = "COA Preview Line"

    _code_uniq = models.Constraint(
        'unique (code, wizard_id)',
        "Two accounts can't share the same code !",
    )

    wizard_id = fields.Many2one("project.tools.coa.converter.wizard", required=True, ondelete="cascade")

    xml_id = fields.Char(readonly=True)
    code = fields.Char()
    name = fields.Char()
    old_name = fields.Char(readonly=True)
    account_type = fields.Char()
    currency_id = fields.Char()
    reconcile = fields.Boolean()
    deprecated = fields.Boolean()

    # Flags
    in_odoo = fields.Boolean(readonly=True)
    in_client = fields.Boolean(readonly=True)