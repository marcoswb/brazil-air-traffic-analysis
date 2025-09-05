from controllers.database import engine, Base
from models import *

from controllers.csv_controller import CSVController
from controllers.base_controller import BaseController
from controllers.database import get_connection
from models.aircraft import Aircraft
from models.airline import Airline
from models.airport import Airport
from models.flights import Flights

class LoadDataController(BaseController):

    def __init__(self):
        super().__init__()
        self.__base_path = self.get_env('BASE_PATH')
        self.__data_db = {}
        self.__connection_db = get_connection()

    def create_tables(self):
        Base.metadata.create_all(bind=engine)
        self.update_progress('Tabelas criadas com sucesso!')

    def load_data(self):
        df = CSVController.normalize_csv(f'{self.__base_path}/normalized/aeronaves.csv')
        for row in df.itertuples():
            icao_code = row.icao_aeronave
            aircraft = Aircraft(
                icao_code=icao_code,
                iata_code=[item.strip() for item in str(row.iata_aeronave).split(',')],
                model=row.modelo_aeronaver,
                critical_aircraft=row.aeronave_critica,
            )
            self._save_data(aircraft, 'aircraft', icao_code)
        self.__connection_db.commit()

        print(self.__data_db)

    def _save_data(self, object_insert, table, key_search):
        self.__connection_db.add(object_insert)
        self.__connection_db.flush()
        self.__data_db[table, key_search] = object_insert.id