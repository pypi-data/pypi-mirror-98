from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base

class Backend():
    Base = automap_base()

    def __init__(self, dburi):
        self._engine = create_engine(dburi, echo=True)
        self.Base.prepare(self._engine, reflect=True)

    def get_nodes():
        """
        """
        Node = self.Base.classes.nodes
