# ResumeApp - FastAPI + PostgreSQL в Docker

Простое приложение для управления резюме на FastAPI.

## Функционал
- Создание резюме
- Получение резюме по `id`
- Список всех резюме
- Обновление резюме
- Удаление резюме
- Улучшение резюме
- Swagger UI по адресу `/docs`

## Технологии
- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Pytest](https://docs.pytest.org/)

## Запуск проекта

1. Клонируйте репозиторий:

```bash
git clone https://github.com/Tqgeng/fastapi_user_resume.git
cd fastapi_user_resume
```

2. Соберите и запустите контейнеры:
```bash
docker compose up -d
```
3. Приложение будет доступно по адресу:

Frontend: http://localhost:8000/

Swagger UI: http://localhost:8000/docs

4. Тесты

```bash
pytest tests/test_resumes.py -v
```

5. Структура проекта
```
fastapi-application/
├── actions/ 
├── alembic/  
├── api/               
├── core/
├── static/
├── templates/              
├── crud/              
├── tests/  
├── utils/         
├── main.py            
```
- **actions/** - скрипты для админских/вспомогательных задач.  
- **alembic/** - миграции Alembic для обновления схем БД. 
- **api/** - здесь описаны все маршруты и эндпоинты FastAPI.  
- **core/** - модели SQLAlchemy, Pydantic-схемы, конфигурации. 
- **static/** - css и js файлы для фронта
- **templates/** - jinja html шаблоны
- **crud/** - функции для работы с базой данных.  
- **tests/** - юнит- и интеграционные тесты.  
- **utils/** - удобное наименование для миграций
- **main.py** - запускает FastAPI-приложение.
