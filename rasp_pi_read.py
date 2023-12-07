import serial
import time
import matplotlib.pyplot as plt

class TimeSync:
    def __init__(self) -> None:
        self.ser1=serial.Serial('COM5',115200)
        self.ser2=serial.Serial('COM9',115200)
    
    def ReadData(self,port:int) -> list:
        if port == 1:
            indata:str = self.ser1.readline().decode('utf-8')
        elif port == 2:
            indata:str = self.ser2.readline().decode('utf-8')
        else:
            raise ValueError('No Data Read:Port must be 1 or 2')
        if indata == 'waiting for sync message':
            print('Waiting for Sync')
            return -1
        tmp=['','']
        tmp = indata.split('#')
        data = tmp[1]
        #print('Recieved Time:',data,'Recieved Data:',tmp[0]+' C')
        return float(data)

    def ClockDrift(self,data_arr,tm) -> float:
        delay = abs(data_arr - tm)
        print('Clock Drift:',delay)
        return delay
    
    def NetworkDelay(self,port) -> None:
        tm = time.time()
        send = 'T'+str(tm)
        if port == 1:
            self.ser1.write(send.encode('utf-8'))
            while self.ser1.out_waiting > 0:
                pass
            delay = len(bytes(send,'utf-8'))/(time.time()-tm)
        elif port == 2:
            self.ser2.write(send.encode('utf-8'))
            while self.ser2.out_waiting > 0:
                pass
            delay = len(bytes(send,'utf-8'))/(time.time()-tm)
        print("Network Delay:",delay)
        return delay
        
    def TimeSync(self,port,tm):
        if port == 1:
            time_out = tm
            time_out = 'T'+str(time_out)
            self.ser1.write(time_out.encode("utf-8"))
        elif port == 2:
            time_out = tm
            time_out = 'T'+str(time_out)
            self.ser2.write(time_out.encode("utf-8"))
        else:
            raise ValueError('No Data Sent:Port must be 1 or 2')

if __name__ == '__main__':
    prog = TimeSync()
    clckplt1 = []
    clckplt2 = []
    i = 1
    x = []
    while(i <=100):
        x.append(i)
        tm = time.time()
        prog.TimeSync(1,tm)
        data1 = prog.ReadData(1)
        drift1 = prog.ClockDrift(data1,tm)
        tm = time.time()
        prog.TimeSync(2,tm)
        data2 = prog.ReadData(2)
        drift2 = prog.ClockDrift(data2,tm)
        if drift1 < 100:
            clckplt1.append(drift1)
        else:
            clckplt1.append(0)
        if drift2 < 100:
            clckplt2.append(drift2)
        else:
            clckplt2.append(0)
        #prog.ClockDrift(data2,data2)
        print(i)
        i+=1
    avg1 = sum(clckplt1)/len(clckplt1)
    avg2 = sum(clckplt2)/len(clckplt2)
    print('Average Clock Drift (Device 1):',avg1)
    print('Average Clock Drift (Device 2):',avg2)

    
    plt.plot(x,clckplt1, label ='Arduino 1')
    plt.plot(x,clckplt2,label = 'Arduino 2')
    ax = plt.gca()
    ax.set_xlim([5,len(x)])
    ax.set_ylim([-1.75,1.75])
    plt.xlabel('Iterations')
    plt.ylabel('Clock Drift')
    plt.title('Clock Drift through Wired Connections')
    plt.legend()
    plt.show()

    
    
'''
print(prog.NetworkDelay(1),prog.NetworkDelay(2))
'''
