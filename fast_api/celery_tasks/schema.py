from sqlalchemy import Column, Integer, String, LargeBinary, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CeleryTaskMeta(Base):
    __tablename__ = "celery_taskmeta"
    id = Column(Integer, primary_key=True)
    task_id = Column(String)
    status = Column(String)
    result = Column(LargeBinary)