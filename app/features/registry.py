from importlib import import_module

from fastapi import FastAPI


ROUTER_MODULES = [
    "app.features.users.route",
    "app.features.auth.route",
    "app.features.setting.roles.route",
    "app.features.tickets.route",
    "app.features.organization.departments.route",
    "app.features.setting.statuses.route",
    "app.features.setting.telegram.route",
    "app.features.notifications.route",
    "app.features.dashboard.route",
    "app.features.organization.positions.route",
    "app.features.organization.staff.route",
    "app.features.reports.route",
    "app.features.students.route",
    "app.features.organization.print.route",
    "app.features.setting.system.route",
    "app.features.organization.offices.route",
    "app.features.setting.code.route",
    "app.features.assets.route",
]


DATABASE_MODEL_MODULES = [
    "app.features.users.schema",
    "app.features.organization.departments.schema",
    "app.features.setting.roles.schema",
    "app.features.setting.roles.permission_schema",
    "app.features.setting.statuses.schema",
    "app.features.setting.statuses.category_schema",
    "app.features.setting.statuses.priority_schema",
    "app.features.tickets.schema",
    "app.features.tickets.item_schema",
    "app.features.setting.telegram.schema",
    "app.features.notifications.schema",
    "app.features.organization.positions.schema",
    "app.features.organization.staff.schema",
    "app.features.students.schema",
    "app.features.organization.print.schema",
    "app.features.setting.system.schema",
    "app.features.organization.offices.schema",
    "app.features.setting.code.schema",
    "app.features.assets.schema",
    "app.features.assets.assignments_schema",
]


def include_feature_routers(app: FastAPI) -> None:
    for module_path in ROUTER_MODULES:
        module = import_module(module_path)
        app.include_router(module.router)


def import_database_models() -> None:
    for module_path in DATABASE_MODEL_MODULES:
        import_module(module_path)
