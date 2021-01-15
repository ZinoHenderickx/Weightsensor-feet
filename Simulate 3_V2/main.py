import pycom
import machine
import time
from machine import Pin
import socket
from network import LoRa
import binascii

############### LoRa Connectie ###############
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

app_eui = binascii.unhexlify('70B3D57ED003B935')
app_key = binascii.unhexlify('D0258B34705B17B2DD2C87CA07CA5D68')

lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!')

############### Weightsensor ###############
def main():
    while True:
        adc = machine.ADC()             # create an ADC object
        apin = adc.channel(pin='P16')   # create an analog pin on P16
        val = apin()                    # read an analog value

        if val < 20:
            print(val)
            print("Weight is good")
            binaryString = bin(val)
            print(binaryString)
            time.sleep(5)
        if val > 20:
            print(val)
            print("Weight is to high")
            binaryString = bin(val)
            print(binaryString)
            time.sleep(5)

        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        s.setblocking(False)
        s.send(bytes([val]))



if __name__ == "__main__":
    main()