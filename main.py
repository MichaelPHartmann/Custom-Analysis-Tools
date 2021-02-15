from FinMesh.iex import stock

def find_value(ticker):
    ks = stock.key_stats(ticker)
    bs = stock.balance_sheet(ticker)['balancesheet'][0]
    p = stock.price(ticker)

    # Bring in raw data from IEX key stats data
    company_name = ks['companyName']
    shares_outstanding = ks['sharesOutstanding']

    # Bring in raw data from IEX balance sheet data
    current_cash = bs['currentCash']
    inventory = bs['inventory']
    current_assets = bs['currentAssets']
    current_liabilities = bs['totalCurrentLiabilities']
    net_tangible_assets = bs['netTangibleAssets']
    total_assets = bs['totalAssets']
    total_liabilities = bs['totalLiabilities']

    # Various measures of share price
    cash_price = current_cash / shares_outstanding
    inventory_price = inventory / shares_outstanding
    cash_inventory_price = (current_cash + inventory) / shares_outstanding
    tangible_price = net_tangible_assets / shares_outstanding
    current_price = (current_assets - current_liabilities) / shares_outstanding
    asset_price = (total_assets - total_liabilities) / shares_outstanding
    cash_delta = cash_price - p
    current_delta = current_price - p
    asset_delta = asset_price - p

    # Package results as a list
    result = [ticker, company_name, p, cash_price, cash_delta, inventory_price, cash_inventory_price, tangible_price, current_price, current_delta, asset_price, asset_delta]

    return result

def write_screen_to_csv():
    with open('NYSE-Listed.csv', 'r') as nyse:
        with open('NYSE-Value.csv', 'w+') as v:
            tickers = nyse.readlines()
            v.write('Ticker, Company Name, Price, cash_price, cash_delta, inventory_price, cash_inventory_price, tangible_price, current_price, current_delta, asset_price, asset_delta\n')
            for ticker in tickers:
                t = ticker.rstrip('\n')
                try:
                    result = map(str, find_value(t))
                    result = ','.join(result)
                    v.write(result + '\n')

                except BaseException:
                    v.write('')

def clean_value_csv():
    with open('NYSE-Value.csv', 'r') as nyse:
        with open('NYSE-Value-Clean.csv', 'w+') as clean:
            lines = nyse.readlines()
            clean.write(lines[0])
            for line in lines[1:]:
                linelist = line.split(',')
                sample = linelist[2].strip(',')
                try:
                    sample = float(sample)
                except ValueError:
                    linelist.pop(2)
                result = ','.join(linelist)
                clean.write(result)

clean_value_csv()
