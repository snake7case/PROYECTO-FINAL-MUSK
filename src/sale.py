class Sale:
    """Representa una venta individual."""

    def __init__(self, sale_id, client_id, product, category, amount, date):
        self.sale_id = sale_id
        self.client_id = client_id
        self.product = product
        self.category = category
        self.amount = amount
        self.date = date

    @classmethod
    def from_dict(cls, data):
        """Crea una venta desde un diccionario o fila ya normalizada."""
        return cls(
            data["sale_id"],
            data["client_id"],
            data["product"],
            data["category"],
            data["amount"],
            data["date"],
        )

    def to_dict(self):
        """Devuelve la venta como un diccionario serializable."""
        return {
            "sale_id": self.sale_id,
            "client_id": self.client_id,
            "product": self.product,
            "category": self.category,
            "amount": self.amount,
            "date": self.date,
        }

    def __repr__(self):
        return (
            "Sale("
            f"sale_id={self.sale_id!r}, "
            f"client_id={self.client_id!r}, "
            f"product={self.product!r}, "
            f"category={self.category!r}, "
            f"amount={self.amount!r}, "
            f"date={self.date!r}"
            ")"
        )
