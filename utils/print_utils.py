from typing import List, Tuple, Dict
from utils.date_utils import * 

def print_pairs(data: List[Tuple[str, float, float, float]], title: str, header: bool = True) -> None:
    """
    Prints formatted data to the console.

    Args:
        data (List[Tuple[str, float, float, float]]): A list of tuples containing the pair information. 
        Each tuple represents a row of data and consists of the pair name, price, funding rate, and 24-hour change.
        title (str): The title for the section of pairs being printed.
        header (bool, optional): A flag indicating whether to print the header row or not. Defaults to True.

    Returns:
        None: The function only prints the formatted data to the console.
    """
    print(f"\r\n--- {title} ---")
    if header:
        print(f"  {'Pair':<8} | "
              f"{'Price':<10} | "
              f"{'% Funding':<10} | "
              f"{'% 24h Change':<10}")

    for pair, price, funding_rate, change_24hr in data:
        color = '\033[92m' if change_24hr >= 0 else '\033[91m'  # Green for positive, red for negative
        print(color + f"{pair:<10} | "
              f"{price if price is not None else 'N/A':<10} | "
              f"{round(funding_rate, 4) if funding_rate is not None else 'N/A':<10} | "
              f"{round(change_24hr, 3) if change_24hr is not None else 'N/A':<10}" + '\033[0m')  # Reset color
        
async def print_data(data: Dict, countdown: str, num_pairs: int) -> None:
    """
    Prints formatted data to the console.

    Args:
        data (List[Tuple[str, float, float, float]]): A list of tuples containing the data to be printed.
        Each tuple represents a row of data and consists of the pair name, price, funding rate, and 24-hour change.

    Returns:
        None: The function only prints the formatted data to the console.
    """
    print_pairs(data['trading_pairs'], "My Pairs Information", header=True)
    print_pairs(data['top_shorted_pairs'], "Top shorted pairs", header=True)
    print_pairs(data['top_longed_pairs'], "Top longed pairs", header=True)  # New line
    print_pairs(data['top_gainers'], "Top Gainers", header=True)
    print_pairs(data['top_losers'], "Top Losers", header=True)

    # Move the cursor up by the number of trading pairs
    print(f"\nFunding countdown: {countdown} ")
    print(f"\033[{num_pairs + 17}A", end="")