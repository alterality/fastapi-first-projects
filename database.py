from sqlalchemy import create_engine, MetaData
from databases import Database

# Замените следующую строку своей строкой подключения к базе данных
DATABASE_URL = "postgresql://aspire:1@localhost/fastapi"


# Создание объекта engine для синхронного доступа к базе данных через SQLAlchemy
engine = create_engine(DATABASE_URL)

# Создание объекта database для асинхронного доступа к базе данных через databases
database = Database(DATABASE_URL)

metadata = MetaData()
database = Database(DATABASE_URL)
metadata = MetaData()