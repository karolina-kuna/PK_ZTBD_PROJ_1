from market_app.services.reader_manager import ReaderManager
from market_app.services.reader_options import ReaderOptions


def get_reader_manager():
    repository: ReaderManager = ReaderManager(ReaderOptions.CASSANDRA)
    yield repository
