"""CLI Commands"""
import datetime
import json
import logging
import numpy as np
import pathlib
import pandas as pd

# from openai import OpenAI
import typer

from src import utilities
from src import plot_utilities
from src import stock_utilities


APP = typer.Typer()
logging.basicConfig()
logging.getLogger().setLevel(level=logging.INFO)
PETPOOJA_SKIP_N_ROWS = 4


@APP.command("sales-by-category")
def sales_by_category(
    excel_path: pathlib.Path = typer.Argument(..., 
                                            help="Path to excel file"),
    output_path: pathlib.Path = typer.Option(
        None, help="Output folder.")
) -> None:
    """Create Pie Chart."""
    dataframe = utilities.load_dataframe(excel_path)
    dataframe.dropna(subset=["Category"], inplace=True)
    logging.info(f"Dataframe columns: {dataframe.columns}")
    dataframe["ItemNameAndQuantity"] = dataframe["Item Name"] + ' - (' + dataframe["Qty."].astype(str) + ')'
    
    categories = dataframe["Category"].unique()
    logging.info(f"Unique Categories - {len(categories)} : {categories}")
    for category in categories:
        category_dataframe = dataframe.loc[dataframe["Category"] == category]
        logging.info(f"Number of items in {category} - {category_dataframe.shape[0]}")
        category_output_path = output_path / f"Sales_By_Category_{category}.png"
        plot_utilities.pie_chart(category_dataframe,
                                 "ItemNameAndQuantity",
                                 "Total Amount",
                                 f"{str(category).upper()} SALES",
                                 category_output_path)


# @APP.command("categorize-items")
# def categorize_items(
#         file_path: pathlib.Path = typer.Argument(..., 
#                         help="Path to excel file"),):
#     """Categorize items """
#     client = OpenAI(api_key=OPENAI_KEY)
#     items = utilities.load_text(file_path)
#     content = "Categorize items into Vegetables, Spices, Meat, Packaging, Canned Items, Foodgrains, Dals, Oil And Butter in json format - "
#     content += " " + items
#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "user", "content": content}
#     ]
#     )

#     result = completion.choices[0].message.content
#     result = json.loads(result)
#     print(result)


@APP.command()
def track_packaging(
    orders: pathlib.Path = typer.Argument(
        ...,
        help="Order File From PetPooja. Should be CSV File."
    )
):
    """Tracks the packaging Materials."""
    order_listing = utilities.load_dataframe(orders, skipfirstnrows=PETPOOJA_SKIP_N_ROWS)
    order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value] = pd.to_datetime(
        order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value]).sort_values(ascending=False)
    latest_date = order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value].values[0]
    latest_date = pd.to_datetime(str(latest_date))
    latest_date = latest_date.strftime("%d_%m_%Y")
    updated_order_listing=stock_utilities.update_packaging_stock_on_orders(
            order_listing, orders_latest_date = latest_date
        )
    updated_order_listing.to_excel(f"./data/processedOrders/packaging/PP_Order_list_{latest_date}.xlsx")
    print("Packaging Updated Successfully!")


@APP.command()
def track_stock(
    orders: pathlib.Path = typer.Argument(
        ...,
        help="Order File From PetPooja. Should be CSV File."
    )
):
    """Tracks the stock Materials."""
    order_listing = utilities.load_dataframe(orders, skipfirstnrows=PETPOOJA_SKIP_N_ROWS)
    order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value] = pd.to_datetime(
        order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value]).sort_values(ascending=False)
    latest_date = order_listing[stock_utilities.PetPoojaOrderFileColumns.CREATED.value].values[0]
    latest_date = pd.to_datetime(str(latest_date))
    latest_date = latest_date.strftime("%d_%m_%Y")
    updated_order_listing=stock_utilities.update_material_stock_on_orders(
            order_listing, orders_latest_date = latest_date
        )
    updated_order_listing.to_excel(f"./data/processedOrders/stock/PP_Order_list_{latest_date}.xlsx")

    print("Stock Updated Successfully!")


@APP.command("summarize-expenses")
def summarize_expense_reports(
    expenses: pathlib.Path = typer.Argument(
        ...,
        help="Expense Report having Excel File"
    )
) -> None:
    """Summarize expense reports."""
    dataframe = pd.read_excel(expenses)
    dataframe["Category"] = dataframe["Category"].str.lower().str.strip()
    grouped_dataframe = dataframe.groupby("Category")["Expense"].sum().reset_index()
    print("Category Wise Expenses")
    print(grouped_dataframe)
    grouped_dataframe = dataframe.groupby("Paid By")["Expense"].sum().reset_index()
    print("Paid By Expenses")
    print(grouped_dataframe)


if __name__ == "__main__":
    APP()