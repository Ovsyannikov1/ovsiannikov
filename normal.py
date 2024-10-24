
import RPi.GPIO as gp
import time

def dec2bin(num):
    return [int(bit) for bit in bin(int(num))[2:].zfill(8)]


    
leds=[9,10,22,27,17,4,3,2]

dac = [8,11,7,1,0,5,12,6]
comp = 14
troyka = 13
gp.cleanup()
gp.setmode(gp.BCM)

gp.setup(comp, gp.IN)
gp.setup(troyka, gp.OUT, initial=gp.HIGH)

u_max = 3.3

gp.setup(leds, gp.OUT)
for led in dac:
    gp.setup(led, gp.OUT)

for led in dac:
    gp.output(led, 0)

def adc():
    num = [0]*8
    for i in range(8):
        # print('binary ', str(num))
        num[i] = 1
        for j in range(8):
            gp.output(dac[j], num[j])
        time.sleep(0.01)
        if gp.input(comp):
            num[i] = 0
        
    return int(''.join(str(x) for x in num), 2)

try:
    gp.output(leds, [0]*8)
    while True:
        n = adc()
        print(n, n*3.3/255)

        perc = round(n/255*8)
        for i in range(perc):
            gp.output(leds[i],1)
        for i in range(perc, 8):
            gp.output(leds[i],0)
        time.sleep(0.1)

        
finally:
    gp.output(troyka, 0)
    for led in dac:
        gp.output(led, 0)
import RPi.GPIO as GPIO
import sys
from time import sleep
GPIO.setmode(GPIO.BCM)
dac=[26,19,13,6,5,11,9,10]
c=4
t=17
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(t,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(c,GPIO.IN)
def p(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]
def adc():
    s=0
    for i in range(7,-1,-1):
        s=s+2**i
        GPIO.output(dac,p(s))
        comp=GPIO.input(c)
        sleep(0.05)
        if GPIO.input(c)==0:
            s=s-2**i
    return s
try:
    while True:
        s=adc()
        if s!=0:
            print(s,'{:.2f}v'.format(3.3*s/256))
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()
import RPi.GPIO as GPIO
import sys
from time import sleep
GPIO.setmode(GPIO.BCM)
dac=[26,19,13,6,5,11,9,10]
c=4
t=17
GPIO.setup(dac,GPIO.OUT)
GPIO.setup(t,GPIO.OUT,initial=GPIO.HIGH)
GPIO.setup(c,GPIO.IN)
def p(a):
    return [int (elem) for elem in bin(a)[2:].zfill(8)]
def adc():
    for i in range(256):
        das=p(i)
        GPIO.output(dac,das)
        comp=GPIO.input(c)
        sleep(0.05)
        if comp==0:
            return i
try:
    while True:
        i=adc()
        if i!=0:
            print(i,'{:.2f}v'.format(3.3*i/256))
finally:
    GPIO.output(dac,0)
    GPIO.cleanup()



import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

data = np.loadtxt('data (1).txt')
with open('settings (1).txt') as f:
    dt = float(f.readline())
    dU = float(f.readline())

t_ax = np.arange(0, dt*(len(data)), dt)
data = data * dU

t_charge = t_ax[np.argmax(data)]
t_discharge = t_ax[-1] - t_charge

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(16,10))
ax.plot(t_ax, data, label='V(t)', color='b', marker='o', markevery=10)
ax.set_title('Процесс заряда и разряда конденсатора в RC-цепочке', loc='left', wrap=True)

plt.ylabel('Напряжение, В')
plt.xlabel('Время, с')

plt.annotate('Время зарядки: ' + str(t_charge) + 'c \nВремя разрядки: ' + str(t_discharge), [8,2])

plt.xlim(0,12)
plt.ylim(0,2.9)

ax.yaxis.set_minor_locator(AutoMinorLocator())
ax.xaxis.set_minor_locator(AutoMinorLocator())
ax.grid(which='minor', axis='both', linestyle='--')
ax.grid(which='major', axis='both', linestyle='-')
ax.legend()
plt.show()
fig.savefig('graph.svg', dpi=100)

