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
BTCUSDT    | 26428.20   | 0.0007     | -0.172    
ETHUSDT    | 1622.02    | -0.0034    | -0.239    

--- Top shorted pairs ---
  Pair     | Price      | % Funding  | % 24h Change
TRBUSDT    | 32.983     | -2.5       | 3.607     
BLZUSDT    | 0.15764    | -0.4855    | 2.249     
SPELLUSDT  | 0.0005074  | -0.2719    | 17.059    
DEFIUSDT   | 480.4      | -0.1928    | 0.0       
AXSUSDT    | 4.73000    | -0.0943    | 8.467     

--- Top longed pairs ---
  Pair     | Price      | % Funding  | % 24h Change
AMBUSDT    | 0.0080040  | 0.01       | 1.264     
SXPUSDT    | 0.2541     | 0.01       | 0.593     
XEMUSDT    | 0.0251     | 0.01       | 1.746     
ZILUSDT    | 0.01603    | 0.01       | -0.187    
CTSIUSDT   | 0.1248     | 0.01       | -1.108    

--- Top Gainers ---
  Pair     | Price      | % Funding  | % 24h Change
SPELLUSDT  | 0.0005074  | -0.2719    | 17.059    
OXTUSDT    | 0.0817500  | 0.01       | 32.577    
WLDUSDT    | 1.1166000  | -0.0087    | 10.803    
STORJUSDT  | 0.3502     | 0.008      | 10.013    
NMRUSDT    | 13.340000  | 0.0061     | 8.11      

--- Top Losers ---
  Pair     | Price      | % Funding  | % 24h Change
GALUSDT    | 1.23920    | 0.01       | -3.804    
AGLDUSDT   | 0.5560000  | 0.01       | -5.442    
UNFIUSDT   | 8.456      | -0.0133    | -5.674    
APEUSDT    | 1.1000     | 0.0002     | -5.892    
OGNUSDT    | 0.0941     | 0.01       | -10.551   

Funding countdown: 03:38:18 


## License

This project is licensed under the terms of the MIT license.