class ClientCollection:
    """Gestiona una lista de clientes."""

    def __init__(self, clients=None):
        self.clients = clients or []

    def get_client_by_id(self, client_id):
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return None

    def clients_by_country(self, country):
        return [client for client in self.clients if client.country == country]

    def add_client(self, client):
        self.clients.append(client)

    def __iter__(self):
        return iter(self.clients)

    def __len__(self):
        return len(self.clients)
