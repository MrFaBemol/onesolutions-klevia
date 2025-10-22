import pandas as pd

def _is_truthy(value, accept_range_extended=False):
    accepted_value = bool(value) if accept_range_extended else str(value).lower() in ['true', '1', 'vrai']
    return not (pd.isna(value) or pd.isnull(value) or not accepted_value)


class ChartOfAccounts(dict):
    """
    Classe générique pour gérer un plan comptable provenant d'Odoo ou d'un fichier client.
    Permet de normaliser la structure des colonnes et manipuler les comptes de manière homogène.
    """
    _required_columns_odoo = ['id', 'name', 'code', 'account_type', 'reconcile']
    _required_columns_client = ['Code', 'Nom du compte', 'Type']
    _dtype_arg_default = {'code': str, 'reconcile': str, 'deprecated': str, 'id': str, 'Code': str}


    def __init__(self, excel_file=None, file_type=None, sheet_name=0, dataframe=None, name=None):
        super().__init__()
        self.df = None
        self.company_name = ""
        self.is_odoo_export = False
        self.name = name or "Chart of Accounts"
        self.file_type = file_type or "odoo"
        self._dtype_arg = self._dtype_arg_default


        if excel_file is not None:
            self.df = pd.read_excel(excel_file, dtype=self._dtype_arg, sheet_name=sheet_name)
        elif dataframe is not None:
            self.df = dataframe
        else:
            raise ValueError("Aucun fichier ou DataFrame fourni.")

        # Identifier le format du fichier
        self.is_odoo_export = self._detect_odoo_format(self.df)
        self.df = self._normalize_dataframe(self.df)
        # if self.file_type == 'odoo':
        #     self.company_ids = self._get_company_ids()

        # Charger les comptes
        self._load_accounts()

    # ------------------------------------------------------------------

    def _detect_odoo_format(self, df):
        """Détermine si le fichier vient d’un export Odoo ou d’un modèle client"""
        return all(col in df.columns for col in self._required_columns_odoo)

    @staticmethod
    def _get_column_mapping(to_technical=True):
        mapping = {
            "Code": "code",
            "Nom du compte": "name",
            "Type": "account_type",
            "Autoriser le lettrage": "reconcile",
            "Devise": "currency_id",
        }
        return mapping if to_technical else {v: k for k, v in mapping.items()}

    def _get_company_ids(self):
        return int(self.df[pd.notna(self.df['id']) & self.df['id'].str.startswith('account.')].head(1)['id'].iloc[0].split(".")[1].split("_")[0])

    def _normalize_dataframe(self, df):
        """
        Harmonise les colonnes du DataFrame pour avoir une structure uniforme
        quelle que soit la source du fichier.
        """
        if self.is_odoo_export:
            # Déjà formaté pour Odoo
            df = df.rename(columns=str.lower)
            return df

        # Format client → on renomme les colonnes
        column_mapping = self._get_column_mapping()

        for fr, std in column_mapping.items():
            if fr in df.columns:
                df.rename(columns={fr: std}, inplace=True)

        # Ajouter les colonnes manquantes
        for col in ['id', 'deprecated', 'company_ids']:
            if col not in df.columns:
                df[col] = ""

        for col, typ in self._dtype_arg.items():
            if col in df.columns:
                df[col] = df[col].astype(typ)

        return df

    # ------------------------------------------------------------------

    def _load_accounts(self):
        """Instancie les comptes à partir du DataFrame normalisé"""
        for _, row in self.df.iterrows():
            print(row.get('code'))
            self.create_account(
                row.get('code'),
                row.get('name'),
                row.get('account_type', ''),
                reconcile=_is_truthy(row.get('reconcile', False)),
                deprecated=_is_truthy(row.get('deprecated', False)),
                xml_id=row.get('id', ''),
                currency_id=row.get('currency_id', '') if _is_truthy(row.get('currency_id', ''), accept_range_extended=True) else False,
                company_ids=row.get('company_ids', ''),
            )

    # ------------------------------------------------------------------

    def create_account(self, code, name, account_type, company_ids=None, reconcile=False, deprecated=False, xml_id=None, currency_id=None):
        if not code:
            return
        self[code] = Account(
            self, code, name, account_type,
            company_ids, reconcile, deprecated, xml_id, currency_id
        )

    # ------------------------------------------------------------------

    def export_to_excel(self, path=None, name_prefix="COA export"):
        """Exporte le plan de comptes au format Excel"""
        df = self.get_dataframe()
        filename = f"{name_prefix}.xlsx"
        if path:
            df.to_excel(path + "/" + filename, index=False)
        else:
            df.to_excel(filename, index=False)
        return filename

    # ------------------------------------------------------------------

    def get_dataframe(self):
        """Retourne le DataFrame des comptes"""
        data = [
            {
                'code': a.code,
                'name': a.name,
                'account_type': a.account_type,
                'reconcile': a.reconcile,
                'deprecated': a.deprecated,
                'currency_id': a.currency_id,
                'xml_id': a.id,
            }
            for a in self.values()
        ]
        return pd.DataFrame(data)


# ------------------------------------------------------------

class Account:
    def __init__(self, coa, code, name, account_type, company_ids, reconcile, deprecated, xml_id, currency_id=None):
        self.coa = coa
        self.code = code
        self.name = name
        self.account_type = account_type.strip()
        # Gros patch pourri
        if 'crédit' in self.account_type or 'credit' in self.account_type:
            self.account_type = 'liability_credit_card'
        self.company_ids = company_ids

        if self.account_type in ['Banque et espèces', 'liability_credit_card', 'Hors bilan']:
            self.reconcile = False
        elif self.account_type in ['Client', 'Fournisseur']:
            self.reconcile = True
        else:
            self.reconcile = reconcile

        self.deprecated = deprecated
        self.id = xml_id or ""
        self.currency_id = currency_id or ""

    def __repr__(self):
        return f"Account({self.code} - {self.name} - {self.account_type})"


    def to_table_row(self):
        columns = []
        for (dummy, field, length) in self.coa._print_columns_data:
            str_value = str(getattr(self, field))
            str_res = str_value if len(str_value) < length else str_value[:length-3] + "..."
            columns.append(str_res.ljust(length))

        return ''.join(columns)

    def print_difference(self, **kwargs):
        columns = []
        for (dummy, field, length) in self.coa._print_columns_data:
            str_value = str(kwargs.get(field)) if field in kwargs else ""
            str_res = str_value if len(str_value) < length else str_value[:length - 3] + "..."
            columns.append(str_res.ljust(length))
        self.coa.print_headers()
        print(self.to_table_row())
        print(''.join(columns))


    def update_company(self, new_company_id):
        if self.id:
            self.id = self.id.replace(f"account.{self.company_ids}_", f"account.{new_company_id}_")
        self.company_ids = new_company_id


