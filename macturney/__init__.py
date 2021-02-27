import os

from FinMesh.iex import stock


def find_macturney_value(ticker):
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

def write_macturney_to_csv(ticker_file):
    newfile = tickerfile + '_MacTurney.csv'
    with open(ticker_file, 'r') as nyse:
        with open(newfile, 'w+') as s:
                tickers = nyse.readlines()
                s.write('Ticker, Company Name, Price, cash_price, cash_delta, inventory_price, cash_inventory_price, tangible_price, current_price, current_delta, asset_price, asset_delta\n')
                for ticker in tickers:
                    t = ticker.rstrip('\n')
                    try:
                        # Make all the entries strings so they can be joined and written as one piece
                        map_result = map(str, find_macturney_value(t))
                        unfiltered_result = list(map_result)

                        # Check for comma errors in company names and pop them if they exist
                        sample = unfiltered_result[2]
                        try:
                            sample = float(sample)
                        except ValueError:
                            unfiltered_result.pop(2)

                        # Join the now-filtered list so it is ready to write to the universal csv file
                        result = ','.join(unfiltered_result)
                        s.write(result + '\n')

                    except BaseException:
                        s.write('')

def update_macturney_csv(target_file):
    with open(target_file, 'r+') as s:
        with open('MT-temp.csv', 'w+') as temp:
            lines = s.readlines()[1:]
            newlines_to_write = []
            for index, line in enumerate(lines):
                line_entries = line.split(',')
                # Update price
                price = stock.price(line_entries[0])
                line_entries[2] = price
                # Update cash_delta, current_delta, and asset_delta
                cash_delta = float(line_entries[3]) - price
                line_entries[4] = cash_delta
                current_delta = float(line_entries[8]) - price
                line_entries[9] = current_delta
                asset_delta = float(line_entries[10]) - price
                line_entries[11] = asset_delta
                unjoined_result = map(str, line_entries)
                result = ','.join(unjoined_result)
                result = result + '\n'
                temp.write(result)

    os.remove('NYSE-MacTurney.csv')
    os.rename('MT-temp.csv', target_file)

def sort_macturney_csv():
    pass
