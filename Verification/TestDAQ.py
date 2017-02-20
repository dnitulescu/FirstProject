import ctypes
import time

daq_mx_dll = ctypes.CDLL(r'C:\Users\m16726\PycharmProjects\FirstProject\nicaiu.dll')
print(daq_mx_dll)

task_handle = ctypes.pointer(ctypes.c_int())
line_grouping = ctypes.c_long(1)
sample_rate = ctypes.c_double(10000.0)
active_edge = ctypes.c_long(10171)  # used Specifies on which edge of the clock to acquire or generate samples 0 or 1
                                    # DAQmx_Val_Rising = 10280  DAQmx_Val_Falling = 10171
sample_mode = ctypes.c_long(10178)  # Specifies whether the task acquires or generates samples continuously or if it acquires or generates a finite number of samples.
                                    # DAQmx_Val_FiniteSamps = 10178 Acquire or generate a finite number of samples.
                                    # DAQmx_Val_ContSamps = 10123 Acquire or generate samples until you stop the task.
                                    # DAQmx_Val_HWTimedSinglePoint = 12522 Acquire or generate samples continuously using hardware timing without a buffer. Hardware timed single point sample mode is supported only for the sample clock and change detection timing types.
sample_per_Ch = ctypes.c_ulonglong(4)
sample_written = ctypes.c_ulonglong(10)
ch0_name = "DAQ6321/port0/line0"
ref_clock = " OnboardClock "
auto_start = ctypes.c_bool(0)
timeout = ctypes.c_double(10)

a = (ctypes.c_uint8 * 4)
data_array = a(255, 0, 255, 0)
print(data_array)
flag_task_done = ctypes.c_bool(0)

name = ctypes.c_wchar()
daq_mx_dll.DAQmxCreateTask("j", ctypes.byref(task_handle))
daq_mx_dll.DAQmxGetTaskName(task_handle, ctypes.byref(name), ctypes.c_uint32(32))
print('task name ', name)

daq_mx_dll.DAQmxCreateDOChan(task_handle, ch0_name.encode('utf-8'), "", line_grouping)
daq_mx_dll.DAQmxCfgSampClkTiming(task_handle, ref_clock.encode('utf-8'), sample_rate, active_edge, sample_mode, sample_per_Ch)
daq_mx_dll.DAQmxWriteDigitalU8(task_handle,
                               sample_per_Ch,
                               auto_start,
                               timeout,
                               ctypes.c_bool(0),  # bool32 dataLayout,
                               data_array,  # uInt8 writeArray[],
                               ctypes.byref(sample_written),
                               None)
daq_mx_dll.DAQmxStartTask(task_handle)
while flag_task_done == ctypes.c_bool(0):
    daq_mx_dll.DAQmxIsTaskDone(task_handle, ctypes.byref(flag_task_done))

time.sleep(10)

daq_mx_dll.DAQmxStopTask(task_handle)
daq_mx_dll.DAQmxClearTask(task_handle)
