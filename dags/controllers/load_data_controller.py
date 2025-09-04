from controllers.database import engine, Base
from models import *

from controllers.base_controller import BaseController

class LoadDataController(BaseController):

    def __init__(self):
        super().__init__()

    def create_tables(self):
        Base.metadata.create_all(bind=engine)
        self.update_progress('Tabelas criadas com sucesso!')