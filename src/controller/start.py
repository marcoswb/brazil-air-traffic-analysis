import os.path

import requests
from bs4 import BeautifulSoup

import src.utils.shared as shared
from src.controller.base_controller import BaseController
from src.utils.functions import (
    get_env,
    clean_path
)


class StartController(BaseController):

    def __init__(self):
        super().__init__()
        self.__base_url_anac = get_env('ANAC_RESOURCE')

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
            self.update_progress(f"Anos a baixar: {years}")
            clean_path(shared.path_data)

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

            self.update_progress(f'Total de {downloaded_files} arquivos baixados!')
        except Exception as error:
            self.raise_error(error)

    def _download_file(self, link, name_file):
        self.update_progress(f'Baixando arquivo {name_file}')

        response = requests.get(link)
        if response.status_code == 200:
            with open(f'{shared.path_data}\\{name_file}', 'wb') as output_file:
                output_file.write(response.content)

        if not os.path.exists(f'{shared.path_data}\\{name_file}'):
            self.update_progress(f'Falha ao baixar arquivo {name_file}')
            return False
        else:
            return True
