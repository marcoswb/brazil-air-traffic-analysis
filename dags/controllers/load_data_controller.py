import pandas as pd
from models import *
from controllers.csv_controller import CSVController
from controllers.base_controller import BaseController
from controllers.database import engine, Base, get_connection, create_schema
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
        create_schema()
        Base.metadata.create_all(bind=engine)
        self.update_progress('TABELAS CRIADAS COM SUCESSO!')

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

        df = CSVController.normalize_csv(f'{self.__base_path}/normalized/cias.csv')
        for row in df.itertuples():
            icao_code = row.icao_operador_aereo
            airline = Airline(
                icao_code=icao_code,
                iata_code=row.iata_operador_aereo,
                name=row.nome_operador_aereo,
                headquarters_country=row.pais_sede,
            )
            self._save_data(airline, 'airline', icao_code)

        df = CSVController.normalize_csv(f'{self.__base_path}/normalized/aerodromos.csv')
        for row in df.itertuples():
            icao_code = row.sigla_icao_aerodromo
            airport = Airport(
                icao_code=icao_code,
                iata_code=row.sigla_iata_aerodromo,
                name=row.nome_aerodromo,
                municipality=row.municipio_aerodromo,
                state=row.estado_aerodromo,
                country=row.pais_aerodromo,
                critical_aircraft=row.aeronave_critica,
                latitude=row.latitude,
                longitude=row.longitude,
            )
            self._save_data(airport, 'airport', icao_code)

        self.__connection_db.commit()

        self.update_progress('--------------------------------------------------------------------')
        self.update_progress('REGISTROS AUXILIARES GRAVADOS')
        self.update_progress(self.__data_db)
        self.update_progress('--------------------------------------------------------------------')

        df = CSVController.normalize_csv(f'{self.__base_path}/normalized/voos.csv')
        df = CSVController.format_timestamp_column(df, 'partida_prevista')
        df = CSVController.format_timestamp_column(df, 'partida_real')
        df = CSVController.format_timestamp_column(df, 'chegada_prevista')
        df = CSVController.format_timestamp_column(df, 'chegada_real')

        total_records = len(df)
        batch_size = 20000
        for i, row in enumerate(df.itertuples(), start=1):
            flight_number = row.numero_voo

            flight = Flights(
                flight_number=flight_number,
                seat_capacity=row.numero_de_assentos,
                scheduled_departure=row.partida_prevista,
                actual_departure=row.partida_real,
                scheduled_arrival=row.chegada_prevista,
                actual_arrival=row.chegada_real,
                flight_status=row.situacao_voo,
                reference_date=row.referencia,
                aircraft_id=self.__data_db.get(('aircraft', row.modelo_equipamento)),
                airline_id=self.__data_db.get(('airline', row.sigla_icao_empresa_aerea)),
                departure_airport_id=self.__data_db.get(('airport', row.sigla_icao_aeroporto_origem)),
                arrival_airport_id=self.__data_db.get(('airport', row.sigla_icao_aeroporto_destino)),
            )
            self._save_data(flight, 'flight', None)

            if i % batch_size == 0:
                self.__connection_db.commit()
                self.update_progress(f'REGISTROS INSERIDOS: {i}/{total_records}')

        self.__connection_db.commit()

    def _save_data(self, object_insert, table, key_search):
        self.__connection_db.add(object_insert)
        if key_search:
            self.__connection_db.flush()
            self.__data_db[table, key_search] = object_insert.id