from django.conf import settings

from django_db_views.db_view import DBView


def _get_cleaned_view_definition_value(view_definition: str) -> str:
    assert isinstance(view_definition, str), \
        "View definition must be callable and return string or be itself a string."
    return view_definition.strip()


def get_view_definitions_from_model(view_model: DBView) -> dict:
    view_definitions = {}
    if callable(view_model.view_definition):
        raw_view_definition = view_model.view_definition()
    else:
        raw_view_definition = view_model.view_definition

    if isinstance(raw_view_definition, dict):
        for engine, definition in raw_view_definition.items():
            view_definitions[engine] = _get_cleaned_view_definition_value(definition)
    else:
        engine = settings.DATABASES['default']['ENGINE']
        view_definitions[engine] = _get_cleaned_view_definition_value(raw_view_definition)
    return view_definitions
