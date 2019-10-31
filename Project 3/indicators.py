#Milan Patel 47449770

class TrueRangeIndicator:
    def __init__(self):
        self._list_of_indicators = ['']
        
    def true_range(self, stock_info: dict, num_days: int) -> list:
        '''Finds true range from the set of days provided and returns list of indicator values'''
        previous_close = stock_info[-num_days]['close']
        for dictionary in stock_info[-num_days+1:]:
            if dictionary['low'] > previous_close:
                tr = float((((dictionary['high'] - previous_close) / previous_close) * 100))
                previous_close = dictionary['close']
            elif dictionary['high'] < previous_close:
                tr = float((((previous_close - dictionary['low']) / previous_close) * 100))
                previous_close = dictionary['close']
            else:
                tr = float((((dictionary['high'] - dictionary['low']) / previous_close) * 100))
                previous_close = dictionary['close']
            self._list_of_indicators.append(tr)

        return self._list_of_indicators
                                            
            

class SimpleMovingAverageIndicator:
    def __init__(self):
        self._averages = []
        self._indicators = []
        self._close_or_volume_values = []
        
    def sma_closing_prices(self, stock_info: dict, num_days: int, days: int) -> list:
        '''Gets simple moving average of closing prices by looping through the valid days'''
        for item in stock_info[-num_days:(-num_days+days-1)]:
            self._indicators.append('')
            self._close_or_volume_values.append(item['close'])
            
        for item in stock_info[-num_days+days-1:]:
            total = sum(self._close_or_volume_values) + item['close']
            average = total / days
            self._averages.append(average)
            self._close_or_volume_values.append(item['close'])
            self._close_or_volume_values.pop(0)
            
        for item in self._averages:
            self._indicators.append(item)

        return self._indicators
    
    def sma_volume(self, stock_info: dict, num_days: int, days: int) -> list:
        '''Gets simple moving average of volumes by looping through the valid days'''
        for item in stock_info[-num_days:(-num_days+days-1)]:
            self._indicators.append('')
            self._close_or_volume_values.append(item['volume'])
            
        for item in stock_info[-num_days+days-1:]:
            total = sum(self._close_or_volume_values) + item['volume']
            average = total / days
            self._averages.append(average)
            self._close_or_volume_values.append(item['volume'])
            self._close_or_volume_values.pop(0)
            
        for item in self._averages:
            self._indicators.append(item)

        return self._indicators



class DirectionalIndicator:
    def __init__(self):
        self._close_or_volume_values = []
        self._up_or_down_tracker = [0]
        self._indicators = []
        
    def di_closing_prices(self, stock_info: dict, num_days: int, days: int) -> list:
        '''Calculates directional indicator of closing prices and returns a list of them'''
        for item in stock_info[-num_days:]:
            self._close_or_volume_values.append(item['close'])

        #this for loop stores 1's and -1's if price went up or down from previous day
        for i in range(1, len(self._close_or_volume_values)):
            if self._close_or_volume_values[i] < self._close_or_volume_values[i-1]:
                self._up_or_down_tracker.append(-1)

            elif self._close_or_volume_values[i] > self._close_or_volume_values[i-1]:
                self._up_or_down_tracker.append(1)
                
        #sums up the last N up_or_down values to get the indicator at a certain day
        for i in range(0, len(self._up_or_down_tracker)):
            if i <= days:
                self._indicators.append(sum(self._up_or_down_tracker[0:i+1]))
            elif i > days:
                last_N_days = sum(self._up_or_down_tracker[i-days+1:i+1])
                self._indicators.append(last_N_days)
   
        return self._indicators
        
            

    def di_volumes(self, stock_info: dict, num_days: int, days: int) -> list:
        '''Calculates directional indicator of volumes and returns a list of them'''
        for item in stock_info[-num_days:]:
            self._close_or_volume_values.append(item['volume'])
            
        for i in range(1, len(self._close_or_volume_values)):
            if self._close_or_volume_values[i] < self._close_or_volume_values[i-1]:
                self._up_or_down_tracker.append(-1)
                
            elif self._close_or_volume_values[i] > self._close_or_volume_values[i-1]:
                self._up_or_down_tracker.append(1)

        
        for i in range(0, len(self._up_or_down_tracker)):
            if i <= days:
                self._indicators.append(sum(self._up_or_down_tracker[0:i+1]))
            elif i > days:
                last_N_days = sum(self._up_or_down_tracker[i-days+1:i+1])
                self._indicators.append(last_N_days)
          
        return self._indicators
        
        
