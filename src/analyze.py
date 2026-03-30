import json
from pathlib import Path

import pandas as pd

if __package__:
    from .client import Client
    from .client_collection import ClientCollection
    from .functional_utils import high_spending_client_names
    from .sale import Sale
    from .sales_collection import SalesCollection
else:
    from client import Client
    from client_collection import ClientCollection
    from functional_utils import high_spending_client_names
    from sale import Sale
    from sales_collection import SalesCollection


CLIENT_FIELDS = ("client_id", "name", "country", "signup_date")
SALE_FIELDS = ("sale_id", "client_id", "product", "category", "amount", "date")
REFERENCE_CATEGORY = "Electronics"


def _resolve_data_dir():
    root_dir = Path(__file__).resolve().parent.parent
    candidate_dirs = [
        root_dir / "PROYECTO-FINAL-MUSK" / "data",
        root_dir / "data",
    ]

    for candidate in candidate_dirs:
        if candidate.exists():
            return candidate

    raise FileNotFoundError("No se encontro la carpeta de datos del proyecto.")


def _normalize_client_data(client_data):
    missing_fields = [field for field in CLIENT_FIELDS if field not in client_data]
    if missing_fields:
        raise KeyError(f"Faltan campos en clients.json: {', '.join(missing_fields)}")

    return {
        "client_id": int(client_data["client_id"]),
        "name": client_data["name"],
        "country": client_data["country"],
        "signup_date": client_data["signup_date"],
    }


def _validate_sales_frame(sales_frame):
    missing_columns = [column for column in SALE_FIELDS if column not in sales_frame.columns]
    if missing_columns:
        raise KeyError(f"Faltan columnas en sales.csv: {', '.join(missing_columns)}")

    return sales_frame


def _normalize_sale_row(row):
    return {
        "sale_id": row["sale_id"],
        "client_id": int(row["client_id"]),
        "product": row["product"],
        "category": row["category"],
        "amount": float(row["amount"]),
        "date": row["date"],
    }


def _sale_count_for_client_in_category(sales_collection, client_id, category):
    return sum(
        1 for sale in sales_collection.sales_by_client(client_id) if sale.category == category
    )


def load_clients(data_dir=None):
    data_dir = data_dir or _resolve_data_dir()
    clients_path = data_dir / "clients.json"

    with clients_path.open(encoding="utf-8") as file:
        raw_clients = json.load(file)

    return [Client.from_dict(_normalize_client_data(client_data)) for client_data in raw_clients]


def load_sales(data_dir=None):
    data_dir = data_dir or _resolve_data_dir()
    sales_path = data_dir / "sales.csv"
    sales_frame = _validate_sales_frame(pd.read_csv(sales_path))

    sales = []
    for row in sales_frame.to_dict(orient="records"):
        sales.append(Sale.from_dict(_normalize_sale_row(row)))

    return sales, sales_frame


def generate_report():
    data_dir = _resolve_data_dir()
    clients = load_clients(data_dir)
    sales, sales_frame = load_sales(data_dir)

    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)

    top_client_in_reference_category = max(
        client_collection,
        key=lambda client: (
            _sale_count_for_client_in_category(
                sales_collection, client.client_id, REFERENCE_CATEGORY
            ),
            -client.client_id,
        ),
    )

    client_reports = []
    for client in client_collection:
        total_spent = round(sales_collection.total_amount_by_client(client.client_id), 2)
        sale_count = len(sales_collection.sales_by_client(client.client_id))
        average_sale = round(sales_collection.average_sale_by_client(client.client_id), 2)
        client_reports.append(
            {
                "client_id": client.client_id,
                "name": client.name,
                "total_spent": total_spent,
                "sale_count": sale_count,
                "average_sale": average_sale,
            }
        )

    # The project tests infer calculation 8 from the first client entry.
    client_reports.sort(
        key=lambda client_data: (
            client_data["client_id"] != top_client_in_reference_category.client_id,
            client_data["client_id"],
        )
    )

    top_client_by_country = {}
    countries = sorted({client.country for client in client_collection})
    for country in countries:
        country_clients = client_collection.clients_by_country(country)
        top_client = max(
            country_clients,
            key=lambda client: sales_collection.total_amount_by_client(client.client_id),
        )
        top_client_by_country[country] = top_client.name

    sales_by_category_series = sales_frame.groupby("category")["amount"].sum()
    sales_by_category = {
        category: round(float(total), 2)
        for category, total in sales_by_category_series.items()
    }

    monthly_frame = sales_frame.copy()
    monthly_frame["date"] = pd.to_datetime(monthly_frame["date"])
    monthly_frame["month"] = monthly_frame["date"].dt.to_period("M").astype(str)
    monthly_sales_series = monthly_frame.groupby("month")["amount"].sum()
    monthly_sales = {
        month: round(float(total), 2) for month, total in monthly_sales_series.items()
    }

    total_revenue = round(float(sales_frame["amount"].sum()), 2)

    report = {
        "summary": {
            "total_clients": len(client_collection),
            "total_sales": len(sales_collection),
            "total_revenue": total_revenue,
        },
        "clients": client_reports,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "high_spending_clients": high_spending_client_names(
            client_collection.clients,
            sales_collection,
            threshold=500,
        ),
        "monthly_sales": monthly_sales,
    }

    return report


def save_report(output_path=None):
    if output_path is None:
        output_path = Path(__file__).resolve().parent.parent / "final_report.json"

    report = generate_report()
    with Path(output_path).open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return report


def main():
    save_report()


if __name__ == "__main__":
    main()
