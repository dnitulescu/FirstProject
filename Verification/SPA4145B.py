import re

from Verification.InstrumentClass import VInstrument


class SPA4145B(VInstrument):
    source_type = 'voltage'
    channel = '4'
    source_range = '3'
    value = '1'
    compliance = '0.1'
    pattern=re.compile('[-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?')   # regulat expresion to recognize string of numbers

    def initialize(self):
        print(self.write_to_gpib('US;'))  # set user mode
        print(self.write_to_gpib('IT1 CA1 BC;'))  # set measurment integration time , auot calib  , data buffer clear
        print(self.query('*IDN?'))  # get name

    def close(self):
        self.write_to_gpib('DE;')  # close Instument
        self.inst.clear()

    def status_byte(self):
        # stb = {'1': 'Data ready', '2': 'SyntaxError', '3': 'End status', '4': 'Illegal Program', '5': 'Busy', '6': 'Self Test Fail', '7': 'Request Service', '8': 'Emergency'}
        return self.inst.read_stb()
        # add code to interpret the result base on the above dic

    def prg_instrument(self, source_type='voltage', channel='4', source_range='3', value='0.1', compliance='0.1'):
        # votage range 0= AUTo ; 1 = 20V ; 2 =40V ; 3 = 100V
        # current range 0 = AUTO ; 1 = 1nA; 2 = 10nA ; 3 = 100nA ; ... 9 = 100mA
        if source_type.lower() == 'voltage':
            print(self.write_to_gpib('DV' + channel + ',' + source_range + ',' + value + ',' + compliance, '\n'))  # add new line to indicate end of comunication to instrument
        elif source_type.lower() == 'current':
            print(self.write_to_gpib('DI' + channel + ',' + source_range + ',' + value + ',' + compliance, '\n'))  # add new line to indicate end of comunication to instrument
        else:
            print('prg_instrument function hac incorect parameters')

    def config_instrument(self):
        # votage range 0= AUTo ; 1 = 20V ; 2 =40V ; 3 = 100V
        # current range 0 = AUTO ; 1 = 1nA; 2 = 10nA ; 3 = 100nA ; ... 9 = 100mA
        if self.source_type.lower() == 'voltage':
            print(self.write_to_gpib('DV' + self.channel + ',' + self.source_range + ',' + self.value + ',' + self.compliance, '\n'))  # add new line to indicate end of comunication to instrument
        elif self.source_type.lower() == 'current':
            print(self.write_to_gpib('DI' + self.channel + ',' + self.source_range + ',' + self.value + ',' + self.compliance, '\n'))  # add new line to indicate end of comunication to instrument
        else:
            print('config_instrument function hac incorect parameters')
            pass

    def measure_channel(self, source_type='voltage', channel='4'):
        if source_type.lower() == 'voltage':
            number = self.pattern.search(self.query('TV' + channel))
            return number.group()
        elif source_type.lower() == 'current':
            number = self.pattern.search(self.query('TI' + channel))
            return number.group()
        else:
            # implement handle
            print('measure_channel function hac incorect parameters')

    def get_measurement(self):
        if self.source_type.lower() == 'voltage':
            number = self.pattern.search(self.query('TV' + self.channel))  # get the string containing the floating value of the result
            return number.group()
        elif self.source_type.lower() == 'current':
            number = self.pattern.search(self.query('TI' + self.channel))
            return number.group()
        else:
            print('get_measurement function hac incorect parameters')
            # implement handle
