import os.path

import requests
from bs4 import BeautifulSoup

import src.utils.shared as shared
from src.controller.data_controller import DataController
from dags.controllers.base_controller import BaseController
from dags.utils import (
    get_env,
    clean_path,
    create_dirs
)


class StartController(BaseController):

    def __init__(self):
        super().__init__()
        self.__base_url_anac = get_env('ANAC_RESOURCE')
        self.__work_path = ''
        self.__other_files_download = [
            '/siros/registros/aerodromo/aerodromos.csv',
            '/siros/registros/aeronave/aeronaves.csv',
            '/siros/registros/cia/cias.csv'
        ]

    def search_periods_anac(self):
        """
        Retorna os anos com dados de avião a serem baixados
        """
        try:
            result = []

            self.update_progress(f"Consultando dados site: '{self.__base_url_anac}'")
            response = requests.get(f'{self.__base_url_anac}/siros/registros/diversos/vra/')
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                links = [a['href'] for a in soup.find_all('a', href=True)]

                self.update_progress('Filtrando anos disponíveís')
                for link in links:
                    year = link.split('/')[-2]
                    if year.isnumeric():
                        result.append(year)

            self.update_progress(f'Encontrado períodos {result}')
            return result
        except Exception as error:
            self.raise_error(error)

    def download_data_anac(self, years: list):
        """
        Baixa os dados dos anos informados
        """
        try:
            self._set_work_path(f'{shared.path_data}\\downloaded')
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
            self._set_work_path(f'{shared.path_data}\\normalized')
            create_dirs(self.__work_path)
            clean_path(self.__work_path)

            others_files = [item.split('/')[-1] for item in self.__other_files_download]
            for file in os.listdir(f'{shared.path_data}\\downloaded'):
                self.update_progress(f'Normalizando arquivo {file}')

                if file.startswith('VRA_'):
                    DataController.normalize_flights_data(
                        f'{shared.path_data}\\downloaded\\{file}',
                        f'{shared.path_data}\\normalized\\flights.csv'
                    )
                elif file in others_files:
                    DataController.normalize_csv(
                        f'{shared.path_data}\\downloaded\\{file}',
                        path_new_csv=f'{shared.path_data}\\normalized\\{file}'
                    )

            self.update_progress(f'Processo finalizado!')
        except Exception as error:
            self.raise_error(error)

    def load_data(self):
        try:
            self._set_work_path(f'{shared.path_data}\\normalized')
            create_dirs(self.__work_path)
            clean_path(self.__work_path)

            self.update_progress(f'Processo finalizado!')
        except Exception as error:
            self.raise_error(error)

    def _download_file(self, link, name_file):
        self.update_progress(f'Baixando arquivo {name_file}')

        response = requests.get(link)
        if response.status_code == 200:
            with open(f'{self.__work_path}\\{name_file}', 'wb') as output_file:
                output_file.write(response.content)

        if not os.path.exists(f'{self.__work_path}\\{name_file}'):
            self.update_progress(f'Falha ao baixar arquivo {name_file}')
            return False
        else:
            return True

    def _set_work_path(self, path):
        self.__work_path = str(path)