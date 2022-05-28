import acconeer.exptool as et
import numpy as np
import time

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

    session_info = client.setup_session(config)
    print("Session info:\n", session_info, "\n")

    client.start_session()

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")
   
    #init :
    Swipe_right_counter = 0
    Swipe_left_counter = 0
    Timer_Swipe_Menu = 0 #Counter for time in menu
    cycles = 0 #
    Menu_timer_start = 0 #Init menu Menu
    Swipe_timer_1 = 0
    Swipe_timer_0 = 0
    

    #Parameters:
    Swipe_Menu_time = 10
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
        #print(index)
        
        #Pause/Play Toggle, hold right side
        if index[1] > 200 and index[0] < 70:
            Counter_PP = Counter_PP + 1
            if Counter_PP > DataPoint_PP:
                print("Toggle Pause/Play")
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
                print("--- Menu ----")
                Swipe_timer_1 = 0
                Timer_Swipe_Menu = time.time()
                
        else:
            Swipe_left_counter = 0
            
        
        
        #Volume Menu 
        if index[0] > 250 and index[1] > 250 and Timer_Vol_Menu == 0 and Timer_Swipe_Menu == 0: 
            Counter_Vol_Menu = Counter_Vol_Menu + 1
            if Counter_Vol_Menu > DataPoint_Vol_Menu:
                Timer_Vol_Menu = time.time()
                print("---Vol Menu---")
                Counter_Vol_Menu = 0
        else: 
            Counter_Vol_Menu = 0
        #Inside Vol Menu    
        if Timer_Vol_Menu > 0:
            if (time.time() - Timer_Vol_Menu) > Swipe_Menu_time:
                print("---Vol Timeout---")
                Timer_Vol_Menu = 0
            #Higher Vol
            elif index[1] > 270 and index[0] > 270:
                Counter_Vol_Up = Counter_Vol_Up + 1 
                if Counter_Vol_Up > DataPoint_Volume:
                    print("---Volume Up---")
                    Timer_Vol_Menu = time.time()
                    Counter_Vol_Up = 0
            else:
                Counter_Vol_Up = 0
            #Lower Vol
            if  50 < index[1] < 150  and 50 < index[0] < 150:
                Counter_Vol_Down = Counter_Vol_Down + 1 
                if Counter_Vol_Down > DataPoint_Volume:
                    print("---Volume Down---")
                    Timer_Vol_Menu = time.time()
                    Counter_Vol_Down = 0
            else:
                Counter_Vol_Down = 0
        
        
        
        #Inside Swipe Menu
        
        if Timer_Swipe_Menu > 0 :
           
            if (time.time() - Timer_Swipe_Menu) > Swipe_Menu_time: 
               Timer_Swipe_Menu = 0
               print("---Menu Timeout---")
            
            
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
                    print("--- Previous Song ----")
                    Counter_V1 = 0
                    Counter_H1 = 0  
                    Timer_Swipe_Menu = 0
                    Timer_Control = time.time()
                    
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
                    print("--- Next Song ----")
                    Counter_V2 = 0
                    Counter_H2 = 0 
                    Timer_Swipe_Menu = 0
                    Timer_Control = time.time()
            else:
                Timer_H2 = 0
                Counter_V2 = 0
        
    
    
    
        
    # We're done, stop the session. All buffered/waiting data is thrown
    # away. This call will block until the server has confirmed that the
    # session has ended.
    client.stop_session()

    # Calling stop_session before disconnect is not necessary as
    # disconnect will call stop_session if a session is started.

    # Remember to always call disconnect to do so gracefully
    client.disconnect()


if __name__ == "__main__":
    main()
