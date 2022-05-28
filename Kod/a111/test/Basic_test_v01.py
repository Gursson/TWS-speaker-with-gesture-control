import acconeer.exptool as et
import numpy as np
import time

def main():
    # To simplify the examples, we use a generic argument parser. It
    # lets you choose between UART/SPI/socket, set which sensor(s) to
    # use, and the verbosity level of the logging.
    args = et.a111.ExampleArgumentParser().parse_args()

    # The client logs using the logging module with a logger named
    # acconeer.exptool.*. We call another helper function which sets up
    # the logging according to the verbosity level set in the arguments:
    # -q  or --quiet:   ERROR   (typically not used)
    # default:          WARNING
    # -v  or --verbose: INFO
    # -vv or --debug:   DEBUG
    et.utils.config_logging(args)

    # Pick client depending on whether socket, SPI, or UART is chosen
    # from the command line.
    client = et.a111.Client(**et.a111.get_client_args(args))

    # Create a configuration to run on the sensor. A good first choice
    # is the envelope service, so let's pick that one.
    config = et.a111.EnvelopeServiceConfig()

    # In all examples, we let you set the sensor(s) via the command line
    #config.sensor = args.sensors
    config.sensor = [1,2]

    #config.sensor
    # Set the measurement range [meter]
    config.range_interval = [0.1, 0.3]

    # Set the target measurement rate [Hz]
    config.update_rate = 15

    # Other configuration options might be available. Check out the
    # example for the corresponding service/detector to see more.

    client.connect()

    # In most cases, explicitly calling connect is not necessary as
    # setup_session below will call connect if not already connected.

    # Set up the session with the config we created. If all goes well,
    # some information/metadata for the configured session is returned.
    session_info = client.setup_session(config)
    print("Session info:\n", session_info, "\n")

    # Now would be the time to set up plotting, signal processing, etc.

    # Start the session. This call will block until the sensor has
    # confirmed that it has started.
    client.start_session()

    # Alternatively, start_session can be given the config instead. In
    # that case, the client will call setup_session(config) for you
    # before starting the session. For example:
    # session_info = client.start_session(config)
    # As this will call setup_session in the background, this will also
    # connect if not already connected.

    # In this simple example, we just want to get a couple of sweeps.
    # To get a sweep, call get_next. get_next will block until the sweep
    # is recieved. Some information/metadata is returned together with
    # the data.

    interrupt_handler = et.utils.ExampleInterruptHandler()
    print("Press Ctrl-C to end session\n")

    #sum_index = 0
    #lengd = 10
    #init :

    Menu_counter = 0
    Volume_up_counter = 0
    Volume_down_counter = 0
    Pause_Play_counter = 0
    Swipe_right_counter = 0
    Swipe_left_counter = 0
    Menu_timer = 0 #Counter for time in menu
    cycles = 0 #
    Menu_timer_start = 0 #Init menu Menu
    Swipe_timer_right = 0
    Swipe_timer_left = 0
    Menu_swipe = False
    right_swipe_detected = False
    left_swipe_detected = False

    #Parameters:
    DataPoint_Menu = 15
    Menu_time = 15
    DataPoint_Volume = 20
    DataPoint_Pause_Play = 20
    DataPoint_Swipe = 3


    while not interrupt_handler.got_signal:#for i in range(lengd):
        data_info, data = client.get_next()


        index = np.argmax(data, axis = 1, out = None);
        print(index)

        #Menu Start 
        if index[1] > 70 and Swipe_timer_right == 0 and Menu_timer == 0:
            Swipe_right_counter = Swipe_right_counter + 1
            if Swipe_right_counter > DataPoint_Swipe:
                print("Menu swipe detected")

                Swipe_timer_right = time.time()


        elif (time.time() - Swipe_timer_right) > 1:
            Swipe_timer_right = 0 
        else:
            Swipe_right_counter = 0

        if index[0] > 70 and 0 < (time.time() - Swipe_timer_right) < 1 and index[1] < 100:
            Swipe_left_counter = Swipe_left_counter + 1
            if Swipe_left_counter > DataPoint_Swipe:
                print("--- Menu ----")
                Swipe_timer_right = 0
                Menu_timer = time.time()
        else:
            Swipe_left_counter = 0
            
        #Inside Menu
        
        if Menu_timer > 0 :
            #print(time.time() - Menu_timer)
            if (time.time() - Menu_timer) > Menu_time:
                Menu_timer = 0
                print("---Menu Timeout---")
            
            
            #CHECK SWIPE RIGHT HAND (PREVIOUS SONG) #SAME AS MENU
            elif index[1] > 70 and Swipe_timer_right == 0:
                Swipe_right_counter = Swipe_right_counter + 1
                if Swipe_right_counter > DataPoint_Swipe:
                    print("Right Sweep")

                    Swipe_timer_right = time.time()


            elif (time.time() - Swipe_timer_right) > 1:
                Swipe_timer_right = 0 
            else:
                Swipe_right_counter = 0
            
            if index[0] > 70 and 0 < (time.time() - Swipe_timer_right) < 1 and index[1] < 100:
                Swipe_left_counter = Swipe_left_counter + 1
                if Swipe_left_counter > DataPoint_Swipe:
                    print("--- Previous Song ----")
                    Swipe_timer_right = 0
                    Menu_timer = time.time()
            else:
                Swipe_left_counter = 0
                
            """      
            #CHECK SWIPE LEFT HAND (NEXT SONG)
            if index[0] > 70 and Swipe_timer_right == 0:
                Swipe_right_counter = Swipe_right_counter + 1
                if Swipe_right_counter > DataPoint_Swipe:
                    print("Next Song -- Left Sweep")

                    Swipe_timer_right = time.time()


            elif (time.time() - Swipe_timer_right) > 2:
                Swipe_timer_right = 0 
            else:
                Swipe_right_counter = 0
            
            if index[1] > 70 and 0 < (time.time() - Swipe_timer_right) < 2 and index[0] < 100:
                Swipe_left_counter = Swipe_left_counter + 1
                if Swipe_left_counter > DataPoint_Swipe:
                    print("--- Next Song ----")
                    Swipe_timer_right = 0
                    Menu_timer = time.time()
            else:
                Swipe_left_counter = 0
            """
        
        
        
        
        

        #
        # if index[1] > 70 and Menu_timer_start == 0:
        #     Swipe_right_counter = Swipe_right_counter + 1
        #     if Swipe_right_counter > DataPoint_Swipe:
        #         print("Right swipe detected")
        #         Menu_swipe = True
        #         Swipe_right_counter = 0
        #         Menu_timer_start = time.time() #Start time for menu.
        #
        # if Menu_swipe == True:
        #     if index[0] > 70:
        #         Swipe_left_counter = Swipe_left_counter + 1
        #         print(Swipe_left_counter)
        #         if Swipe_left_counter > DataPoint_Swipe:
        #             print("Menu------------------------------")
        #             Menu_swipe = False
        #             Swipe_left_counter = 0
        # else:
        #
        #
        #
        #
        #
        # #Check if hand is in place, go in menu
        # if 70 < index[0] < 120 and Menu_timer_start == 0: #Menu range
        #     Menu_counter = Menu_counter + 1
        #
        #     if Menu_counter == DataPoint_Menu: # Data points in row to go into menu
        #         print("Welcome to the Menu")
        #         #time.sleep(2) #Wait for 1 sec before registrate input
        #         Menu_counter = 0 #reset menu counter
        #         Menu_timer_start = time.time() #Start time for menu.
        #
        # else:
        #     Menu_counter = 0
        #
        #
        # if Menu_timer_start > 0: #Inne i menyn
        #
        #     if (time.time() - Menu_timer_start) > MenuTime: #Meny timeout
        #         Menu_timer_start = 0
        #         print("Menu timeout")
        #
        #     elif 70 < index[0] < 150 and 70 < index[1] < 150: #Volume up interval
        #         Pause_Play_counter = Pause_Play_counter + 1
        #         if Pause_Play_counter == DataPoint_Pause_Play:
        #             Menu_timer_start = time.time() # Reset menu timer
        #             Pause_Play_counter = 0
        #             print("Pause/Play")
        #     #Hand is high, increase volume
        #     elif 260 < index[0] < 414: #Volume up interval
        #         Volume_up_counter = Volume_up_counter + 1
        #         if Volume_up_counter == DataPoint_Volume:
        #             Menu_timer_start = time.time() # Reset menu timer
        #             Volume_up_counter = 0
        #             print("Volume up+")
        #
        #     #Hand is low, decrease volume
        #     elif 70 < index[0] < 150:#Volyume down interval
        #         Volume_down_counter = Volume_down_counter + 1
        #         if Volume_down_counter == DataPoint_Volume:
        #             Menu_timer_start = time.time()
        #             Volume_down_counter = 0
        #             print("Volume down-")
        #
        #     else:
        #         Volume_up_counter = 0
        #         Volume_down_counter = 0
        #         Pause_Play_counter = 0

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
