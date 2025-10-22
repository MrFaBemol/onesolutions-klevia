import pandas as pd


def _is_truthy(value, accept_range_extended=False):
    accepted_value = bool(value) if accept_range_extended else str(value).lower() in ['true', '1', 'vrai']
    return not (pd.isna(value) or pd.isnull(value) or not accepted_value)




class ChartOfAccounts(dict):
    _required_columns = ['id', 'name', 'code', 'account_type', 'reconcile']     # deprecated
    _print_columns_data = [
        ("Code", "code", 15),
        ("Name", "name", 80),
        ("Account Type", "account_type", 24),
        ("Reconcile", "reconcile", 12),
        ("Deprecated", "deprecated", 12),
        ("Company", "company_ids", 12),
        ("Currency", "currency_id", 12),
        ("XMLID", "id", 60),
    ]
    _columns_mapping = {}
    _dtype_arg_default = {'code': str, 'reconcile': str, 'deprecated': str, 'id': str}
    _default_name = "My Chart of Accounts"

    def __init__(self, company_name, excel_file=None, dataframe=None, name=None):
        super().__init__()

        self._dtype_arg = self._dtype_arg_default       # Todo: either delete or implement it someday

        self.company_name = company_name

        if excel_file is not None:
            dataframe = pd.read_excel(excel_file, dtype=self._dtype_arg)
            self.working_directory = "/".join(excel_file.split("/")[:-1])


        if dataframe is not None:
            if not self._check_df(dataframe):
                raise ValueError('The dataframe does not have the required columns')
            self.df = dataframe
            self.name = name or self._get_name() or self.company_name
            self.company_ids = self._get_company_ids()
            self._load_accounts()
        else:
            self.name = name or self._default_name


    def __missing__(self, key):
        raise Exception

    def _check_df(self, df):
        # Check if the dataframe has the required columns
        return all(col in df.columns for col in self._required_columns)

    def _get_name(self):
        if 'company_ids' not in self.df.columns:
            return None
        value_counts = self.df['company_ids'].value_counts()
        return None if value_counts.empty else value_counts.idxmax()

    def _get_company_ids(self):
        return int(self.df[pd.notna(self.df['id']) & self.df['id'].str.startswith('account.')].head(1)['id'].iloc[0].split(".")[1].split("_")[0])


    def _load_accounts(self):
        for index, row in self.df.iterrows():
            self.create_account(
                row['code'],
                row['name'],
                row['account_type'],
                company_ids=self.company_ids,
                reconcile=_is_truthy(row['reconcile']),
                # deprecated=_is_truthy(row['deprecated']),     # Maybe uncomment someday this line if we want deprecated to be a mandatory column
                xml_id=row['id'] if not (pd.isna(row['id']) or pd.isnull(row['id'])) else None,
                # currency_id=row['currency_id'],
            )

    def order_coa(self, reverse=False):
        # Order self by key alphabetically
        sorted_accounts = dict(sorted(self.items(), reverse=reverse))
        self.clear()
        self.update(sorted_accounts)

    def print_headers(self):
        columns = [
            thead.ljust(length)
            for thead, dummy, length in self._print_columns_data
        ]
        print(''.join(columns))


    def print_table(self):
        self.print_headers()
        for account in self:
            print(self[account].to_table_row())

    def create_account(self, code, name, account_type, company_ids=None, reconcile=False, deprecated=False, xml_id=None, currency_id=None):
        if code in self:
            raise ValueError('The code already exists: ', code)
        if xml_id:
            existing_xml_ids = self.search_by_xml_id(xml_id)
            if existing_xml_ids:
                raise ValueError('This xml_id already exists: ', xml_id, existing_xml_ids)
        company_ids = company_ids or self.company_ids
        self[code] = Account(self, code, name, account_type, company_ids, reconcile, deprecated, xml_id, currency_id)

    def search_by_xml_id(self, xml_id, strict=True):
        res = []
        if not xml_id:
            return res
        for account in self.values():
            if not account.id:
                continue
            if (strict and account.id == xml_id) or (not strict and xml_id in account.id):
                res.append(account)
        return res

    def update_company(self, new_company_ids, update_all_accounts=True):
        self.company_ids = new_company_ids
        if update_all_accounts:
            for account in self.values():
                account.update_company(new_company_ids)


    def get_dataframe(self):
        self.order_coa()
        # Prepare data for DataFrame creation
        columns = ['id', 'code', 'name', 'account_type', 'company_ids', 'reconcile', 'deprecated', 'currency_id']
        data = [
            [
                account.id,
                account.code,
                account.name,
                account.account_type,
                # account.company_ids,
                self.company_name,                    # Particular case, with a unique patch to put name instead of company ID.
                1 if account.reconcile else 0,
                1 if account.deprecated else 0,
                account.currency_id or "",
                ]
            for account in self.values()
        ]

        # Create DataFrame
        df = pd.DataFrame(data, columns=columns)

        # Apply a style to DataFrame to highlight rows with a light red background where 'deprecated' is 0
        def highlight_row(row):
            return ['background-color: lightcoral' if row['deprecated'] == 1 else '' for _ in row]
        styled_df = df.style.apply(highlight_row, axis=1)

        return styled_df


    def export_to_excel(self):
        df = self.get_dataframe()

        # Construct the filename using the company_ids and name
        filename = f"COA export - {self.company_ids} {self.name}.xlsx"
        full_path = self.working_directory + "/" + filename

        # Save the DataFrame to an Excel file
        df.to_excel(full_path, index=False)
        print(f"Exported Excel to {full_path}")




# ------------------------------------------------------------

class Account:
    def __init__(self, coa, code, name, account_type, company_ids, reconcile, deprecated, xml_id, currency_id=None):
        self.coa = coa
        self.code = code
        self.name = name
        self.account_type = account_type.strip()
        # Gros patch pourri
        if 'crédit' in self.account_type:
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