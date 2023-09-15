# Binance Futures Data Fetcher

This project is a Python application that fetches and displays data from the Binance Futures API. It retrieves price data, 24-hour change data, funding rates, and other information related to Binance Futures trading pairs.

## Installation

1. Clone the repository:
git clone https://github.com/rtuchman/binance-futures-data-fetcher.git

2. Navigate to the project directory:
cd binance-futures-data-fetcher

3. Install the required Python packages:
pip install -r requirements.txt


## Usage

Run the `main.py` script:
python main.py


## Output

The script will print the following data to the console:

- Price, funding rate, and 24-hour change for a list of trading pairs
- Top shorted and longed trading pairs based on funding rates
- Top gainers and losers among Binance Futures trading pairs

Example output:

--- My Pairs Information ---
  Pair     | Price      | % Funding  | % 24h Change
BTCUSDT    | 26357.20   | 0.0013     | -0.28     
ETHUSDT    | 1619.57    | -0.0019    | -0.132    

--- Top shorted pairs ---
  Pair     | Price      | % Funding  | % 24h Change
TRBUSDT    | 33.744     | -2.5       | 8.787     
BLZUSDT    | 0.15678    | -0.5124    | 1.611     
SPELLUSDT  | 0.0004965  | -0.2341    | 14.599    
DEFIUSDT   | 479.0      | -0.2128    | 0.0       
AXSUSDT    | 4.72000    | -0.0873    | -4.444    

--- Top longed pairs ---
  Pair     | Price      | % Funding  | % 24h Change
SXPUSDT    | 0.2532     | 0.01       | -0.039    
XEMUSDT    | 0.0251     | 0.01       | 1.456     
ZILUSDT    | 0.01602    | 0.01       | -0.558    
DYDXUSDT   | 1.945      | 0.01       | 0.673     
CTSIUSDT   | 0.1247     | 0.01       | -1.422    

--- Top Gainers ---
  Pair     | Price      | % Funding  | % 24h Change
SPELLUSDT  | 0.0004965  | -0.2341    | 14.599    
OXTUSDT    | 0.0804100  | 0.01       | 30.519    
STORJUSDT  | 0.3498     | 0.008      | 11.675    
WLDUSDT    | 1.1078000  | -0.01      | 10.239    
KEYUSDT    | 0.0058100  | 0.01       | 10.859    

--- Top Losers ---
  Pair     | Price      | % Funding  | % 24h Change
AXSUSDT    | 4.72000    | -0.0873    | -4.444    
AGLDUSDT   | 0.5556000  | 0.01       | -4.467    
UNFIUSDT   | 8.500      | -0.01      | -5.346    
OGNUSDT    | 0.0933     | 0.01       | -5.567    
APEUSDT    | 1.0980     | -0.0031    | -6.463    

Funding countdown: 03:10:01 


## License

This project is licensed under the terms of the MIT license.