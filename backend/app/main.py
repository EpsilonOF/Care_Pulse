
from fastapi import FastAPI
from routes import router
import os
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI()


DATABASE_URL = "postgres://user:password@db:5432/mydatabase"

register_tortoise(
    app,
    db_url=os.environ.get('DATABASE_URL'),
    modules={'models': ['db_models']},
    generate_schemas=True,
    add_exception_handlers=True,
)

# Inclure le router des routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
