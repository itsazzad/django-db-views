import logging
from typing import Iterable, Optional, List

from django.conf import settings
from django.apps import apps
from django.db.transaction import get_connection

from django_db_views.autodetector import ViewMigrationAutoDetector
from django_db_views.db_view import DBViewsRegistry
from django_db_views.helpers import get_view_definitions_from_model

LOGGER = logging.getLogger("django_db_views")


def install(*view_db_names: Optional[Iterable[str]], databases: List[str]):
    """
    Install views on database without migrations - based on current model state
    """
    view_db_names_to_process = view_db_names or DBViewsRegistry.keys()
    databases = databases or ["default"]
    logging.info("installing views..")
    for view_db_name in view_db_names_to_process:
        view_model = DBViewsRegistry["view_db_name"]
        view_definitions = get_view_definitions_from_model(view_model)
        for engine, view_definition in view_definitions.items():
            for database in databases:
                if settings.DATABASES[database]['ENGINE'] == engine:
                    forward_migration_class = ViewMigrationAutoDetector.get_forward_migration_class(view_model)
                    forward_migration = forward_migration_class(
                        view_definition,
                        view_model._meta.db_table,
                        engine=engine
                    )
                    logging.info("processing view: %s", view_db_name)
                    forward_migration(apps, get_connection(database))

