from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.db import Base, get_async_session

# Настройка тестовой базы данных
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Переопределение зависимости для получения тестовой сессии
def override_get_db():
    global db
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_async_session] = override_get_db

# Клиент для тестирования
client = TestClient(app)

def test_get_users():
    # Подготовка данных для теста
    # Здесь можно добавить пользователей в тестовую базу данных, если это необходимо

    # Выполнение запроса к эндпоинту
    response = client.get("/api/v1/users")

    # Проверка ответа
    assert response.status_code == 200
    assert isinstance(response.json(), list)