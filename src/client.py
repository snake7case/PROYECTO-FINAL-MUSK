class Client:
    """Representa un cliente individual del proyecto."""

    def __init__(self, client_id, name, country, signup_date):
        self.client_id = client_id
        self.name = name
        self.country = country
        self.signup_date = signup_date

    @classmethod
    def from_dict(cls, data):
        """Crea un cliente a partir de un diccionario del JSON."""
        return cls(
            data["client_id"],
            data["name"],
            data["country"],
            data["signup_date"],
        )

    def to_dict(self):
        """Devuelve el cliente con el formato esperado por el JSON final."""
        return {
            "client_id": self.client_id,
            "name": self.name,
            "country": self.country,
            "signup_date": self.signup_date,
        }

    def __repr__(self):
        return (
            "Client("
            f"client_id={self.client_id!r}, "
            f"name={self.name!r}, "
            f"country={self.country!r}, "
            f"signup_date={self.signup_date!r}"
            ")"
        )
