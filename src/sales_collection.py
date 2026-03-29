class SalesCollection:
    """Gestiona una lista de ventas."""

    def __init__(self, sales=None):
        self.sales = sales or []

    def sales_by_client(self, client_id):
        return [sale for sale in self.sales if sale.client_id == client_id]

    def total_amount_by_client(self, client_id):
        return sum(sale.amount for sale in self.sales_by_client(client_id))

    def total_amount_by_category(self, category):
        return sum(sale.amount for sale in self.sales if sale.category == category)

    def average_sale_by_client(self, client_id):
        client_sales = self.sales_by_client(client_id)
        if not client_sales:
            return 0
        return self.total_amount_by_client(client_id) / len(client_sales)

    def add_sale(self, sale):
        self.sales.append(sale)

    def __iter__(self):
        return iter(self.sales)

    def __len__(self):
        return len(self.sales)
