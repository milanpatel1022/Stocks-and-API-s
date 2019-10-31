#Milan Patel 47449770

class TrueRangeSignal:
    def __init__(self):
        self._signals = ['\t\t']
        self._formatted_indicators = ['']
        
    def tr_signal(self, analysis: list, indicators: list) -> tuple:
        '''Checks each case and returns list with formatted strings to be printed in main'''
        first_threshold = analysis[1]
        second_threshold = analysis[2]
        first_sign = first_threshold[0]
        first_number = float(first_threshold[1:])
        second_sign = second_threshold[0]
        second_number = float(second_threshold[1:])
        
        if first_sign == '<' and second_sign == '>':
            for indicator in indicators[1:]:
                string = ''
                if indicator < first_number and indicator > second_number:
                    string += '\tBUY\tSELL'
                elif indicator < first_number and indicator < second_number:
                    string += '\tBUY\t'
                elif indicator > first_number and indicator > second_number:
                    string += '\t\tSELL'
                else:
                    string += '\t\t'
                self._signals.append(string)
        
        elif first_sign == '>' and second_sign == '<':
            for indicator in indicators[1:]:
                string = ''
                if indicator > first_number and indicator < second_number:
                    string += '\tBUY\tSELL'
                elif indicator > first_number and indicator > second_number:
                    string += '\tBUY\t'
                elif indicator < first_number and indicator < second_number:
                    string += '\t\tSELL'
                else:
                    string += '\t\t'
                self._signals.append(string)
        
        elif first_sign == '>' and second_sign == '>':
            for indicator in indicators[1:]:
                string = ''
                if indicator > first_number and indicator > second_number:
                    string += '\tBUY\tSELL'
                elif indicator > first_number and indicator < second_number:
                    string += '\tBUY\t'
                elif indicator < first_number and indicator > second_number:
                    string += '\t\tSELL'
                else:
                    string += '\t\t'
                self._signals.append(string)
        
        elif first_sign == '<' and second_sign == '<':
            for indicator in indicators[1:]:
                string = ''
                if indicator < first_number and indicator < second_number:
                    string += '\tBUY\tSELL'
                elif indicator < first_number and indicator > second_number:
                    string += '\tBUY\t'
                elif indicator > first_number and indicator < second_number:
                    string += '\t\tSELL'
                else:
                    string += '\t\t'
                self._signals.append(string)

        for item in indicators[1:]:
            self._formatted_indicators.append(format(item, '.4f'))

        return self._signals, self._formatted_indicators


class SMASignal:
    def __init__(self):
        self._signals = []
        self._close_or_volume_values = []
        self._final_indicators = []
        self._formatted_indicators = []
    
    def sma_prices_signal(self, analysis: list, indicators: list, stock_info: dict, num_days: int) -> tuple:
        '''Calculates simple moving average for closing prices and returns two lists to be printed in main'''
        signal_days = int(analysis[1])

        if num_days < signal_days:
            for i in range(num_days):
                self._formatted_indicators.append('')
                self._signals.append('\t\t')
                return self._signals, self._formatted_indicators
                
        day = 1
        
        for day in range(signal_days-1):
            self._final_indicators.append('')
            
        for day in range(signal_days):
            self._signals.append('\t\t')
            
        del indicators[-num_days:-num_days+signal_days-1]
        
        for item in stock_info[-num_days+signal_days-1:]:
            self._close_or_volume_values.append(item['close'])

        i = 0
        
        for self._close_or_volume_values[i] in self._close_or_volume_values:
            try:
                if self._close_or_volume_values[i+1] > indicators[1] and self._close_or_volume_values[i] < indicators[0]:
                    self._signals.append('\tBUY\t')
                elif self._close_or_volume_values[i+1] < indicators[1] and self._close_or_volume_values[i] > indicators[0]:
                    self._signals.append('\t\tSELL')
                else:
                    self._signals.append('\t\t')
                i += 1
                self._final_indicators.append(indicators.pop(0))
            except:
                self._final_indicators.append(indicators.pop(0))
                
        for indicator in self._final_indicators:
            try:
                self._formatted_indicators.append(format(indicator, '.4f'))
            except:
                self._formatted_indicators.append(indicator)

        return self._signals, self._formatted_indicators
    
    
    def sma_volumes_signal(self, analysis: list, indicators: list, stock_info: dict, num_days: int) -> tuple:
        '''Calculates simple moving average of volumes and returns two lists of values to be printed in main'''
        signal_days = int(analysis[1])

        if num_days < signal_days:
            for i in range(num_days):
                self._formatted_indicators.append('')
                self._signals.append('\t\t')
                return self._signals, self._formatted_indicators

        day = 1

        for day in range(signal_days-1):
            self._final_indicators.append('')
            
        for day in range(signal_days):
            self._signals.append('\t\t')
        
        del indicators[-num_days:-num_days+signal_days-1]
        
        for item in stock_info[-num_days+signal_days-1:]:
            self._close_or_volume_values.append(item['volume'])

        i = 0
        
        for self._close_or_volume_values[i] in self._close_or_volume_values:
            try:
                if self._close_or_volume_values[i+1] > indicators[1] and self._close_or_volume_values[i] < indicators[0]:
                    self._signals.append('\tBUY\t')
                elif self._close_or_volume_values[i+1] < indicators[1] and self._close_or_volume_values[i] > indicators[0]:
                    self._signals.append('\t\tSELL')
                else:
                    self._signals.append('\t\t')
                i += 1
                self._final_indicators.append(indicators.pop(0))
            except:
                self._final_indicators.append(indicators.pop(0))

        for indicator in self._final_indicators:
            try:
                self._formatted_indicators.append(format(indicator, '.4f'))
            except:
                self._formatted_indicators.append(indicator)
        return self._signals, self._formatted_indicators



class DirectionalSignal():
    def __init__(self):
        self._signals = ['\t\t']
        self._formatted_indicators = []
        self._buy_value = 0
        self._sell_value = 0
    '''Calculates directional indicator for closing prices and volumes'''
    
    def ds_price_or_volume(self, analysis: list, indicators: list) -> tuple:
        buy_thresh = analysis[2]
        sell_thresh = analysis[3]
        
        if buy_thresh[0] == '-':
            self._buy_value = int('-%s' %buy_thresh[1:])

        if sell_thresh[0] == '-':
            self._sell_value = int('-%s' %sell_thresh[1:])

        if buy_thresh[0] == '+':
            self._buy_value = int(buy_thresh[1:])

        if sell_thresh[0] == '+':
            self._sell_value = int(sell_thresh[1:])
            
        if len(buy_thresh) == 1:
            self._buy_value = 0
            
        if len(sell_thresh) == 1:
            self._sell_value = 0


        for i in range(1, len(indicators)):
            if indicators[i] > self._buy_value and indicators[i-1] <= self._buy_value:
                self._signals.append('\tBUY\t')
            elif indicators[i] < self._sell_value and indicators[i-1] >= self._sell_value:
                self._signals.append('\t\tSELL')
            else:
                self._signals.append('\t\t')

        for indicator in indicators:
            if indicator > 0:
                self._formatted_indicators.append('+%d' %indicator)
            else:
                self._formatted_indicators.append(indicator)

        return self._signals, self._formatted_indicators
        





