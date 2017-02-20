import re

from Verification.InstrumentClass import VInstrument


class AgilentE3631A(VInstrument):

    def initialize(self):
        print(self.write_to_gpib('*RST'))  # reset Instument
        print(self.query('*IDN?'))  # get name

    def close(self):
        self.write_to_gpib('*RST')  # reset Instumenr
        self.inst.clear()
        # self.inst.close()

    def system_version(self):
        return self.query("SYSTem:VERSion?")

    def read_error(self):
        return self.query("SYSTem:Error?")

    def prg_instument(self, output="out1", voltage='1', current='0.2'):
        p = re.compile('(out){1}[a-z]*[1-3]{1}')  # this regular expresion searches for outx outputx
        n = re.compile('[1-3]{1}')
        channels = {'1': 'P6V', '2': 'P25V', '3': 'N25V'}   # channel names
        if p.fullmatch(output.lower()):
            print('mathed detected')
            i = n.findall(output.lower(),)  # get channel value 1 ,2 or 3 ; the values is returned as list
            return self.write_to_gpib('APPLy '+channels[i.pop()]+' , '+voltage+' , '+current)
        else:
            # insert code to raise exception or error
            print('nothing')

    def enable_output(self,enable='false'):
        if enable.lower()=='true':
            self.write_to_gpib('OUTPut:STATe ON')
        else:
            self.write_to_gpib('OUTPut:STATe OFF')