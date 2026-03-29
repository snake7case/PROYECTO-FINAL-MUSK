from functools import reduce


def filter_sales_by_category(sales, category):
    return list(filter(lambda sale: sale.category == category, sales))


def filter_sales_by_client(sales, client_id):
    return list(filter(lambda sale: sale.client_id == client_id, sales))


def sum_sale_amounts(sales):
    return reduce(lambda total, sale: total + sale.amount, sales, 0.0)


def high_spending_client_names(clients, sales_collection, threshold):
    return list(
        map(
            lambda client: client.name,
            filter(
                lambda client: sales_collection.total_amount_by_client(client.client_id)
                > threshold,
                clients,
            ),
        )
    )
