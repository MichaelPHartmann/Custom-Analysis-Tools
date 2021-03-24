import os
import datetime

from FinMesh.iex import stock

class CairoStockAnalysis:
    def __init__(self):
        self.tickers = []
        self.tickerfile = ''
        self.resultfile = ''

    def csv_to_tickers(tickerCSV):
        with open(tickerCSV, 'r') as c:
            self.tickerfile = tickerCSV
            lines = c.readlines()
            for line in lines:
                tickers = line.split(',')
                if len(tickers) == 0:
                    pass
                else:
                    for tick in tickers:
                        self.tickers.append(tick)

    def list_to_tickers(tickerList):
        for tick in tickers:
            self.tickers.append(tick)

    def find_cairo_value(self, ticker):
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

        # Package results as a list
        result = [ticker, company_name, p, cash_price, inventory_price, cash_inventory_price, tangible_price, current_price, asset_price]

        return result

    def write_cairo_to_csv(self, tickers):
        newfile = self.tickerfile + '_cairo.csv'
        self.resultfile = newfile
        with open(newfile, 'w+') as s:
            s.write('Ticker, Company Name, Price, cash_price, inventory_price, cash_inventory_price, tangible_price, current_price, asset_price\n')
            for ticker in tickers:
                t = ticker.rstrip('\n')
                try:
                    # Make all the entries strings so they can be joined and written as one piece
                    map_result = map(str, find_cairo_value(t))
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

    def update_cairo_csv(self):
        with open(self.resultfile, 'r+') as s:
            with open('Cairo-Data/cairo-temp.csv', 'w+') as temp:
                lines = source.readlines()
                header_line = lines[0]
                data_lines = lines[1:]
                newlines_to_write = []
                newlines_to_write.append(header_line)
                for line in data_lines:
                    line_entries = line.split(',')

                    # Update price
                    price = stock.price(line_entries[0])
                    line_entries[2] = price

                    # Turn the list into strings and join the updated string
                    unjoined_result = map(str, line_entries)
                    result = ','.join(unjoined_result)
                    result = result + '\n'
                    temp.write(result)

        os.remove(self.resultfile)
        os.rename('Cairo-Data/cairo-temp.csv', self.resultfile)

    def sort_cairo_csv(self):
        with open(self.resultfile, 'r') as source:
            date = str(datetime.date.today())
            newfile = self.resultfile.strip('.csv') + f'_sorted_{date}.csv'
            with open(newfile, 'w+') as sort:
                lines = source.readlines()
                header_line = lines[0]
                data_lines = lines[1:]
                sort.write(header_line)
                for line in data_lines:
                    line_entries = line.split(',')
                    # Need this try statement to end the loop when it reaches the end of the document
                    try:
                        # Check cash, current, and asset deltas
                        price = float(line_entries[2])
                        if float(line_entries[3]) > price or float(line_entries[7]) > price or float(line_entries[8]) > price:
                            result = ','.join(line_entries)
                            sort.write(result)
                        else:
                            pass
                    except IndexError:
                        pass



def find_cairo_value(ticker):
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

    # Package results as a list
    result = [ticker, company_name, p, cash_price, inventory_price, cash_inventory_price, tangible_price, current_price, asset_price]

    return result

def write_cairo_to_csv(ticker_file):
    newfile = tickerfile + '_cairo.csv'
    with open(ticker_file, 'r') as nyse:
        with open(newfile, 'w+') as s:
                tickers = nyse.readlines()
                s.write('Ticker, Company Name, Price, cash_price, inventory_price, cash_inventory_price, tangible_price, current_price, asset_price\n')
                for ticker in tickers:
                    t = ticker.rstrip('\n')
                    try:
                        # Make all the entries strings so they can be joined and written as one piece
                        map_result = map(str, find_cairo_value(t))
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

def update_cairo_csv(target_file):
    with open(target_file, 'r+') as s:
        with open('Cairo-Data/cairo-temp.csv', 'w+') as temp:
            lines = source.readlines()
            header_line = lines[0]
            data_lines = lines[1:]
            newlines_to_write = []
            newlines_to_write.append(header_line)
            for line in data_lines:
                line_entries = line.split(',')

                # Update price
                price = stock.price(line_entries[0])
                line_entries[2] = price

                # Turn the list into strings and join the updated string
                unjoined_result = map(str, line_entries)
                result = ','.join(unjoined_result)
                result = result + '\n'
                temp.write(result)

    os.remove(target_file)
    os.rename('Cairo-Data/cairo-temp.csv', target_file)

def sort_cairo_csv(target_file):
    with open(target_file, 'r') as source:
        date = str(datetime.date.today())
        newfile = target_file.strip('.csv') + f'_sorted_{date}.csv'
        with open(newfile, 'w+') as sort:
            lines = source.readlines()
            header_line = lines[0]
            data_lines = lines[1:]
            sort.write(header_line)
            for line in data_lines:
                line_entries = line.split(',')
                # Need this try statement to end the loop when it reaches the end of the document
                try:
                    # Check cash, current, and asset deltas
                    price = float(line_entries[2])
                    if float(line_entries[3]) > price or float(line_entries[7]) > price or float(line_entries[8]) > price:
                        result = ','.join(line_entries)
                        sort.write(result)
                    else:
                        pass
                except IndexError:
                    pass
