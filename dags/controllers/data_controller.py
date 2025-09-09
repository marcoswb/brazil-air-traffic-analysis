import os
import requests
from bs4 import BeautifulSoup

from controllers.csv_controller import CSVController
from controllers.base_controller import BaseController
from utils.functions import (
    create_dirs,
    clean_path
)

class DataController(BaseController):

    def __init__(self):
        super().__init__()
        self.__base_url_anac = self.get_env('ANAC_RESOURCE')
        self.__base_path = self.get_env('BASE_PATH')
        self.__work_path = ''
        self.__other_files_download = [
            '/siros/registros/aerodromo/aerodromos.csv',
            '/siros/registros/aeronave/aeronaves.csv',
            '/siros/registros/cia/cias.csv'
        ]
        self.__float_columns = {
            'aerodromos.csv': ['latitude', 'longitude']
        }

    def download_data_anac(self):
        """
        Baixa os dados dos anos informados
        """
        try:
            years = self.get_env('YEARS_TO_DOWNLOAD', default_value='2025').split(',')
            self._set_work_path(f'{self.__base_path}/downloaded')
            create_dirs(self.__work_path)
            clean_path(self.__work_path)

            self.update_progress(f"Anos a baixar: {years}")

            downloaded_files = 0
            for year in years:
                self.update_progress(f"Consultando dados do ano de {year}")

                response = requests.get(f'{self.__base_url_anac}/siros/registros/diversos/vra/{year}')
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')

                    links = [a['href'] for a in soup.find_all('a', href=True)]
                    for link in links:
                        if not link.lower().endswith('.csv'):
                            continue

                        full_link = f'{self.__base_url_anac}{link}'
                        name_file = link.split('/')[-1]
                        if self._download_file(full_link, name_file):
                            downloaded_files += 1

            for link in self.__other_files_download:
                full_link = f'{self.__base_url_anac}{link}'
                name_file = link.split('/')[-1]
                if self._download_file(full_link, name_file):
                    downloaded_files += 1

            self.update_progress(f'Total de {downloaded_files} arquivos baixados!')
            self.update_progress(f'Processo finalizado!')
        except Exception as error:
            self.raise_error(error)

    def normalize_data(self):
        try:
            self._set_work_path(f'{self.__base_path}/normalized')
            create_dirs(self.__work_path)
            clean_path(self.__work_path)

            name_files = [item.split('/')[-1] for item in self.__other_files_download]
            for file in os.listdir(f'{self.__base_path}/downloaded'):
                self.update_progress(f'Normalizando arquivo {file}')

                if file.startswith('VRA_'):
                    CSVController.normalize_flights_data(
                        f'{self.__base_path}/downloaded/{file}',
                        f'{self.__base_path}/normalized/voos.csv'
                    )
                elif file in name_files:
                    dataframe = CSVController.normalize_csv(f'{self.__base_path}/downloaded/{file}')

                    float_columns = self.__float_columns.get(file)
                    if float_columns:
                        dataframe = CSVController.format_float_columns(dataframe, float_columns)

                    if file == 'aerodromos.csv':
                        dataframe = CSVController.replace_column_value(
                            dataframe,
                            'sigla_iata_aerodromo',
                            '...',
                            ''
                        )

                    CSVController.to_csv(dataframe, f'{self.__base_path}/normalized/{file}')

            self.update_progress(f'Processo finalizado!')
        except Exception as error:
            self.raise_error(error)

    def _download_file(self, link, name_file):
        self.update_progress(f'Baixando arquivo {name_file}')

        response = requests.get(link)
        if response.status_code == 200:
            with open(f'{self.__work_path}/{name_file}', 'wb') as output_file:
                output_file.write(response.content)

        if not os.path.exists(f'{self.__work_path}/{name_file}'):
            self.update_progress(f'Falha ao baixar arquivo {name_file}')
            return False
        else:
            return True

    def _set_work_path(self, path):
        self.__work_path = str(path)