############### Library ###############
import pycom
import machine
import time
from machine import Pin
import socket
from network import LoRa
import binascii
import array
from machine import PWM


############### LoRa Connectie ###############
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868) # LoRa connectie binnen Europa
app_eui = binascii.unhexlify('70B3D57ED003B935') # App EUI van TTN/Device
app_key = binascii.unhexlify('D0258B34705B17B2DD2C87CA07CA5D68') # App Key van TTN/Device
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0) # Code om de connectie te kunnen maken tussen de Lopy en TTN/LoRa Gateway

# Wachten tot LoRa joined
while not lora.has_joined():
    time.sleep(2.5)
    print('Not joined yet...')

print('Network joined!') # Print als het geconnecteerd is

############### Weightsensor ###############
def main():
    while True:
        adc = machine.ADC()             # maak een ADC object
        apin = adc.channel(pin='P16')   # maak een analoge pin op P16
        val = apin()                    # lees de analoge waarde

        if val < 20:                    # als de value onder de 20 blijft dan is het gewicht goed
            print(val)                  # print de value van de analoge waarde
            print("Weight is good")     # print als het gewicht goed is
            binaryString = bin(val)     # zet de value om naar binaire waarde in een string
            print(binaryString)         # print de value in binaire vorm
            time.sleep(2.5)             # laat 2.5 seconden tussen elke lezing

        if val > 20:
            print(val)
            print("Weight is to high") # print als het gewicht te hoog is
            binaryString = bin(val)
            print(binaryString)
            time.sleep(2.5)

            # pulse Width Modulation van de buzzer
            pwm = PWM(3, frequency=78000)  # de timer staat op 3, de frequentie(integer) op 78k (maximale waarde)
            pwm_c = pwm.channel(0, pin='P20', duty_cycle=1.0)   # pwm kanaal op P20 met een duty cycle(float argument) van 100% (maximale waarde)
            pwm_c.duty_cycle(0.3) # verandering van duty cycle

        ############### Verzenden van data naar TTN ###############
        # een socket is een manier om twee nodes to connecteren en te laten communiceren met elkaar.
        s = socket.socket(socket.AF_LORA, socket.SOCK_RAW) # maak een socket aan om pakketjes te verzenden
        s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5) # wijs een socket toe
        s.setblocking(False) # als de waarde False is zend het de volgende waarde
        s.send(bytes(val)) # verzend de waarde in bytes als een string



if __name__ == "__main__":
    main()