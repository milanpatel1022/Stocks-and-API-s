#Milan Patel 47449770

import download_api_info
import indicators
import signal_strategies

def run_program():
    '''Runs through program, collecting all needed data from different modules and eventually printing it out'''
    stock = what_stock()
    num_days = num_trading_days()
    analysis_combination = indicator_and_signal()
    info = download_api_info.info_to_download(num_days)
    url = download_api_info.build_search_url(stock, info)
    valid_stock = download_api_info.try_url(url)
    if valid_stock == True:
        company_name = download_api_info.get_company_name(stock)
        total_shares = download_api_info.get_total_existing_shares(stock)
        result = download_api_info.stock_info(url)
        lst_of_days = days_with_data(result, num_days)
        indicators = what_indicator(analysis_combination, result, num_days, lst_of_days)
        signals, indicators = what_signal(analysis_combination, indicators, result, num_days)
        print_info(result, num_days, stock, company_name, total_shares, lst_of_days, indicators, signals)


def what_stock() -> str:
    '''Get stock symbol from input'''
    stock = input()
    return stock

def num_trading_days() -> int:
    '''Get number of days to print info out for'''
    num_days = input()
    try:
        int(num_days)
    except:
        print('This line must be a positive integer, the number of trading days.')
    else:
        return int(num_days)
        

def indicator_and_signal() -> str:
    '''Get what indicator and signal is to be used from input'''
    analysis_combination = input()
    return analysis_combination



def what_indicator(analysis_combination: str, result: dict, num_days: int, lst_of_days: list) -> list:
    '''According to input calls respective function to obtain indicator values'''
    analysis = analysis_combination.split(' ')
    indicator = analysis[0]
    if indicator == 'TR':
        return _get_true_range(analysis, result, num_days)
    if indicator == 'DP' or indicator == 'DV':
        return _get_directional_indicator(analysis, result, num_days)
    if indicator == 'MP' or indicator == 'MV':
        return _get_simple_moving_average(analysis, result, num_days, lst_of_days)



def what_signal(analysis_combination: str, indicators: list, result: dict, num_days: int) -> tuple:
    '''According to input calls, creates object of respective class and obtains signals using the obtained indicator values'''
    analysis = analysis_combination.split(' ')
    if analysis[0] == 'TR':
        get_signals = signal_strategies.TrueRangeSignal()
        signals, formatted_indicators = get_signals.tr_signal(analysis, indicators)
        return signals, formatted_indicators
    
    elif analysis[0] == 'MP' or analysis[0] == 'MV':
        get_signals = signal_strategies.SMASignal()
        if analysis[0] == 'MP':
            signals, formatted_indicators = get_signals.sma_prices_signal(analysis, indicators, result, num_days)
            return signals, formatted_indicators
        elif analysis[0] == 'MV':
            signals, formatted_indicators = get_signals.sma_volumes_signal(analysis, indicators, result, num_days)
            return signals, formatted_indicators
    
    elif analysis[0] == 'DP' or analysis[0] == 'DV':
        get_signals = signal_strategies.DirectionalSignal()
        signals, formatted_indicators = get_signals.ds_price_or_volume(analysis, indicators)
        return signals, formatted_indicators



def _get_true_range(analysis: list, result: dict, num_days: int) -> list:
    '''Creates object of the true range class and returns indicator values'''
    tr = indicators.TrueRangeIndicator()
    range_of_prices = tr.true_range(result, num_days)
    return range_of_prices


def _get_simple_moving_average(analysis: list, result: dict, num_days: int, lst_of_days: list) -> list:
    '''Creates object of the simple moving average class and returns indicator values'''
    sma = indicators.SimpleMovingAverageIndicator()
    days = int(analysis[1])
    if analysis[0] == 'MP':
        average = sma.sma_closing_prices(result, num_days, int(days))
        return average
    elif analysis[0] == 'MV':
        average = sma.sma_volume(result, num_days, int(days))
    return average


def _get_directional_indicator(analysis: list, result: dict, num_days: int) -> list:
    '''Creates object of the directional indicator class and returns indicator values'''
    indicator = indicators.DirectionalIndicator()
    if analysis[0] == 'DP':
        di = indicator.di_closing_prices(result, num_days, int(analysis[1]))
        return di
    elif analysis[0] == 'DV':
        di = indicator.di_volumes(result, num_days, int(analysis[1]))
        return di
    


def days_with_data(search_result: dict, num_days: int) -> list:
    '''Gets list of all the dates'''
    lst_of_days = [ ]
    for item in search_result[-num_days:]:
        lst_of_days.append(item['date'])
    return lst_of_days



def _header() -> None:
    '''Prints the header for the table'''
    print(f"{'Date'}\t{'Open'}\t{'High'}\t{'Low'}\t{'Close'}\t{'Volume'}\t{'Indicator'}\t{'Buy?'}\t{'Sell?'}")


def print_info(search_result: dict, num_days: int, stock: str, company_name: str, total_shares: str, lst_of_days: list, indicators: list, signals: list) -> None:
    '''Prints all the obtained stock info in tab delimited format'''
    print(stock)
    print(company_name)
    print(total_shares)
    _header()
    #subtract number of days you need from the end of the list to get the latest # of days
    for item in search_result[-num_days:]:
        result_string = ''
        result_string += (f"{item['date']}\t{format(item['open'], '.4f')}\t{format(item['high'], '.4f')}\t{format(item['low'], '.4f')}\t{format(item['close'], '.4f')}\t{item['volume']}\t")
        result_string += (f"{indicators[0]}")
        if len(indicators) != 1:
            indicators.pop(0)
        try:
            result_string += (f"{signals[0]}")
            signals.pop(0)
        except:
            pass
        print(result_string)        
    print('Data provided for free by IEX')
    print("View IEX's Terms of Use")
    print("https://iextrading.com/api-exhibit-a/")

if __name__ == '__main__':
    run_program()
