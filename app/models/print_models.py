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

from typing import (
    Optional
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Subtheme,
        Sales
    )

class BrandModel(BaseModel):
    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[Optional[str]] = mapped_column(default="",nullable=True)

    print_models:Mapped[list["PrintModel"]] = relationship("PrintModel",back_populates="brand")

class SetModel(BaseModel):
    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[Optional[str]] = mapped_column(default="",nullable=True)

    print_models:Mapped[list["PrintModel"]] = relationship("PrintModel",back_populates="set")

class PrintModel(BaseModel):
    id_subtheme:Mapped[int] = mapped_column(ForeignKey("subtheme.id"))
    subtheme:Mapped["Subtheme"] = relationship("Subtheme",back_populates="print_models")

    name:Mapped[str] = mapped_column(unique=True)
    description:Mapped[Optional[str]] = mapped_column(default="",nullable=True)
    url_image:Mapped[str] = mapped_column(default="")

    id_brand:Mapped[Optional[int]] = mapped_column(ForeignKey("brand_model.id"),nullable=True)
    brand:Mapped["BrandModel"] = relationship("BrandModel",back_populates="print_models")

    id_set:Mapped[Optional[int]] = mapped_column(ForeignKey("set_model.id"),nullable=True)
    set:Mapped["SetModel"] = relationship("SetModel",back_populates="print_models")

    model:Mapped[Optional[str]] = mapped_column(default="",nullable=True)

    sales:Mapped[list["Sales"]] = relationship("Sales",back_populates="print_model")

    def get_theme(self):
        return self.subtheme.theme