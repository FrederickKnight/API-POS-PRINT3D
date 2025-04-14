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
        MaterialInventory,
        GeneralPrices
    )

measurement_type_enum = ENUM("none", "l", "ml", "kg", "g", name="measurement_type",create_type=True)


class MaterialType(BaseModel):
    name:Mapped[str] = mapped_column(default="")

    materials:Mapped[list["Material"]] = relationship(back_populates="material_type",cascade="all, delete-orphan")
    general_prices:Mapped[list["GeneralPrices"]] = relationship(back_populates="material_type",cascade="all, delete-orphan")

class Material(BaseModel):
    name:Mapped[str] = mapped_column(default="")
    brand:Mapped[str] = mapped_column(default="")
    measurement_type:Mapped[str] = mapped_column(measurement_type_enum,default="none")
    color:Mapped[str] = mapped_column(default="")

    id_material_type:Mapped[int] = mapped_column(ForeignKey("material_type.id"))
    material_type:Mapped["MaterialType"] = relationship("MaterialType",back_populates="materials")
    
    inventory:Mapped["MaterialInventory"] = relationship(back_populates="material",cascade="all, delete-orphan")