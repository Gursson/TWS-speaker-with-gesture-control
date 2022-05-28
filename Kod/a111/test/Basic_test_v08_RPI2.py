#Radarsensor
import acconeer.exptool as et
import numpy as np
import time
import gpiozero
import RPi.GPIO as GPIO

import subprocess  #Run RF send.py


def main():
    args = et.a111.ExampleArgumentParser().parse_args()

    # The client logs using the logging module with a logger named
    # acconeer.exptool.*. We call another helper function which sets up
    # the logging according to the verbosity level set in the arguments:
    # -q  or --quiet:   ERROR   (typically not used)
    # default:          WARNING
    # -v  or --verbose: INFO
    # -vv or --debug:   DEBUG
    et.utils.config_logging(args)
    client = et.a111.Client(**et.a111.get_client_args(args))

    config = et.a111.EnvelopeServiceConfig()

    # In all examples, we let you set the sensor(s) via the command line
    #config.sensor = args.sensors
    config.sensor = [1,2]

    #config.sensor
    # Set the measurement range [meter]
    config.range_interval = [0.1, 0.3]

    # Set the target measurement rate [Hz]
    config.update_rate = 15

    client.connect()
    
    #13(pin 33), 16(pin 36), 
    def Swipe_Menu_LED_On():
        GPIO.output(13, True)
        print("--- Swipe Menu ----")
    
    def Swipe_Menu_LED_Off():
        GPIO.output(13, False)
        
    def Vol_Menu_LED_On():
        print("---Vol Menu---")
        GPIO.output(13, True)
    
    def Vol_Menu_LED_Off():
        print("---Vol Timeout---")    
        GPIO.output(13, False)
        
    def LED_blink():
        if GPIO.input(13) == True:
            GPIO.output(13, False)
            time.sleep(0.2)
            GPIO.output(13, True)
            time.sleep(0.2)
            GPIO.output(13, False)
            time.sleep(0.2)
            GPIO.output(13, True)
        else:
            GPIO.output(13, True)
            time.sleep(0.2)
            GPIO.output(13, False)
            time.sleep(0.2)
            GPIO.output(13, True)
            time.sleep(0.2)
            GPIO.output(13, False)
            
    def Play_Pause(): #Double tap on left earbud
        print("Play/Pause")
    """
        GPIO.output(16, False)
		time.sleep(0.1)
        GPIO.output(16, True) 
        time.sleep(0.1)
        GPIO.output(16, False)
        time.sleep(0.1)
        GPIO.output(16, True) #Pull down
        time.sleep(0.1)
        GPIO.output(16, False)
    """
    def Volume_Up(): #Touch logo once on right earbud (no bluetooth)
        GPIO.output(16, False)
        time.sleep(0.15)
        GPIO.output(16, True) #Pull down
        time.sleep(0.15)
        GPIO.output(16, False)
        
    def Volume_Down(): #Touch logo once on left earbud (bluetooth)
        print("---Volume Down---")
        #subprocess.Popen(['python3','send.py','-g','19','-p', '250','-t','1','12345678'])

        
    def Song_next(): #Touch logo on the right for 2 seconds (no bluetooth)    
        print("--- Next Song ----")
        LED_blink()
        GPIO.output(16, False)
        time.sleep(0.1)
        GPIO.output(16, True) 
        time.sleep(2.2)
        GPIO.output(16, False)
        time.sleep(0.1)
        
    def Song_previous(): #Touch logo on the left for 2 seconds (bluetooth)
        print("--- Previous Song ----")
        #subprocess.Popen(['python3','send.py','-g','19','-p', '250','-t','1','23456789'])
        LED_blink()
        
    session_info = client.setup_session(config)
    print("Session info:\n", session_info, "\n")

    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")
   
    #init :
    GPIO.setmode(GPIO.BCM) #Using pins BCM numbers
    #GPIO.setup(17 of pin, GPIO.OUT)
    
    GPIO.setup(16, GPIO.OUT) #Signal to earbud
    GPIO.setup(13, GPIO.OUT) #Signal to LED
    GPIO.output(13, False)
    LED_blink()
    #använder nr 36 som är GPIO16, använd 16
    #Skriv pinout för att se GPIOs
    
    
    
    Swipe_right_counter = 0
    Swipe_left_counter = 0
    Timer_Swipe_Menu = 0 #Counter for time in menu
    cycles = 0 #
    Menu_timer_start = 0 #Init menu Menu
    Swipe_timer_1 = 0
    Swipe_timer_0 = 0
    
    #Parameters:
    Swipe_Menu_time = 5
    DataPoint_Volume = 20
    DataPoint_Pause_Play = 20
    DataPoint_Swipe = 3
    DataPoint_Vol_Menu = 10
    DataPoint_PP = 15
    
    Counter_PP = 0
    Timer_PP = 0
    Counter_Vol_Menu = 0
    Counter_Vol_Up = 0
    Counter_Vol_Down = 0
    Timer_Vol_Menu = 0
    Counter_H1 = 0
    Counter_V1 = 0
    Counter_H2 = 0
    Counter_V2 = 0
    Timer_H1 = 0
    Timer_V1 = 0
    Timer_H2 = 0
    Timer_V2 = 0
    Timer_Control = 0


    while not interrupt_handler.got_signal:#for i in range(lengd):
        data_info, data = client.get_next()

        index = np.argmax(data, axis = 1, out = None);
        print(index)
        
        #Pause/Play Toggle, hold right side. (Double click left earbud)
        if index[1] > 200 and index[0] < 70:
            Counter_PP = Counter_PP + 1
            if Counter_PP > DataPoint_PP:
                print("Toggle Pause/Play")
                subprocess.Popen(['python3','send.py','-g','19','-p','250','-t','1','34567890'])
                Play_Pause()
                Counter_PP = 0
        else:
            Counter_PP = 0
            
        # Swipe Menu Start 
        if index[1] > 70 and Swipe_timer_1 == 0 and Timer_Swipe_Menu == 0 and (time.time() - Timer_Control) > 2 and Timer_Vol_Menu == 0: #Timer, not spamming when holding hand
            Swipe_right_counter = Swipe_right_counter + 1
            if Swipe_right_counter > DataPoint_Swipe:
                print("Menu swipe detected")
                Timer_Control = 0
                Swipe_timer_1 = time.time()


        elif (time.time() - Swipe_timer_1) > 2:
            Swipe_timer_1 = 0 
        else:
            Swipe_right_counter = 0

        if index[0] > 70 and 0 < (time.time() - Swipe_timer_1) < 2 and index[1] < 160:
            Swipe_left_counter = Swipe_left_counter + 1
            if Swipe_left_counter > DataPoint_Swipe:
                #print("--- Menu ----")
                Swipe_Menu_LED_On()
                Swipe_timer_1 = 0
                Timer_Swipe_Menu = time.time()
                
        else:
            Swipe_left_counter = 0
            
        
        
        #Volume Menu 
        if index[0] > 250 and index[1] > 250 and Timer_Vol_Menu == 0 and Timer_Swipe_Menu == 0: 
            Counter_Vol_Menu = Counter_Vol_Menu + 1
            if Counter_Vol_Menu > DataPoint_Vol_Menu:
                Timer_Vol_Menu = time.time()
                #print("---Vol Menu---")
                Vol_Menu_LED_On()
                Counter_Vol_Menu = 0
        else: 
            Counter_Vol_Menu = 0
        #Inside Vol Menu    
        if Timer_Vol_Menu > 0:
            if (time.time() - Timer_Vol_Menu) > Swipe_Menu_time:
                #print("---Vol Timeout---")
                Vol_Menu_LED_Off()
                Timer_Vol_Menu = 0
            #Higher Vol
            elif index[1] > 270 and index[0] > 270:
                Counter_Vol_Up = Counter_Vol_Up + 1 
                if Counter_Vol_Up > DataPoint_Volume:
                    print("---Volume Up---")
                    Volume_Up()
                    LED_blink()
                    Timer_Vol_Menu = time.time()
                    Counter_Vol_Up = 0
            else:
                Counter_Vol_Up = 0
            #Lower Vol
            if  50 < index[1] < 150  and 50 < index[0] < 150:
                Counter_Vol_Down = Counter_Vol_Down + 1 
                if Counter_Vol_Down > DataPoint_Volume:
                    subprocess.Popen(['python3','send.py','-g','19','-p','250','-t','1','12345678'])
                    Volume_Down()
                    LED_blink()
                    Timer_Vol_Menu = time.time()
                    Counter_Vol_Down = 0
            else:
                Counter_Vol_Down = 0
        
        
        
        #Inside Swipe Menu
        
        if Timer_Swipe_Menu > 0 :
           
            if (time.time() - Timer_Swipe_Menu) > Swipe_Menu_time: 
               Timer_Swipe_Menu = 0
               print("---Menu Timeout---")
               Swipe_Menu_LED_Off()
            
            #CHECK SWIPE LEFT (PREVIOUS SONG)
            elif index[1] > 70 and Swipe_timer_1 == 0 and Timer_H2 == 0 and ((time.time() - Timer_Swipe_Menu) > 1):# and index[0] < 120:
                Counter_H1 = Counter_H1 + 1
                if Counter_H1 > DataPoint_Swipe:
                    Timer_H1 = time.time()
            else:
                Counter_H1 = 0   
            if 0 < (time.time() - Timer_H1) < 1 and index[0] > 70 :
                Counter_V1 = Counter_V1 + 1
                if  Counter_V1 > DataPoint_Swipe :
                    Song_previous()
                    Counter_V1 = 0
                    Counter_H1 = 0  
                    Timer_Swipe_Menu = 0
                    Timer_Control = time.time()
                    Swipe_Menu_LED_Off()
                    subprocess.Popen(['python3','send.py','-g','19','-p','250','-t','1','23456789'])

                    
            else:
                Timer_H1 = 0
                Counter_V1 = 0
                
            
          
              #CHECK SWIPE RIGHT (NEXT SONG)
            
            if index[0] > 70 and Swipe_timer_0 == 0 and Timer_H1 == 0 and ((time.time() - Timer_Swipe_Menu) > 1):# and index[1] < 120:
                Counter_H2 = Counter_H2 + 1
                if Counter_H2 > DataPoint_Swipe:
                    Timer_H2 = time.time()
            else:
                Counter_H2 = 0     
            if 0 < (time.time() - Timer_H2) < 1 and index[1] > 70 :
                Counter_V2 = Counter_V2 + 1
                if  Counter_V2 > DataPoint_Swipe :
                    Song_next()
                    Counter_V2 = 0
                    Counter_H2 = 0 
                    Timer_Swipe_Menu = 0
                    Timer_Control = time.time()
                    Swipe_Menu_LED_Off()
                   
            else:
                Timer_H2 = 0
                Counter_V2 = 0
        
    
    
    
        
    # We're done, stop the session. All buffered/waiting data is thrown
    # away. This call will block until the server has confirmed that the
    # session has ended.
    GPIO.output(13, False)
    client.stop_session()

    # Calling stop_session before disconnect is not necessary as
    # disconnect will call stop_session if a session is started.

    # Remember to always call disconnect to do so gracefully
    client.disconnect()


if __name__ == "__main__":
    main()
