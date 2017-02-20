import ctypes

from Verification.InstrumentClass import VInstrument


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class DAQ6321(VInstrument):
    daq_mx_dll = ctypes.CDLL
    task_handle = ctypes.pointer(ctypes.c_int())
    line_grouping = ctypes.c_long(1)  # One channel for each line or One channel for all lines
    sample_rate = ctypes.c_double(10000.0)
    active_edge = ctypes.c_long(
        10171)  # used Specifies on which edge of the clock to acquire or generate samples 0 or 1
    # DAQmx_Val_Rising = 10280  DAQmx_Val_Falling = 10171
    sample_mode = ctypes.c_long(
        10178)  # Specifies whether the task acquires or generates samples continuously or if it acquires or generates a finite number of samples.
    # DAQmx_Val_FiniteSamps = 10178 Acquire or generate a finite number of samples.
    # DAQmx_Val_ContSamps = 10123 Acquire or generate samples until you stop the task.
    # DAQmx_Val_HWTimedSinglePoint = 12522 Acquire or generate samples continuously using hardware timing without a buffer. Hardware timed single point sample mode is supported only for the sample clock and change detection timing types.
    sample_per_Ch = ctypes.c_ulonglong(4)
    samples_written = ctypes.c_ulonglong(10)
    ref_clock = " OnboardClock "
    auto_start = ctypes.c_bool(0)
    timeout = ctypes.c_double(10)
    dataLayout = ctypes.c_bool(0),  # gropu by channel or by line

    def __init__(self, device_name):
        self.device_name = device_name
        self.daq_mx_dll = ctypes.CDLL(r'C:\Users\m16726\PycharmProjects\FirstProject\nicaiu.dll')

    def check_response(self, code):
        if code == 0:
            pass
        elif code < 0:
            er_string = ctypes.cast("This is used ass adress for the error string ", ctypes.c_char_p)
            self.daq_mx_dll.DAQmxGetErrorString(code, er_string, 200)
            raise Exception(er_string.value)
        else:
            print('warning')

    def prg_do_channel(self, port='0', line='0', value=(0, 0, 0, 0, 0), samplerate=10000):
        task_name = ctypes.c_wchar()
        ch_name = self.device_name+'/port'+port+'/line'+line
        print(ch_name)
        sample_per_ch = ctypes.c_ulonglong(len(value))
        sample_written = ctypes.c_ulonglong(10)
        data_array = (ctypes.c_uint8 * len(value))(*value)
        flag_task_done = ctypes.c_bool(0)

        self.daq_mx_dll.DAQmxCreateTask("j", ctypes.byref(self.task_handle))
        self.daq_mx_dll.DAQmxGetTaskName(self.task_handle, ctypes.byref(task_name),
                                         ctypes.c_uint32(32))  # get Task name
        self.check_response(self.daq_mx_dll.DAQmxCreateDOChan(self.task_handle,
                                                              ch_name.encode('utf-8'),
                                                              "",
                                                              self.line_grouping))
        self.check_response(self.daq_mx_dll.DAQmxCfgSampClkTiming(self.task_handle,
                                                                  self.ref_clock.encode('utf-8'),
                                                                  ctypes.c_double(samplerate),
                                                                  self.active_edge,
                                                                  self.sample_mode,
                                                                  sample_per_ch))
        self.check_response(self.daq_mx_dll.DAQmxWriteDigitalU8(self.task_handle,
                                                                sample_per_ch,
                                                                ctypes.c_bool(0),  # autostart
                                                                self.timeout,
                                                                ctypes.c_bool(0),  # bool32 dataLayout/gr by ch or line
                                                                data_array,  # uInt8 writeArray[],
                                                                ctypes.byref(sample_written),  # number of sample writen
                                                                None))
        self.check_response(self.daq_mx_dll.DAQmxStartTask(self.task_handle))
        while flag_task_done.value == ctypes.c_bool(0).value:
            self.daq_mx_dll.DAQmxIsTaskDone(self.task_handle, ctypes.byref(flag_task_done))
        self.daq_mx_dll.DAQmxStopTask(self.task_handle)
        self.daq_mx_dll.DAQmxClearTask(self.task_handle)

    # noinspection PyBroadException
    def prg_ao_channel(self, line='0', value=(0, 0, 0, 0, 0), samplerate=10000, min=-1, max=10):
        task_name = ctypes.c_wchar()
        ch_name = self.device_name+'/ao'+line
        sample_per_ch = ctypes.c_ulonglong(len(value))
        sample_written = ctypes.c_ulonglong(10)
        data_array = (ctypes.c_double * len(value))(*value)
        flag_task_done = ctypes.c_bool(0)
        self.daq_mx_dll.DAQmxCreateTask("j", ctypes.byref(self.task_handle))
        self.daq_mx_dll.DAQmxGetTaskName(self.task_handle,
                                         ctypes.byref(task_name),
                                         ctypes.c_uint32(32))  # get Task name
        self.check_response(self.daq_mx_dll.DAQmxCreateAOVoltageChan(self.task_handle,
                                                                     ch_name.encode('utf-8'),
                                                                     "",
                                                                     ctypes.c_double(min),
                                                                     ctypes.c_double(max),
                                                                     ctypes.c_long(10348),  # the integer for Volt units
                                                                     None))
        self.check_response(self.daq_mx_dll.DAQmxCfgSampClkTiming(self.task_handle,
                                                                  self.ref_clock.encode('utf-8'),
                                                                  ctypes.c_double(samplerate),
                                                                  self.active_edge,
                                                                  self.sample_mode,
                                                                  sample_per_ch))
        self.check_response(self.daq_mx_dll.DAQmxWriteAnalogF64(self.task_handle,
                                                                sample_per_ch,
                                                                ctypes.c_bool(0),  # autostart
                                                                self.timeout,
                                                                ctypes.c_bool(0),  # bool32 dataLayout,gr by ch or line
                                                                data_array,
                                                                ctypes.byref(sample_written),  # number of sample writen
                                                                None))
        self.check_response(self.daq_mx_dll.DAQmxStartTask(self.task_handle))
        while flag_task_done.value == ctypes.c_bool(0).value:
            self.daq_mx_dll.DAQmxIsTaskDone(self.task_handle, ctypes.byref(flag_task_done))
        self.daq_mx_dll.DAQmxStopTask(self.task_handle)
        self.daq_mx_dll.DAQmxClearTask(self.task_handle)

    def build_spi_cmd(self, data=(0, 0, 0, 0, 0), edge='falling'):
        clk_data = []
        csn_data = []
        sdi_data = []
        if edge == 'rising':
            for i in range(0, len(data), 1):
                clk_data.extend((0, 255))
                csn_data.extend((0, 0))
                sdi_data.extend((data[i], data[i]))
        else:
            for i in range(0, len(data), 1):
                clk_data.extend((255, 0))
                csn_data.extend((0, 0))
                sdi_data.extend((data[i], data[i]))
        # add csn info
        csn_data = [255] + csn_data + [255]
        clk_data = [0] + clk_data + [0]
        sdi_data = [0] + sdi_data+ [0]
        # print(clk_data[0:])
        # print(sdi_data[0:])
        # print(csn_data[0:])
        sdi_data.extend(csn_data)
        clk_data.extend(sdi_data)
        return clk_data[0:]

    def SPI_pattern(self, CLKLine='0', SDILine='3',CSNLine='2', SDOLine='4', SPI_pattern=(0, 0, 0, 0, 0), samplerate=10000):
        task_name = ctypes.c_wchar()
        CLK_channel = self.device_name+'/port'+'0'+'/line'+CLKLine
        SDI_channel = self.device_name+'/port'+'0'+'/line'+SDILine
        CSN_channel = self.device_name+'/port'+'0'+'/line'+CSNLine
        sample_per_ch = ctypes.c_ulonglong(int(len(SPI_pattern)/3))
        sample_written = ctypes.c_ulonglong(10)
        data_array = (ctypes.c_uint8 * len(SPI_pattern))(*SPI_pattern)
        flag_task_done = ctypes.c_bool(0)
        self.daq_mx_dll.DAQmxCreateTask("j", ctypes.byref(self.task_handle))
        self.daq_mx_dll.DAQmxGetTaskName(self.task_handle, ctypes.byref(task_name),
                                         ctypes.c_uint32(32))  # get Task name
        self.check_response(self.daq_mx_dll.DAQmxCreateDOChan(self.task_handle,
                                                              CLK_channel.encode('utf-8'),
                                                              str("CLK").encode('utf-8'),
                                                              self.line_grouping))
        self.check_response(self.daq_mx_dll.DAQmxCreateDOChan(self.task_handle,
                                                              SDI_channel.encode('utf-8'),
                                                              str("SDI").encode('utf-8'),
                                                              self.line_grouping))
        self.check_response(self.daq_mx_dll.DAQmxCreateDOChan(self.task_handle,
                                                              CSN_channel.encode('utf-8'),
                                                              str("CSN").encode('utf-8'),
                                                              self.line_grouping))
        self.check_response(self.daq_mx_dll.DAQmxCfgSampClkTiming(self.task_handle,
                                                                  self.ref_clock.encode('utf-8'),
                                                                  ctypes.c_double(samplerate),
                                                                  self.active_edge,
                                                                  self.sample_mode,
                                                                  sample_per_ch))
        self.check_response(self.daq_mx_dll.DAQmxDisableStartTrig(self.task_handle))
        #self.check_response(self.daq_mx_dll.DAQmxCfgDigEdgeStartTrig(self.task_handle,
         #                                                            self.ref_clock.encode('utf-8'),  # trig signal
         #                                                            self.active_edge))  # trigger edge
        print(sample_per_ch.value)
        print(data_array[1])
        self.check_response(self.daq_mx_dll.DAQmxWriteDigitalU8(self.task_handle,
                                                                sample_per_ch,
                                                                ctypes.c_bool(0),  # autostart
                                                                self.timeout,
                                                                ctypes.c_bool(0),  # bool32 dataLayout/ropu by ch ore
                                                                data_array,
                                                                ctypes.byref(sample_written),  # number of sample writen
                                                                None))
        self.check_response(self.daq_mx_dll.DAQmxStartTask(self.task_handle))
        while flag_task_done.value == ctypes.c_bool(0).value:
            self.daq_mx_dll.DAQmxIsTaskDone(self.task_handle, ctypes.byref(flag_task_done))
        self.daq_mx_dll.DAQmxStopTask(self.task_handle)
        self.daq_mx_dll.DAQmxClearTask(self.task_handle)

    def send_spi_cmd(self,clk_line='0', sdi_line='3',cs_line='2', sdo_line ='4', data=(0, 0, 0, 0, 0), samplerate=10000, edge='falling'):
        self.SPI_pattern(CLKLine=clk_line,
                         SDILine=sdi_line,
                         CSNLine=cs_line,
                         SDOLine=sdo_line,
                         SPI_pattern=self.build_spi_cmd(data=data, edge=edge),
                         samplerate=samplerate)


a = DAQ6321("DAQ6321")
#a.prg_do_channel(value=(0, 0, 255, 0, 0, 0, 255, 255, 0, 255))
#a.prg_ao_channel(value=(1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 1, 5))
#a.SPI_pattern(SPI_pattern=(0,0,255,0,255,0,0,  0,255,0,255,0,255,0, 255,0,0,0,0,0,255 ) , SDILine='7')
#a.build_spi_cmd(data=(0,255,0,255,0))
a.send_spi_cmd(data=(0, 225, 0, 255, 0, 255, 0, 0), sdi_line='7')