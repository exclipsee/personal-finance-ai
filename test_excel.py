import excel

if __name__ == '__main__':
    print('Exporting transactions to export.xlsx...')
    excel.export_xlsx('export.xlsx', db_path='lite.db')
    print('Export complete.')
    print('Importing export.xlsx into lite_test.db...')
    n = excel.import_xlsx('export.xlsx', db_path='lite_test.db')
    print(f'Imported {n} rows into lite_test.db')
    print('Done')
