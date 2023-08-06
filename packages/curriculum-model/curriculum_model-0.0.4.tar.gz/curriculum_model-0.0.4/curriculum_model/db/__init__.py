import sqlalchemy


class DB():
    """Simple class for handling DB connection

    Parameters
    ----------
    uri : str
        SQLAlchemy connection string. 
    verbose : boolean 
        Whether or not to output instructions setn to DB. 
    """

    def __init__(self, uri, verbose):
        self.uri = uri
        self.verbose = verbose

    def __enter__(self):
        self.engine = create_engine(self.engine_string, echo=self.verbose)
        self._sfactory = sessionmaker(bind=self._engine)
        self.con = self._engine.connect()
        return self

    def __exit__(self, type, value, traceback):
        self._engine.dispose()
        pass

    def session(self):
        """
        Returns an SQLAlchemy session object, for ORM work. 
        """
        s = self._sfactory()
        return s
