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
        Subtheme,
        Sales
    )


class PrintModel(BaseModel):
    id_subtheme:Mapped[int] = mapped_column(ForeignKey("subtheme.id"),unique=True)
    subtheme:Mapped["Subtheme"] = relationship("Subtheme",back_populates="print_models")

    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[str] = mapped_column(default="")
    url_image:Mapped[str] = mapped_column(default="")

    sales:Mapped[list["Sales"]] = relationship("Sales",back_populates="print_model")

    def get_theme(self):
        return self.subtheme.theme