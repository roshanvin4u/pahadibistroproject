"""CLI Commands"""
import logging
import pathlib

import typer

from src import utilities
from src import plot_utilities


APP = typer.Typer()
logging.basicConfig()
logging.getLogger().setLevel(level=logging.INFO)


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


@APP.command("categorize-items")
def categorize_items():
    """Categorize items """


if __name__ == "__main__":
    APP()