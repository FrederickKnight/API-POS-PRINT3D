from sympy import sympify
import uuid

from app.models import (
    BaseModel
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    Session
)

from sqlalchemy import (
    ForeignKey,
    JSON,
    event
)

from typing import (
    Optional
)

from sqlalchemy.dialects.postgresql import ENUM

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.models import (
        PrintModel,
        MaterialType,
        Client,
        User
    )

risk_type_enum = ENUM("low", "medium", "high", name="risk_type",create_type=True)


class Sales(BaseModel):
    id_ticket:Mapped[int] = mapped_column(ForeignKey("ticket.id"))
    ticket:Mapped["Ticket"] = relationship("Ticket",back_populates="sales")

    id_print_model:Mapped[int] = mapped_column(ForeignKey("print_model.id"))
    print_model:Mapped["PrintModel"] = relationship("PrintModel",back_populates="sales")
    
    id_general_price:Mapped[int] = mapped_column(ForeignKey("general_prices.id"))
    general_price:Mapped["GeneralPrices"] = relationship("GeneralPrices",back_populates="sales")

    material_quantity:Mapped[int] = mapped_column(default=0)
    print_time:Mapped[int] = mapped_column(default=0)


    risk:Mapped[str] = mapped_column(risk_type_enum,default="low")

    error_sale:Mapped["ErrorSale"] = relationship("ErrorSale",back_populates="sale",uselist=False)

    discount:Mapped[float] = mapped_column(default=0.0)
    raw_total:Mapped[Optional[float]] = mapped_column(default=0.0)
    total:Mapped[Optional[float]] = mapped_column(default=0.0)
    
    def has_error(self):
        return self.error_sale is not None

    def get_error(self):
        if self.has_error():
            return self.error_sale
        else:
            return None
        
@event.listens_for(Sales, "before_insert")
def calculate_totals(mapper, connection, target:Sales):

    session = Session(bind = connection)

    general_price = session.query(GeneralPrices).get(target.id_general_price)
    if not general_price:
        raise ValueError(f"GeneralPrices with id {target.id_general_price} not found")

    raw_total = general_price.calculate_raw_total(target.material_quantity, target.print_time, target.risk)
    total = general_price.calculate_total(target.material_quantity, target.print_time, target.discount, target.risk)

    target.raw_total = float(raw_total)
    target.total = float(total)

@event.listens_for(Sales, "after_update")
def calculate_totals_when_update(mapper, connection, target:Sales):
    raw_total = target.general_price.calculate_raw_total(target.material_quantity, target.print_time, target.risk)
    total = target.general_price.calculate_total(target.material_quantity, target.print_time, target.discount, target.risk)

    target.raw_total = float(raw_total)
    target.total = float(total)

class ErrorSale(BaseModel):
    id_sale:Mapped[int] = mapped_column(ForeignKey("sales.id"),unique=True)
    sale:Mapped["Sales"] = relationship("Sales",back_populates="error_sale")

    waste:Mapped[float] = mapped_column(default=0.0)
    reajusted_price:Mapped[float] = mapped_column(default=0.0)
    description:Mapped[str] = mapped_column(default="")


class Ticket(BaseModel):
    sales:Mapped[list["Sales"]] = relationship("Sales",back_populates="ticket")

    id_client:Mapped[int] = mapped_column(ForeignKey("client.id"))
    client:Mapped["Client"] = relationship("Client",back_populates="tickets")

    id_user:Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"),nullable=True)
    user:Mapped["User"] = relationship("User",back_populates="tickets")

    date:Mapped[str] = mapped_column(default="")
    subject:Mapped[str] = mapped_column(default="")

    uuid:Mapped[Optional[str]] = mapped_column(default=None,unique=True)

    total:Mapped[Optional[float]] = mapped_column(default=0.0)

    def get_total(self):
        total = 0.0
        for sale in self.sales:
            total += sale.error_sale.reajusted_price if sale.has_error() else sale.total
        return total
            
    
@event.listens_for(Ticket, "before_insert")
def generate_uuid(mapper, connection, target:Ticket):
    generated_uuid = str(uuid.uuid4())
    target.uuid = generated_uuid


@event.listens_for(Sales, "after_insert")
def update_total(mapper, connection, target:Sales):

    ticket_id = target.id_ticket
    if not ticket_id:
        return
    
    session = Session(bind = connection)
    
    ticket = session.query(Ticket).get(ticket_id)
    if not ticket:
        raise ValueError(f"Ticket with id {ticket_id} not found")
    
    ticket.total = ticket.get_total()
    session.commit()

class GeneralPrices(BaseModel):
    id_material_type:Mapped[int] = mapped_column(ForeignKey("material_type.id"))
    material_type:Mapped["MaterialType"] = relationship("MaterialType",back_populates="general_prices")

    date:Mapped[str] = mapped_column(default="")

    wear:Mapped[float] = mapped_column(default=0.0)
    electricity:Mapped[float] = mapped_column(default=0.0)
    margin:Mapped[float] = mapped_column(default=0.0)
    failure_risk:Mapped[dict] = mapped_column(JSON, default={"low": 0.0, "medium": 0.0, "high": 0.0})

    formula: Mapped[str] = mapped_column(default="(wear + electricity + margin + failure_risk[risk]) * (material_quantity + print_time)")

    sales:Mapped[list["Sales"]] = relationship("Sales",back_populates="general_price")

    def calculate_raw_total(self,material_quantity,print_time,risk = "low"):
        context = {
            "wear": self.wear,
            "electricity": self.electricity,
            "margin": self.margin,
            "material_quantity": material_quantity,
            "print_time": print_time,
            "risk": risk
        }

        # Reemplazar manualmente failure_risk[risk] con su valor correspondiente
        if "failure_risk[risk]" in self.formula:
            risk_value = self.failure_risk.get(risk, 0.0)  # Obtener el valor del riesgo
            formula = self.formula.replace("failure_risk[risk]", str(risk_value))
        else:
            formula = self.formula

        try:
            # Evaluar la fórmula con sympy
            sympy_formula = sympify(formula)
            total = sympy_formula.evalf(subs=context)
        except Exception as e:
            raise ValueError(f"Error al evaluar la fórmula: {e}")
        return total
    
    def calculate_total(self, material_quantity, print_time, discount=0.0, risk="low"):
        raw_total = self.calculate_raw_total(material_quantity, print_time, risk)
        total = raw_total * (1 - discount / 100)
        return total