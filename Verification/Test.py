import time

import visa

from Verification.AgilentE3631A import AgilentE3631A
from Verification.SPA4145B import SPA4145B

rm = visa.ResourceManager()  # rm opens the resourse manager
print(rm.list_resources())

#init faze
print('\n *********************intialized faze**************************** ')
instrument = AgilentE3631A("GPIB0::13::INSTR")
instrument.initialize()
SPA=SPA4145B("GPIB0::17::INSTR")
SPA.initialize()



#configure faze
print('\n *********************configure faze********************* ')
#print(instument.write_to_gpib("APPLy P6V,1,0.1; OUTPut:STATe ON"))
instrument.prg_instument(output='output1',voltage='2',current='0.5')
instrument.prg_instument(output='output2')
instrument.enable_output('true')
SPA.prg_instrument(source_type='voltage', channel='4',source_range='3',value='2',compliance='0.1' )


time.sleep(5)

#SPA.measure_values()
print(SPA.get_measurement())
print(SPA.get_measurement())
print(SPA.measure_channel(source_type='current'))
time.sleep(10)


print(instrument.write_to_gpib("OUTPut:STATe OFF"))


#close faze
print('\n *********************close faze********************* ')
time.sleep(1)
instrument.close()
SPA.close()
print('error=>', instrument.read_error())
print('system version=>', instrument.system_version())