import requests
from bs4 import BeautifulSoup

from src.components_ui.dialogs import Dialogs
from src.controller.base_controller import BaseController
from src.utils.functions import (
    get_env
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
            response = requests.get(f'{self.__base_url_anac}/diversos/vra/')
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