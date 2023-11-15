import serial
import time

class TimeSync:
    def __init__(self) -> None:
        self.ser1=serial.Serial('dev/ttyACM0',9600)
        self.ser2=serial.Serial('dev/ttyACM1',9600)
    
    def ReadData(self,port:int) -> list:
        if port == 1:
            indata:str = self.ser1.readline()
        elif port == 2:
            indata:str = self.ser2.readline()
        else:
            raise ValueError('No Data Read:Port must be 1 or 2')
        j=0
        tmp=''
        data=[0,0]
        for i in indata:
            if j == 2:
                break
            elif i == ' ':
                data[j]=float(tmp)
                j+=1
            elif i == '\0':
                break
            else:
                tmp+=i
        print(data)
        return data

    def NetworkDelay(self,data_arr:list,port:int) -> float:
        delay = time.clock_gettime() - data_arr[0]
        print(delay)
        return delay
    
    def ClockDrift(time1:float,time2:float) -> None:
        if time1 < 0:
            raise ValueError('Time from Port 1 device is negative')
        if time2 < 0:
            raise ValueError('Time from port 2 device is negative')
        print(time1-time2)


if __name__ == '__main__':
    while(1):
        prog = TimeSync()
        data_arr1 = prog.ReadData(1)
        data_arr2 = prog.ReadData(2)
        delay1 = prog.NetworkDelay(data_arr1)
        delay2 = prog.NetworkDelay(data_arr2)
        prog.ClockDrift(delay1,delay2)


    
    