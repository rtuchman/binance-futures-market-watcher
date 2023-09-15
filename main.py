import aiohttp
import asyncio
import argparse
from datetime import datetime
from typing import List

from utils.binance_api_utils import BinanceAPI
from utils import date_utils, print_utils



async def main(trading_pairs: List[str]) -> None:
    async with aiohttp.ClientSession() as session:
        binance_api = BinanceAPI(session)
        i = 0
        while True:
            if i%500 == 0:
                top_shorted_pairs, top_longed_pairs = await binance_api.fetch_top_funded_pairs(top_n=5)
                top_gainers, top_losers = await binance_api.get_top_gainers_and_losers(top_n=5)

            next_funding_time = date_utils.get_next_funding_time()
            countdown = date_utils.format_timedelta(next_funding_time - datetime.utcnow())

            if i%20 == 0:
                data, num_pairs = await binance_api.fetch_pair_data(trading_pairs=trading_pairs, 
                                                                    top_shorted_pairs=top_shorted_pairs, 
                                                                    top_longed_pairs=top_longed_pairs,
                                                                    top_gainers=top_gainers,
                                                                    top_losers=top_losers)
                
            await print_utils.print_data(data, countdown, num_pairs)  

            i += 1
            await asyncio.sleep(0.05)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch and print futures price and funding rate.')
    parser.add_argument('trading_pairs', metavar='PAIR', type=str, nargs='*', 
                        help='a trading pair to fetch data for (e.g. BTCUSDT)')
    parser.add_argument('--no-default-pairs', dest='default_pairs', action='store_false',
                        help='do not automatically print BTCUSDT and ETHUSDT as the first two pairs')
    parser.add_argument('--file', dest='file', type=str, 
                    help='path to a text file containing trading pairs')
    parser.set_defaults(default_pairs=True)

    # Parse the arguments
    args = parser.parse_args()

    # If a file is provided, read the trading pairs from the file
    if args.file:
        with open(args.file, 'r') as f:
            trading_pairs = [line.strip().upper() for line in f]
    else:
        trading_pairs = [pair.upper() for pair in args.trading_pairs]

    trading_pairs.sort()

    # If default pairs are enabled, add BTCUSDT and ETHUSDT to the trading pairs
    if args.default_pairs:
        for pair in ['ETHUSDT', 'BTCUSDT']:
            if pair not in trading_pairs:
                trading_pairs.insert(0, pair)

    # Run the main function
    try:
        asyncio.run(main(trading_pairs))
    except KeyboardInterrupt:
        print("\nExiting...")