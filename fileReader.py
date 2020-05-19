import os
import pandas as pd

# Set the proper path
CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(CURRENT_PATH, '../data/')


country_record = pd.read_excel(
    os.path.join(DATA_PATH, 'ITC_EPM-Full_correspondences.xlsx'),
    sheetname='regions')


def get_country_name_by_iso(country_iso):
    k, v = 'iso', 'country_name'
    _pair = country_record[[k, v]].set_index(k)[v].to_dict()
    return _pair[int(country_iso)]


def get_iso_by_country_name(country_name='Taipei, Chinese'):
    k, v = 'country_name', 'iso'
    _pair = country_record[[k, v]].set_index(k)[v].to_dict()
    return str(_pair[str(country_name)]).zfill(3)


def read_import_side_tariff(product, country_iso):
    excel_name = '{}-{}-1.xlsx'.format(product, country_iso)
    excel_path = os.path.join(DATA_PATH, 'importer-view',
                              str(product)[:2], excel_name)
    df = pd.read_excel(excel_path, skiprows=4)
    df = df.iloc[:, [0, 1, 2]]
    df.columns = ['exporter', 'corres_num', 'tariff']
    df['tariff'] = df['tariff'].str.replace('%', '')\
                               .str.replace(',', '').astype(float) / 100
    df['importer'] = get_country_name_by_iso(country_iso)
    df['hscode6'] = str(product).zfill(6)
    return df


def read_export_side_tariff(_excel, product, country_iso):
    df = pd.read_excel(_excel, skiprows=4)
    df = df.iloc[:, [0, 1, 2, 3, 4, 7, 8]]
    df.columns = ['importer', 'year', 'revision', 'corres_num',
                  'tariff', 'export_value', 'source']

    # ensure values correct
    df['export_value'] = df['export_value'].astype(str)\
                                           .str.replace(',', '').astype(float)
    df['tariff'] = df['tariff'].str.replace('%', '')\
                               .str.replace(',', '').astype(float) / 100
    df['exporter'] = get_country_name_by_iso(country_iso)
    df['hscode6'] = str(product).zfill(6)
    return df


def normalize_tariff_df(df):
    return df.set_index(['importer', 'exporter', 'hscode6'])\
             .drop('export_value', axis=1)


def select_excels(files):
    return [f for f in files if '.xls' in f]


def get_exist_tariff_excels(target_folder):
    nested_excels = [select_excels(files) for path, folders, files
                     in os.walk(target_folder)]
    excels = sum(nested_excels, [])
    return excels


def get_exist_tariff_info(excels):
    rs_info = {}
    for excel in excels:
        country_iso = excel.split('-')[1]
        product = excel.split('-')[-1].split('.')[0]

        country_products = rs_info.get(country_iso, [])
        country_products.append(product)

        rs_info[country_iso] = sorted(set(country_products))

    return rs_info
