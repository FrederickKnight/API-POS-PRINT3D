from app import db,Bcrypt
bcrypt = Bcrypt()

from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from sqlalchemy import (
    String,
    Boolean,
    DateTime
)

from sqlalchemy.sql import func


class BaseModel(db.Model):
    __abstract__ = True
    
    id:Mapped[int] = mapped_column(primary_key=True)

    
    def __repr__(self):
        attrs = [f"{col.name}={getattr(self, col.name)}" for col in self.__table__.columns]
        return f"<{self.__getClassName__()}({', '.join(attrs)})>"
    
    def get_json(self,include_relationships: bool = False):
        data = {col.name: getattr(self, col.name) for col in self.__table__.columns}
    
        if include_relationships:
            for rel in self.__mapper__.relationships:
                val = getattr(self, rel.key)
                if isinstance(val, list):
                    data[rel.key] = [item.get_json() for item in val]
                elif val is not None:
                    data[rel.key] = val.get_json()
                else:
                    data[rel.key] = None
                    
        return data

    def __getClassName__(self):
        return type(self).__name__

class BaseUser(BaseModel):
    __abstract__ = True

    username:Mapped[str] = mapped_column(String(20),unique=True)
    password:Mapped[str]

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    created_at:Mapped[datetime | None] = mapped_column(DateTime, default=func.now())
    deleted_at:Mapped[datetime | None] = mapped_column(DateTime,nullable=True)

    def __repr__(self):
        return f"<{self.__getClassName__()}(id={self.id},username={self.username})>"
        
    def get_json(self,include_relationships = None):
        return {
            "id":self.id,
            "username":self.username
        }
    
    def set_password(self,password:str):
        self.password = bcrypt.generate_password_hash(password).decode("utf-8")
    
    def validate_password(self,password:str):
        return bcrypt.check_password_hash(self.password,password)

class BaseSession(BaseModel):
    __abstract__ = True
    
    session:Mapped[str] = mapped_column(unique=True)
    expires_at:Mapped[int]