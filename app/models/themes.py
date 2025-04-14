from app.models import (
    BaseModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from sqlalchemy import (
    ForeignKey
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        PrintModel
    )


class Theme(BaseModel):
    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[str] = mapped_column(default="")

    subthemes:Mapped[list["Subtheme"]] = relationship(back_populates="theme",cascade="all, delete-orphan")

    def get_subthemes(self):
        return self.subthemes

class Subtheme(BaseModel):
    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[str] = mapped_column(default="")

    id_theme:Mapped[int] = mapped_column(ForeignKey("theme.id"))
    theme:Mapped["Theme"] = relationship(back_populates="subthemes")

    print_models:Mapped[list["PrintModel"]] = relationship(back_populates="subtheme",cascade="all, delete-orphan")