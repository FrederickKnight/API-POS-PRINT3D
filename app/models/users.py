from app.models import (
    BaseModel,
    BaseUser
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy.dialects.postgresql import ENUM
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Session,
        Ticket
    )


class Client(BaseModel):
    name:Mapped[str] = mapped_column(default="")
    email:Mapped[str] = mapped_column(default="")
    telephone:Mapped[str] = mapped_column(default="")
    address:Mapped[str] = mapped_column(default="")

    tickets:Mapped[list["Ticket"]] = relationship(back_populates="client",cascade="all, delete-orphan")


auth_level_enum = ENUM("admin", "manager", "worker", name="auth_level_type",create_type=True)

class User(BaseUser):
    auth_level:Mapped[str] = mapped_column(auth_level_enum,default="worker")

    user_session:Mapped["Session"] = relationship("Session",back_populates="user",uselist=False)

    tickets:Mapped[list["Ticket"]] = relationship(back_populates="user",cascade="all, delete-orphan")

    def check_auth_level(self,levels):
        if self.auth_level == "admin":
            return True
        
        auth_level = self.auth_level.lower()

        if isinstance(levels,list):
            levels_lower = [level.lower() if isinstance(level, str) else level for level in levels]
            return auth_level in levels_lower
        elif isinstance(levels,str):
            return auth_level == levels.lower()
        
        return False