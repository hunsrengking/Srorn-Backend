# Feature Layout

Each folder in `app/features` owns one business area.

```text
app/features/<feature>/
  route.py       FastAPI router and URL wiring
  controller.py  FeatureController class used by route.py
  service.py     Business logic and database work
  models.py      Pydantic request/response models
  schema.py      SQLAlchemy database model
```

Not every feature needs every file. Keep shared infrastructure in `app/config`,
`app/middlewares`, and `app/constants`.

To add a new feature:

1. Create `app/features/<feature>/`.
2. Put FastAPI decorators only in `route.py`.
3. Put request handling methods on `<Feature>Controller` in `controller.py`.
4. Add the files that feature needs.
5. Add its router module to `ROUTER_MODULES` in `app/features/registry.py`.
6. If it defines SQLAlchemy tables, add those modules to
   `DATABASE_MODEL_MODULES` in `app/features/registry.py`.
