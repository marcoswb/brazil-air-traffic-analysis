import pandas as pd
from unidecode import unidecode
import os


class CSVController:

    @classmethod
    def normalize_csv(cls, path_csv, path_new_csv=None):
        df = pd.read_csv(path_csv, delimiter=';')

        normalized_columns = []
        for column in df.columns:
            normalized_columns.append(unidecode(str(column).replace(' ', '_')).lower())

        df.columns = normalized_columns
        df = df.replace("NaN", "").replace("nan", "").fillna("")
        df = df.replace({None: ""})

        if path_new_csv:
            df.to_csv(path_new_csv, sep=';', header=True, index=False)


        return df

    @classmethod
    def normalize_flights_data(cls, path_csv, path_new_csv):
        df = CSVController.normalize_csv(path_csv)

        df = df.drop(columns=[
            'empresa_aerea',
            'codigo_di',
            'codigo_tipo_linha',
            'descricao_aeroporto_origem',
            'descricao_aeroporto_destino',
            'justificativa',
            'situacao_partida',
            'situacao_chegada'
        ])

        if os.path.exists(path_new_csv):
            df.to_csv(path_new_csv, sep=';', mode='a', header=False, index=False)
        else:
            df.to_csv(path_new_csv, sep=';', header=True, index=False)