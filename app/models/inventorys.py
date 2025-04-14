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

from sqlalchemy.dialects.postgresql import ENUM
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        Material
    )

quantity_type_enum = ENUM("none", "unity", name="quantity_type",create_type=True)

class Inventory(BaseModel):
    type:Mapped[str] = mapped_column(default="")
    name:Mapped[str] = mapped_column(default="")
    description:Mapped[str] = mapped_column(default="")
    quantity:Mapped[int] = mapped_column(default=0)
    quantity_type:Mapped[str] = mapped_column(quantity_type_enum,default="none")


class MaterialInventory(BaseModel):
    id_material:Mapped[int] = mapped_column(ForeignKey("material.id"),nullable=False,unique=True)
    material:Mapped["Material"] = relationship(back_populates="inventory")

    quantity:Mapped[int] = mapped_column(default=0)