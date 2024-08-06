import collections
import datetime
import enum
import itertools
import json
import pandas as pd
import numpy as np

class PackagingMaterial(enum.Enum):
    """Types of Packaging Material."""

    SMALL_PAPER_BOX_6x6 = "SMALL_PAPER_BOX_6x6"
    BIG_PAPER_BOX_8x5 = "BIG_PAPER_BOX_8x5"
    RECTANGULAR_PLASTIC_CONTAINER_500ML = "RECTANGULAR_PLASTIC_CONTAINER_500ML"
    ROUND_PLASTIC_CONTAINER_25ML = "ROUND_PLASTIC_CONTAINER_25ML"
    ROUND_PLASTIC_CONTAINER_50ML = "ROUND_PLASTIC_CONTAINER_50ML"
    ROUND_PLASTIC_CONTAINER_300ML = "ROUND_PLASTIC_CONTAINER_300ML"
    ROUND_PLASTIC_CONTAINER_500ML = "ROUND_PLASTIC_CONTAINER_500ML"
    ROUND_PLASTIC_CONTAINER_600ML = "ROUND_PLASTIC_CONTAINER_600ML"
    ROUND_PLASTIC_CONTAINER_1000ML = "ROUND_PLASTIC_CONTAINER_1000ML"
    ROUND_PAPER_CONTAINER_750ML = "ROUND_PAPER_CONTAINER_750ML"
    XL_TRAY_COMPARTMENT_BENTO_BOX = "XL_TRAY_COMPARTMENT_BENTO_BOX"
    SMALL_PAPER_BAG = "SMALL_PAPER_BAG"
    BIG_PAPER_BAG = "BIG_PAPER_BAG"


class StockMaterial(enum.Enum):
    """Types of Stock Material"""

    COKE_250_ML = "COKE_250_ML"
    THUMS_UP_250_ML = "THUMS_UP_250_ML"
    SPRITE_250_ML = "SPRITE_250_ML"
    WATER_1L = "WATER_1L"
    DIET_COKE_300ML = "DIET_COKE_300ML"


class OrderType(enum.Enum):
    """PetPooja Order Types"""
    DELIVERY = "Delivery"
    TAKEAWAY = "Take Away"


class CategoryType(enum.Enum):
    """PetPooja Order Types"""
    DRINKS = "Drinks"
    STAFF_DRINKS = "Staff Drinks"


class PetPoojaOrderFileColumns(enum.Enum):
    """Columns defining PetPooja Order File."""
    ITEMS = "Items"
    ORDERTYPE = "Order Type"
    PACKAGING_USED = "Packaging_Used"
    CREATED = "Created"
    STOCK_USED = "Stock_Used"


class PackagingConfigFileColumns(enum.Enum):
    """Columns defining Packaging Config File."""
    NAME = "Name"
    ONLINE_NAME = "Online_Name"
    PACKAGING_BOX = "Packaging Box"
    CATEGORY = "Category"
    STOCK = "Stock"


class TrackerTags(enum.Enum):
    """The tags in a tracker."""
    PRODUCT_CODE = "product_code"
    STOCK = "stock"
    AS_ON = "as_on"

def load_packaging_config():
    """Loads the packaging config."""
    packaging_config = pd.read_csv("./config/item_wise_packaging_master.csv")
    return packaging_config


def load_stock_config():
    """Loads the stock config."""
    stock_config = pd.read_csv("./config/item_wise_stock_master.csv")
    return stock_config


def load_packaging_tracker() -> list[dict]:
    """Loads the packaging tracker json file."""
    with open("./stock/packaging.json", "r") as f:
        packaging_stock_tracker = json.load(f)
    return packaging_stock_tracker


def load_stock_tracker() -> list[dict]:
    """Loads the packaging tracker json file."""
    with open("./stock/stock.json", "r") as f:
        stock_tracker = json.load(f)
    return stock_tracker


def save_packaging_tracker(packaging_tracker: list[dict], orders_latest_date: str, is_history: bool = False) -> list[dict]:
    """Loads the packaging tracker json file."""
    if not is_history:
        packaging_tracker_file_name = "./stock/packaging.json"
        with open(packaging_tracker_file_name, "w") as f:
            json.dump(packaging_tracker, f, indent=4)
    else:
        history_file_name = ("./stock/packaging_history/packaging_history_"
                            f"{orders_latest_date}.json")
        with open(history_file_name, "w") as f:
            json.dump(packaging_tracker, f, indent=4)


def save_stock_tracker(stock_tracker: list[dict], orders_latest_date: str, is_history: bool = False) -> list[dict]:
    """Saves the stock tracker json file."""
    if not is_history:
        packaging_tracker_file_name = "./stock/stock.json"
        with open(packaging_tracker_file_name, "w") as f:
            json.dump(stock_tracker, f, indent=4)
    else:
        history_file_name = ("./stock/stock_history/stock_history_"
                            f"{orders_latest_date}.json")
        with open(history_file_name, "w") as f:
            json.dump(stock_tracker, f, indent=4)
    

def find_packaging_used(
        order_row,
        packaging_config: pd.DataFrame,
):
    """Finds the packaging used for items per order."""
    packaging_used = []
    order_items = order_row[PetPoojaOrderFileColumns.ITEMS.value].split(",")
    for item in order_items:
        item = str(item).strip().lower()
        if len(item) > 0:
            item_packaging_config = packaging_config[(packaging_config[
                PackagingConfigFileColumns.ONLINE_NAME.value].str.lower() == item)]
            if (item_packaging_config.empty):
                item_packaging_config = packaging_config[(packaging_config[
                        PackagingConfigFileColumns.NAME.value].str.lower() == item)]
                if item_packaging_config.empty: 
                    raise ValueError(f"Could not find packaging config for item {item}.")
            if (item_packaging_config[PackagingConfigFileColumns.CATEGORY.value].values[0] not in [CategoryType.DRINKS.value, CategoryType.STAFF_DRINKS.value]):
                packaging_box_used = item_packaging_config[PackagingConfigFileColumns.PACKAGING_BOX.value].values[0]
                packaging_box_used = packaging_box_used.split(",")
                packaging_used += packaging_box_used

    order_row[PetPoojaOrderFileColumns.PACKAGING_USED.value] = packaging_used
    return order_row


def find_stock_used(
        order_row,
        stock_config: pd.DataFrame,
):
    """Finds the packaging used for items per order."""
    stock_used = []
    order_items = order_row[PetPoojaOrderFileColumns.ITEMS.value].split(",")
    for item in order_items:
        item = str(item).strip().lower()
        if len(item) > 0:
            item_stock_config = stock_config[(stock_config[
                PackagingConfigFileColumns.ONLINE_NAME.value].str.lower() == item)]
            if (item_stock_config.empty):
                item_stock_config = stock_config[(stock_config[
                        PackagingConfigFileColumns.NAME.value].str.lower() == item)]
                if item_stock_config.empty: 
                    raise ValueError(f"Could not find packaging config for item {item}.")
            stock_item_used = item_stock_config[PackagingConfigFileColumns.STOCK.value].values[0]
            if (type(stock_item_used) == str):
                stock_item_used = stock_item_used.split(",")
                stock_used += stock_item_used

    order_row[PetPoojaOrderFileColumns.STOCK_USED.value] = stock_used
    return order_row


def find_bags_used(order_row): # INCOMPLETE
    """Finds the bags used per order."""
    packaging_used = order_row[PetPoojaOrderFileColumns.PACKAGING_USED.value]
    bags_used = []
    bags_content = collections.defaultdict(list)
    remaining_space_in_bag = collections.defaultdict(int)
    if packaging_used:
        for packaging in packaging_used:
            if (packaging == PackagingMaterial.XL_TRAY_COMPARTMENT_BENTO_BOX.value):
                bags_content[PackagingMaterial.BIG_PAPER_BAG.value].append(packaging)
                bags_used.append(PackagingMaterial.BIG_PAPER_BAG.value)
                remaining_space_in_bag[PackagingMaterial.BIG_PAPER_BAG.value] = 0
                continue
            if (packaging == PackagingMaterial.ROUND_PLASTIC_CONTAINER_300ML.value or
                packaging == PackagingMaterial.ROUND_PLASTIC_CONTAINER_50ML.value):
                if bags_used:
                    bags_content[bags_used[0]].append(packaging)
                remaining_space_in_bag[PackagingMaterial.BIG_PAPER_BAG.value] = 0
                continue
    return order_row


def print_stock(details: list[dict]) -> None:
    """Prints the stock and packaging for messaging."""
    print("Remaining Packaging/Stock.")
    for detail in details:
        print(f"{detail[TrackerTags.PRODUCT_CODE.value]} : {detail[TrackerTags.STOCK.value]}")


def update_packaging_master(
        packaging_used: dict[PackagingMaterial, int],
        orders_latest_date: str
):
    """Updates the packaging master file."""
    packaging_tracker = load_packaging_tracker()
    save_packaging_tracker(packaging_tracker, orders_latest_date, is_history=True)
    for packaging, count_used in packaging_used.items():
        for packaging_stock in packaging_tracker:
            if packaging == packaging_stock[TrackerTags.PRODUCT_CODE.value]:
                packaging_stock[TrackerTags.STOCK.value] -= count_used
                packaging_stock[TrackerTags.AS_ON.value] = datetime.datetime.now().strftime("%d-%m-%Y")
    save_packaging_tracker(packaging_tracker, orders_latest_date)
    print_stock(packaging_tracker)


def update_stock_master(
        stock_used: dict[PackagingMaterial, int],
        orders_latest_date: str
):
    """Updates the packaging master file."""
    stock_tracker = load_stock_tracker()
    save_stock_tracker(stock_tracker, orders_latest_date, is_history=True)
    for stock_, count_used in stock_used.items():
        for stock_stock in stock_tracker:
            if stock_ == stock_stock[TrackerTags.PRODUCT_CODE.value]:
                stock_stock[TrackerTags.STOCK.value] -= count_used
                stock_stock[TrackerTags.AS_ON.value] = datetime.datetime.now().strftime("%d-%m-%Y")
    save_stock_tracker(stock_tracker, orders_latest_date)
    print_stock(stock_tracker)


def update_packaging_stock_on_orders(
        order_details: pd.DataFrame,
        orders_latest_date: str
    ) -> pd.DataFrame:
    """Updates Packaging Stock based on orders."""
    packaging_config = load_packaging_config()
    takeout_order_details =  order_details[
            order_details[PetPoojaOrderFileColumns.ORDERTYPE.value].isin(
                [OrderType.DELIVERY.value, OrderType.TAKEAWAY.value])].copy()
    dine_in_order_details = order_details[
            ~order_details[PetPoojaOrderFileColumns.ORDERTYPE.value].isin(
                [OrderType.DELIVERY.value, OrderType.TAKEAWAY.value])].copy()
    dine_in_order_details[PetPoojaOrderFileColumns.PACKAGING_USED.value] = ""
    takeout_order_details = takeout_order_details.apply(find_packaging_used, args=(packaging_config,), axis=1)
    total_packaging_used = takeout_order_details[PetPoojaOrderFileColumns.PACKAGING_USED.value].to_list()
    total_packaging_used = list(itertools.chain(*total_packaging_used))
    packaging_count = collections.Counter(total_packaging_used)
    print("Packaging Used - \n")
    print(packaging_count)
    update_packaging_master(packaging_count, orders_latest_date)
    all_order_details = pd.concat([dine_in_order_details, takeout_order_details])
    return all_order_details


def update_material_stock_on_orders(
    order_details: pd.DataFrame,
    orders_latest_date: str
) -> pd.DataFrame:
    """Update Raw Material Stock on orders."""
    stock_config = load_stock_config()
    order_details = order_details.apply(find_stock_used, args=(stock_config,), axis=1)
    total_stock_used = order_details[PetPoojaOrderFileColumns.STOCK_USED.value].to_list()
    total_stock_used = list(itertools.chain(*total_stock_used))
    stock_count = collections.Counter(total_stock_used)
    print("Stock Used - \n")
    print(stock_count)
    update_stock_master(stock_count, orders_latest_date)
    return order_details






