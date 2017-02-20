import visa
import re


class VInstrument():
    GPIBAdress = ""
    device_name =""
    rm = visa.ResourceManager()   # rm opens the resourse manager
    inst = visa.Resource    # inst opens an instance to the instrument

    def __init__(self, adress):
        self.GPIBAdress = adress
        # insert try castch block for instrument check
        self.inst = self.rm.open_resource(adress)

    def initialize(self):
        pass

    def query(self, command):
        return(self.inst.query(command))

    def write_to_gpib(self, command, termination=None, encoding=None):
        print(command)
        return(self.inst.write(command,termination, encoding))

    def read_status_byte(self):
        return(self.inst.read_stb())

    def close(self):
        #self.inst.close()
        self.inst.clear()

