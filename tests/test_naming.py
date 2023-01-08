from invoicing_tools.naming import rename_fiscal_invoice


def test_renaming(output_folder, envs_folder, database):
    data_folder = output_folder / 'invoices_to_process'
    renamed_folder = data_folder / 'renamed'
    source_file = data_folder / 'Fact06_20220306-1143.pdf'
    number = "6"
    invoice = database.get_invoices(number)
    rename_fiscal_invoice(invoice, database, source_file, renamed_folder)

