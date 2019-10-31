import locale
import pathlib
import queue
import sys
import subprocess
import threading
import time
import traceback



class TextProcessReadTimeout(Exception):
    pass



class TextProcess:
    _READ_INTERVAL_IN_SECONDS = 0.025


    def __init__(self, args: [str], working_directory: str):
        self._process = subprocess.Popen(
            args, cwd = working_directory, bufsize = 0,
            stdin = subprocess.PIPE, stdout = subprocess.PIPE,
            stderr = subprocess.STDOUT)

        self._stdout_read_trigger = queue.Queue()
        self._stdout_buffer = queue.Queue()

        self._stdout_thread = threading.Thread(
            target = self._stdout_read_loop, daemon = True)

        self._stdout_thread.start()


    def __enter__(self):
        return self


    def __exit__(self, tr, exc, val):
        self.close()


    def close(self):
        self._stdout_read_trigger.put('stop')
        self._process.terminate()
        self._process.wait()
        self._process.stdout.close()
        self._process.stdin.close()


    def write_line(self, line: str) -> None:
        try:
            self._process.stdin.write((line + '\n').encode(locale.getpreferredencoding(False)))
            self._process.stdin.flush()

        except OSError:
            pass


    def read_line(self, timeout: float = None) -> str or None:
        self._stdout_read_trigger.put('read')
        
        sleep_time = 0

        while timeout == None or sleep_time < timeout:
            try:
                next_result = self._stdout_buffer.get_nowait()

                if next_result == None:
                    return None
                elif isinstance(next_result, Exception):
                    raise next_result
                else:
                    line = next_result.decode(locale.getpreferredencoding(False))

                    if line.endswith('\r\n'):
                        line = line[:-2]
                    elif line.endswith('\n'):
                        line = line[:-1]

                    return line

            except queue.Empty:
                time.sleep(TextProcess._READ_INTERVAL_IN_SECONDS)
                sleep_time += TextProcess._READ_INTERVAL_IN_SECONDS

        raise TextProcessReadTimeout()


    def _stdout_read_loop(self):
        try:
            while self._process.returncode == None:
                if self._stdout_read_trigger.get() == 'read':
                    line = self._process.stdout.readline()

                    if line == b'':
                        self._stdout_buffer.put(None)
                    else:
                        self._stdout_buffer.put(line)
                else:
                    break

        except Exception as e:
            self._stdout_buffer.put(e)



def start_process() -> TextProcess:
    filenames_in_dir = [p.name for p in pathlib.Path.cwd().iterdir() if p.is_file()]

    if not 'project3.py' in filenames_in_dir:
        print_labeled_output(
            'ERROR',
            'Cannot find file "project3.py" in this directory.',
            'Make sure that the sanity checker is in the same directory as the',
            '"project3.py" file that is used to execute your Project #3 solution.',
            'Also, be sure that you\'ve named your "project3.py" file correctly,',
            'noting that capitalization and spacing matter.')

        raise TestFailure()
    
    else:
        cwd = pathlib.Path.cwd()

        return TextProcess([sys.executable, str(cwd / 'project3.py')], cwd)



FORMAT_EMPTY = 0
FORMAT_STR = 1
FORMAT_INT = 2
FORMAT_DECIMAL = 3
FORMAT_DATE = 4



def make_empty_checker():
    def is_empty(field_text: str) -> bool:
        return len(field_text) == 0

    return is_empty



def make_str_checker():
    def is_nonempty_str(field_text: str) -> bool:
        return len(field_text) > 0

    return is_nonempty_str



def make_int_checker():
    def is_int(field_text: str) -> bool:
        return field_text.isdigit()

    return is_int



def make_decimal_checker():
    def is_decimal(field_text: str) -> bool:
        first_dot_pos = field_text.find('.')

        return first_dot_pos != -1 \
            and field_text.find('.', first_dot_pos + 1) == -1 \
            and first_dot_pos + 5 == len(field_text) \
            and field_text[0:first_dot_pos].isdigit() \
            and field_text[(first_dot_pos+1):].isdigit()

    return is_decimal



def make_date_checker():
    def is_date(field_text: str) -> bool:
        first_dash_pos = field_text.find('-')
        second_dash_pos = field_text.find('-', first_dash_pos + 1)

        return len(field_text) == 10 \
            and first_dash_pos == 4 and second_dash_pos == 7 \
            and field_text[0:4].isdigit() and field_text[5:7].isdigit() \
            and field_text[8:10].isdigit()

    return is_date



def make_text_checker(text: str):
    def matches_text(field_text: str):
        return field_text == text

    return matches_text



class OutputFieldRule:
    def __init__(self, checker, requirement):
        self._checker = checker
        self._requirement = requirement


    def check(self, field_text: str) -> bool:
        return self._checker(field_text)


    def get_requirement(self) -> str:
        return self._requirement



def make_rule(rule):
    if type(rule) == int:
        if rule == FORMAT_EMPTY:
            return OutputFieldRule(make_empty_checker(), 'empty')
        elif rule == FORMAT_STR:
            return OutputFieldRule(make_str_checker(), 'non-empty')
        elif rule == FORMAT_INT:
            return OutputFieldRule(make_int_checker(), 'an integer')
        elif rule == FORMAT_DECIMAL:
            return OutputFieldRule(make_decimal_checker(), 'a decimal number (with four digits after the decimal)')
        elif rule == FORMAT_DATE:
            return OutputFieldRule(make_date_checker(), 'a date in YYYY-MM-DD format')
        else:
            raise ValueError(f'passed in an int, but not a recognized format; was {rule}')

    elif type(rule) == str:
        return OutputFieldRule(make_text_checker(rule), f'{repr(rule)}')

    else:
        raise ValueError('passed in neither an int nor a str')
    


class OutputField:
    def __init__(self, rules):
        self._rules = []

        if type(rules) == list:
            self._rules = [make_rule(rule) for rule in rules]
        else:
            self._rules = [make_rule(rules)]


    def validate_field(self, field_text: str) -> None or str:
        for rule in self._rules:
            if rule.check(field_text):
               return None

        requirements = ''

        for i in range(len(self._rules) - 1):
            requirements += self._rules[i].get_requirement() + ', '

        if len(self._rules) > 1:
            requirements += 'or '

        requirements += self._rules[len(self._rules) - 1].get_requirement()

        return requirements



def make_line_rules(fields, count = 1):
    return [[OutputField(field) for field in fields]] * count



TEST_INPUT_LINES = ['AAPL', '15', 'MP 5']

EXPECTED_OUTPUT_LINES = \
    make_line_rules(['AAPL']) + \
    make_line_rules([FORMAT_STR]) + \
    make_line_rules([FORMAT_INT]) + \
    make_line_rules(['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Indicator', 'Buy?', 'Sell?']) + \
    make_line_rules([FORMAT_DATE, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_INT, FORMAT_EMPTY, FORMAT_EMPTY, FORMAT_EMPTY], 4) + \
    make_line_rules([FORMAT_DATE, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_DECIMAL, FORMAT_INT, FORMAT_DECIMAL, [FORMAT_EMPTY, 'BUY', 'SELL'], [FORMAT_EMPTY, 'BUY', 'SELL']], 11) + \
    make_line_rules(['Data provided for free by IEX']) + \
    make_line_rules(['View IEX\'s Terms of Use']) + \
    make_line_rules(['https://iextrading.com/api-exhibit-a/'])

NO_OUTPUT_BEFORE_INPUT_TIMEOUT = 2.0
FIRST_OUTPUT_TIMEOUT = 20.0
REMAINING_OUTPUT_TIMEOUT = 2.0
MAX_OUTPUT_LINES = 999



class TestFailure(Exception):
    pass



def print_labeled_output(label: str, *output_lines: str) -> None:
    for output_line in output_lines:
        print(f'{label:10}|{output_line}')



def expect_no_output(process: TextProcess) -> None:
    try:
        print_labeled_output('WAITING', 'Ensuring your program prints no output before reading inputs...')
        line = process.read_line(NO_OUTPUT_BEFORE_INPUT_TIMEOUT)
        print_labeled_output('OUTPUT', line)
        print_labeled_output('ERROR', 'No output was expected before the program reads input, but your program printed some')
        raise TestFailure()

    except TextProcessReadTimeout:
        pass



def write_input_lines(process: TextProcess, input_lines: [str]) -> None:
    for input_line in input_lines:
        print_labeled_output('INPUT', input_line)
        process.write_line(input_line)



def read_output_lines(process: TextProcess) -> [str]:
    lines = []
    
    while True:
        try:
            timeout = FIRST_OUTPUT_TIMEOUT if len(lines) == 0 else REMAINING_OUTPUT_TIMEOUT

            next_line = process.read_line(timeout)

            if next_line == None:
                break
            else:
                lines.append(next_line.split('\t'))

                if len(lines) == MAX_OUTPUT_LINES:
                    break

        except TextProcessReadTimeout:
            pass

    return lines



def check_output_lines(output_lines: [[str]]):
    failures = 0

    for i in range(len(output_lines)):
        print_labeled_output('OUTPUT', '|'.join(output_lines[i]))
        
        if i >= len(EXPECTED_OUTPUT_LINES):
            print_labeled_output('ERROR', 'No more output lines were expected at this point')
            failures += 1

        expected_output_line = EXPECTED_OUTPUT_LINES[i]

        if len(output_lines[i]) != len(EXPECTED_OUTPUT_LINES[i]):
            print_labeled_output(
                'ERROR',
                f'This line of output was expected to have {len(EXPECTED_OUTPUT_LINES[i])} fields, but had {len(output_lines[i])} instead',
                '(Note that the fields must be delimited by tab characters and not spaces.')

            failures += 1

        for j in range(len(output_lines[i])):
            result = EXPECTED_OUTPUT_LINES[i][j].validate_field(output_lines[i][j])

            if result != None:
                print_labeled_output(
                    'ERROR',
                    f'Field #{j + 1} was expected to be ' + result,
                    f"    but was {repr(output_lines[i][j])} instead'")

                failures += 1

    if failures > 0:
        raise TestFailure()



def run_test() -> None:
    process = None

    try:
        print_labeled_output('STARTING', 'Starting "project3.py"...')
        process = start_process()
        expect_no_output(process)
        write_input_lines(process, TEST_INPUT_LINES)

        print_labeled_output('WAITING', 'Waiting for your program\'s output...')
        output_lines = read_output_lines(process)

        print_labeled_output('CHECKING', 'Checking your program\'s output against expectations...')
        check_output_lines(output_lines)

        print_labeled_output(
            'SUCCEEDED',
            'The sanity checker has succeeded.',
            'Your program meets the formatting requirements for input and output.',
            'Note that this does not necessarily mean the output is correct,',
            'but it does meet that it is formatted properly.')

    except TestFailure:
        print_labeled_output('FAILED', 'The sanity checker has failed, for the reasons described above.')

    finally:
        if process != None:
            process.close()



if __name__ == '__main__':
    run_test()
