import logging

from fastapi import FastAPI

from authors_service.routers.authors import authors_router
from authors_service.settings import SETTINGS

FORMAT = "[%(asctime)s][%(levelname)s][%(name)s] %(message)s"
logging.basicConfig(
    format=FORMAT, level=str.upper(SETTINGS.log_level), datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger()

app = FastAPI(title=SETTINGS.app_name)


async def startup_db():
    from authors_service.db import Base, engine, get_db_session
    from authors_service.db_models import AuthorDBModel  # noqa: F401

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db_session_cm = get_db_session()
    with db_session_cm as db_session:
        authors = [
            AuthorDBModel(name="Emily", surname="Emily St. John Mandel"),
            AuthorDBModel(name="Emily", surname="Henry"),
            AuthorDBModel(name="Bonnie", surname="Garmus"),
        ]
        for author in authors:
            db_session.add(author)
        db_session.commit()

    logger.info("created db")


app.add_event_handler("startup", startup_db)

app.include_router(authors_router)
