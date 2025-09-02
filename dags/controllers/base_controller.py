from airflow.models import Variable

class BaseController:

    @staticmethod
    def update_progress(message):
        print(message)

    @staticmethod
    def get_env(variable_key, default_value=None):
        result = Variable.get(variable_key, default_var=default_value)
        return result

    @staticmethod
    def raise_error(error):
        print(error)
        raise Exception
