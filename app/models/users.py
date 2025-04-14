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

    def get_auth_level(self):
        return self.auth_level