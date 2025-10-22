import pandas as pd
import csv
import warnings
import os
import copy
from pprint import pprint as pp

warnings.simplefilter(action='ignore', category=UserWarning)

from ChartOfAccounts import ChartOfAccounts, _is_truthy

FILE_BASE = '/Users/gautier/Library/CloudStorage/OneDrive-OneSolutions/Offering Odoo/Projets/Genecand/CIPE PC export Odoo.xlsx'
FILE_TARGET = '/Users/gautier/Library/CloudStorage/OneDrive-OneSolutions/Offering Odoo/Projets/Genecand/REMPLI Genecand - Plan comptable.xlsx'
COMPANY_NAME = 'CIPE - Centre Industriel Praille-Etoile'
SHEET_NAME = "CIPE"



DUPLICATA_LIST = [
    # ('AVEAS', 2, 'Association Vaudoise des Employés en Assurances Sociales AVEAS'),
    # ('Cuisine', 3, 'Cuisine Suisse'),
    # ('Lamy', 4, 'Lamy Formation Sàrl'),
]



# ------------------------------------------------------------------------------------------

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





odoo_export_coa = ChartOfAccounts(excel_file=FILE_BASE)

# Read the target Excel with proper typing
dtype_additional = {}
for k, v in TARGET_COLUMNS_MAPPING.items():
    if k in COLUMNS_DTYPE:
        dtype_additional[_t(k)] = COLUMNS_DTYPE[k]
final_dtype = COLUMNS_DTYPE | dtype_additional
target_df = pd.read_excel(FILE_TARGET, dtype=final_dtype, sheet_name=SHEET_NAME)




accounts_to_keep_list = list(target_df[_t('code')].unique()) + ACCOUNTS_TO_CHECK


for index, row in target_df.iterrows():
    code = row[_t('code')]
    name = row[_t('name')]
    account_type = row[_t('account_type')]
    reconcile = True if account_type in FORCE_RECONCILE_TYPES else _is_truthy(row[_t('reconcile')])
    currency_id = '' if not _is_truthy(row[_t('currency_id')], accept_range_extended=True) else row[_t('currency_id')] # TO CHANGE OMG extended de merde


    if code in odoo_export_coa:
        account = odoo_export_coa[code]
        if code in ACCOUNTS_TO_CHECK and (name != account.name or account_type != account.account_type):
            account.print_difference(code=code, name=name, account_type=account_type, reconcile=reconcile, currency_id=currency_id)
            if input(f"Update account {code} data ? (Y/n) : ") == 'Y':
                account.name = name
                account.account_type = account_type
                account.reconcile = reconcile
                account.currency_id = currency_id
            else:
                exception_code = code + ".EXCEPTION"
                odoo_export_coa.create_account(exception_code, name, account_type, reconcile=reconcile, currency_id=currency_id)
                accounts_to_keep_list.append(exception_code)
        else:
            account.name = name
            account.account_type = account_type
            account.reconcile = reconcile
            account.currency_id = currency_id

    else:
        odoo_export_coa.create_account(code, name, account_type, reconcile=reconcile, currency_id=currency_id)


print("=====================================================")

odoo_export_coa.order_coa()
odoo_export_coa.print_table()

print("=====================================================")


# Ask for special accounts :
for xml_id in XML_IDS_TO_SETUP:
    current_account = odoo_export_coa.search_by_xml_id(xml_id, strict=False)
    print("XML ID : ", xml_id, " - Current account: ", current_account)
    new_account = input("Choose an account code or leave empty to keep current account : ")
    if new_account:
        odoo_export_coa[new_account].id = current_account[0].id
        current_account[0].id = ""
        deprecate_old_accounts = input(f"Deprecate old accounts ? (Y/n) : ") == 'Y'
        # Might be several account but VERY WEIRD, loop just in case instead of taking index 0
        for account in current_account:
            account.id = ""
            account.deprecated = deprecate_old_accounts
        accounts_to_keep_list.append(new_account)

print("=====================================================")

# Deprecate useless accounts
accounts_to_keep_list = set(accounts_to_keep_list)
for code, account in odoo_export_coa.items():
    if code not in accounts_to_keep_list:
        account.deprecated = True


print("============== FINAL COA TO IMPORT =============")

odoo_export_coa.order_coa()
odoo_export_coa.print_table()
odoo_export_coa.export_to_excel()
print("=====================================================")




coa_list = [odoo_export_coa]

# if DUPLICATA_LIST:
#     print("--- DUPLICATA FOUND : ")
#     pp(DUPLICATA_LIST)
#     if input(f"Use these data ? (Y/n) : ") == 'Y':
#         pass
#     else:
#         DUPLICATA_LIST = []
#         duplicata_qty = input("How many duplicata ? : ")
#         if duplicata_qty:
#             for i in range(int(duplicata_qty)):
#                 print("\n--- Duplicata N°", i+1)
#                 coa_name = input(f"Name : ")
#                 company_ids = int(input(f"Company ID (suggested id: {i+2}): ") or (i+2))
#                 company_name = input(f"Company Name : ")
#
#                 DUPLICATA_LIST.append((coa_name, company_ids, company_name))
#
#
# for (coa_name, company_ids, company_name) in DUPLICATA_LIST:
#     # Create a deep copy of the odoo_export_coa and change values
#     odoo_export_coa_duplicata = copy.deepcopy(odoo_export_coa)
#     odoo_export_coa_duplicata.name = coa_name
#     odoo_export_coa_duplicata.update_company(company_ids)
#     odoo_export_coa_duplicata.company_name = company_name
#
#     coa_list.append(odoo_export_coa_duplicata)
#     # odoo_export_coa_duplicata.order_coa()
#     # odoo_export_coa_duplicata.print_table()


for coa in coa_list:
    coa.export_to_excel()

