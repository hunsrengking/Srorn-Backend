from importlib import import_module

from fastapi import FastAPI


ROUTER_MODULES = [
    "app.features.users.route",
    "app.features.auth.route",
    "app.features.roles.route",
    "app.features.tickets.route",
    "app.features.departments.route",
    "app.features.statuses.route",
    "app.features.telegram.route",
    "app.features.notifications.route",
    "app.features.dashboard.route",
    "app.features.positions.route",
    "app.features.staff.route",
    "app.features.reports.route",
    "app.features.students.route",
    "app.features.organization.route",
    "app.features.system.route",
    "app.features.offices.route",
]


DATABASE_MODEL_MODULES = [
    "app.features.users.schema",
    "app.features.departments.schema",
    "app.features.roles.schema",
    "app.features.roles.permission_schema",
    "app.features.statuses.schema",
    "app.features.statuses.category_schema",
    "app.features.statuses.priority_schema",
    "app.features.tickets.schema",
    "app.features.tickets.item_schema",
    "app.features.telegram.schema",
    "app.features.notifications.schema",
    "app.features.positions.schema",
    "app.features.staff.schema",
    "app.features.students.schema",
    "app.features.organization.print_card_schema",
    "app.features.system.schema",
    "app.features.offices.schema",
]


def include_feature_routers(app: FastAPI) -> None:
    for module_path in ROUTER_MODULES:
        module = import_module(module_path)
        app.include_router(module.router)


def import_database_models() -> None:
    for module_path in DATABASE_MODEL_MODULES:
        import_module(module_path)
