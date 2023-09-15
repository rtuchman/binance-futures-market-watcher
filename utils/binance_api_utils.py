import aiohttp
import asyncio
from typing import Dict, List, Optional, Tuple


class BinanceAPI:
    """
    The `BinanceAPI` class is a wrapper for making asynchronous HTTP requests to the Binance API.
    It provides methods to retrieve price data, 24-hour change data, funding rates,
    and other information related to Binance Futures trading pairs.

    Main functionalities:
    - Retrieve the price of a trading pair
    - Retrieve the 24-hour change percentage of a trading pair
    - Retrieve the top gainers and losers among Binance Futures trading pairs
    - Retrieve the funding rate of a trading pair
    - Retrieve the top shorted and longed trading pairs based on funding rates
    - Retrieve data for multiple trading pairs


    Fields:
    - PRICE_URL: The URL for retrieving price data.
    - FUNDING_URL: The URL for retrieving funding rate data.
    - DAILY_CHANGE_URL: The URL for retrieving 24-hour change data.
    - EXCHANGE_INFO_URL: The URL for retrieving Binance Futures trading pair information.
    - session: The aiohttp.ClientSession object used for making HTTP requests.
    """
    PRICE_URL = "https://fapi.binance.com/fapi/v1/ticker/price"
    FUNDING_URL = "https://fapi.binance.com/fapi/v1/premiumIndex"
    DAILY_CHANGE_URL = "https://api.binance.com/api/v3/ticker/24hr"
    EXCHANGE_INFO_URL = "https://fapi.binance.com/fapi/v1/exchangeInfo"

    def __init__(self, session: aiohttp.ClientSession):
        """
        Initializes an instance of the BinanceAPI class.

        Args:
            session (aiohttp.ClientSession): The aiohttp.ClientSession object used for making HTTP requests.
        """
        self.session = session

    async def get_price(self, pair: str) -> str:
        """
        Retrieves the price of a trading pair from the Binance API.

        Args:
            pair (str): The trading pair for which the price needs to be retrieved.

        Returns:
            str: The price of the trading pair as a string.
        """
        async with self.session.get(self.PRICE_URL, params={"symbol": pair}) as response:
            data = await response.json()
            if "price" in data:
                return data["price"]
            else:
                return "0"  # or some other default value

    async def get_24hr_change(self, pair: str) -> Optional[float]:
        """
        Retrieves the 24-hour change percentage of a trading pair from the Binance API.

        Args:
            pair (str): The trading pair for which the 24-hour change percentage needs to be retrieved.

        Returns:
            Optional[float]: The 24-hour change percentage of the trading pair as a float, or None if the percentage cannot be retrieved or converted.
        """
        async with self.session.get(self.DAILY_CHANGE_URL, params={"symbol": pair}) as response:
            data = await response.json()
            try:
                return float(data.get("priceChangePercent", 0))
            except ValueError:
                return None

    async def get_24hr_change_all(self) -> List[Dict[str, str]]:
        """
        Retrieves the 24-hour change data for all trading pairs from the Binance API.

        Returns:
            A list of dictionaries representing the 24-hour change data for each trading pair.
            Each dictionary contains various key-value pairs, such as the trading pair symbol, price change percentage, and other related information.
        """
        async with self.session.get(self.DAILY_CHANGE_URL) as response:
            data = await response.json()
            return data

    async def get_binance_futures_symbols(self) -> List[str]:
        """
        Retrieves a list of Binance Futures trading pair symbols from the Binance API.

        Returns:
            A list of strings representing the symbols of Binance Futures trading pairs.
        """
        async with self.session.get(self.EXCHANGE_INFO_URL) as response:
            data = await response.json()
            return [item['symbol'] for item in data['symbols']]

    async def get_top_gainers_and_losers(self, top_n: int = 5) -> Tuple[List[str], List[str]]:
        """
        Retrieves the top gainers and losers among Binance Futures trading pairs based on their 24-hour change percentage.

        Args:
            top_n (int, optional): The number of top gainers and losers to retrieve. Default is 5.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing two lists. 
            The first list represents the symbols of the top gainers among Binance Futures trading pairs. 
            The second list represents the symbols of the top losers among Binance Futures trading pairs.
        """
        futures_symbols = await self.get_binance_futures_symbols()
        data = await self.get_24hr_change_all()
        # Filter the data to include only Binance Futures trading pairs
        data = [item for item in data if item['symbol'] in futures_symbols and 'USDT' in item['symbol']]
        sorted_data = sorted(data, key=lambda x: float(x['priceChangePercent']), reverse=True)
        top_gainers = [x['symbol'] for x in sorted_data[:top_n]]
        top_losers = [x['symbol'] for x in sorted_data[-top_n:]]
        return top_gainers, top_losers

    async def fetch_binance_funding_rate(self, pair: str) -> Optional[float]:
        """
        Retrieves the funding rate of a trading pair from the Binance API.

        Args:
            pair (str): The trading pair for which the funding rate needs to be retrieved.

        Returns:
            Optional[float]: The funding rate of the trading pair as a float, multiplied by 100, if available in the response data.
            None if the funding rate cannot be retrieved or converted.
        """
        for _ in range(3):  # Retry up to 3 times
            try:
                async with self.session.get(self.FUNDING_URL, params={"symbol": pair}) as response:
                    data = await response.json()
                    if "lastFundingRate" in data:
                        return float(data.get("lastFundingRate")) * 100
                    else:
                        return None  # or some other default value
            except aiohttp.client_exceptions.ClientOSError as e:
                await asyncio.sleep(1)  # Wait for 1 second before retrying
        return None  # Return None if all retries fail

    async def fetch_all_funding_rates(self) -> Dict[str, float]:
        """
        Retrieves the funding rates for all trading pairs from the Binance API.

        Returns:
            A dictionary where the keys are the trading pair symbols and the values are the corresponding funding rates as floats.
        """
        async with self.session.get(self.FUNDING_URL) as response:
            data = await response.json()
            return {item["symbol"]: float(item.get("lastFundingRate", 0)) * 100 for item in data}

    async def fetch_top_funded_pairs(self, top_n: int = 5) -> Tuple[List[str], List[str]]:
        """
        Retrieve the top shorted and longed trading pairs based on their funding rates.

        Args:
            top_n (int, optional): The number of top shorted and longed trading pairs to retrieve. Default is 5.

        Returns:
            Tuple[List[str], List[str]]: A tuple containing two lists. The first list represents the symbols of the top shorted trading pairs, and the second list represents the symbols of the top longed trading pairs.
        """
        funding_rates = await self.fetch_all_funding_rates()
        sorted_pairs = [x for x in sorted(funding_rates.items(), key=lambda item: item[1]) if 'USDT' in x[0]]
        top_shorted_pairs = [pair for pair, _ in sorted_pairs[:top_n]]
        top_longed_pairs = [pair for pair, _ in sorted_pairs[-top_n:]]
        return top_shorted_pairs, top_longed_pairs

    async def fetch_pair_data(self, **pair_lists: Dict[str, List[str]]) -> Dict[str, List[Tuple[str, float, float, float]]]:
        """
        Retrieves price, funding rate, and 24-hour change data for multiple trading pairs from the Binance API.

        Args:
            pair_lists: A dictionary where the keys are the names of the pair lists and the values are lists of trading pair symbols.

        Returns:
            A dictionary where the keys are the names of the pair lists and the values are lists of tuples containing the trading pair symbol, price, funding rate, and 24-hour change.
            The total count of trading pairs, including duplicates.
        """
        tasks = []
        pair_to_list = {}
        list_names = set()
        pairs_names = []
        seen = set()
        dups = 0
        for list_name, pair_list in pair_lists.items():
            list_names.add(list_name)
            for pair in pair_list:
                pair_to_list[pair] = pair_to_list.get(pair, []) + [list_name]
                if pair in seen:
                    dups += 1
                    continue
                tasks.append(self.get_price(pair))
                tasks.append(self.fetch_binance_funding_rate(pair))
                tasks.append(self.get_24hr_change(pair))
                seen.add(pair)
                pairs_names.append(pair)

        results = await asyncio.gather(*tasks)

        data = {list_name: [] for list_name in list_names}
        for j in range(0, len(results), 3):
            price = results[j]
            funding_rate = results[j+1]
            change_24hr = results[j+2]
            pair = pairs_names[j//3]
            list_names = pair_to_list[pair]
            for l_name in list_names:
                data[l_name].append((pair, price, funding_rate, change_24hr))

        return data, len(pairs_names) + dups