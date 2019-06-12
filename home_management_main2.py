#=============================================
#===============Initilization=================
#=============================================

#Setup and library including
from signal import pause
from time import sleep
import datetime
import time
cycle = True
actual_time = time.time()
actual_time2 = time.time()
tmp = 0
hum = 0
prs = 0
try:
    set_temp = set_temp
except:
    set_temp = 21
con_state = True
fire_al = True
blackout = True
door_lck = True
win1_t = True
win1_o = True
win2_t = True
win2_o = True
cooling = False
#GPIO setup
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Blackout detection
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Front door lock detection
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Window1 tilting detection
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Window1 opening detection
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Window2 opening detection
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Window2 tilting detection
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) #Fire alarm detection
GPIO.setup(26, GPIO.OUT) #Energy breaker in case of fire alarm
GPIO.setup(20, GPIO.OUT) #Socket breaker
GPIO.setup(21, GPIO.OUT) #Thermostat contact
GPIO.setup(21, GPIO.LOW)

#SenseHat setup
from sense_hat import SenseHat
hat = SenseHat()
hat.clear()
    
def db_transfer_datas (): #Hőmérséklet, páratartalom és légnyomás adatok adatbázisba mozgatása
    tmp = hat.get_temperature() 
    tmp = round(tmp,1)
    print (tmp, "'C")
    hum = hat.get_humidity()
    hum = round(hum,1)
    print (hum, "%")
    prs = hat.get_pressure()
    prs = round(prs,1)
    print (prs, "mBar")
    now = datetime.datetime.now()
    cdate = now.strftime("%Y-%m-%d")
    ctime = now.strftime("%H:%M:%S")
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       cursor = connection.cursor()
       cursor.execute("INSERT INTO datas VALUES (%s, %s, %s, %s, %s, %s)", (" ", cdate, ctime, tmp, hum, prs))
       connection.commit()
       print ("Record inserted successfully into the table datas")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into datas table {}".format(error))    
    
def db_transfer_fire (): #Tűzjelzés időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer   
       sql_insert_query = "INSERT INTO fire (date, time) VALUES (current_date, current_time)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table fire")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into fire table {}".format(error))
        
def db_transfer_blackout (): #áramszünet időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer   
       sql_insert_query = "INSERT INTO blackout (date, time) VALUES (current_date, current_time)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table blackout")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into blackout table {}".format(error))        
        
def db_transfer_door (door_state): #Ajtó nyitás/zárás időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       if door_state:
           sql_insert_query = "INSERT INTO Door (date, time, close, open) VALUES (current_date, current_time, 1,0)"
       else:
           sql_insert_query = "INSERT INTO Door (date, time, close, open) VALUES (current_date, current_time, 0,1)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table door")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into door table {}".format(error))
        
def db_transfer_win1t (win1t_state): #Ajtó nyitás/zárás időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       if win1t_state:
           sql_insert_query = "INSERT INTO win1t (date, time, close, open) VALUES (current_date, current_time, 1,0)"
       else:
           sql_insert_query = "INSERT INTO win1t (date, time, close, open) VALUES (current_date, current_time, 0,1)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table win1t")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into win1t table {}".format(error))
        
def db_transfer_win1o (win1o_state): #Ajtó nyitás/zárás időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       if win1o_state:
           sql_insert_query = "INSERT INTO win1o (date, time, close, open) VALUES (current_date, current_time, 1,0)"
       else:
           sql_insert_query = "INSERT INTO win1o (date, time, close, open) VALUES (current_date, current_time, 0,1)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table win1o")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into win1o table {}".format(error))        
  
def db_transfer_win2t (win2t_state): #Ajtó nyitás/zárás időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       if win2t_state:
           sql_insert_query = "INSERT INTO win2t (date, time, close, open) VALUES (current_date, current_time, 1,0)"
       else:
           sql_insert_query = "INSERT INTO win2t (date, time, close, open) VALUES (current_date, current_time, 0,1)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table win2t")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into win2t table {}".format(error))
        
def db_transfer_win2o (win2o_state): #Ajtó nyitás/zárás időpontjának adatbázisba mozgatása
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
    #Data transfer
       if win2o_state:
           sql_insert_query = "INSERT INTO win2o (date, time, close, open) VALUES (current_date, current_time, 1,0)"
       else:
           sql_insert_query = "INSERT INTO win2o (date, time, close, open) VALUES (current_date, current_time, 0,1)"
       cursor = connection.cursor()
       result  = cursor.execute(sql_insert_query)
       connection.commit()
       print ("Record inserted successfully into the table win2o")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed inserting record into win2o table {}".format(error))
        
def db_transfer_thermo (set_temp): #Thermosztát beállított értékének lekérdezése
    import mysql.connector
    from mysql.connector import Error
    from mysql.connector import errorcode
    try:
       connection = mysql.connector.connect(host='localhost',
                             database='phpmyadmin',
                             user='phpmyadmin',
                             password='raspberry')
       
       mycursor = connection.cursor()
    #Data transfer
       sql = "SELECT value FROM thermostat WHERE id=1"
       mycursor.execute(sql)
       myresult = mycursor.fetchone()
       set_temp = myresult[0]
       connection.commit()
       print ("Record red successfully from the table thermostat")
    except mysql.connector.Error as error :
        connection.rollback() #rollback if any exception occured
        print("Failed reading record from thermostat table {}".format(error))
    #Szabályzás
    act_tmp = hat.get_temperature()
    act_tmp = round(act_tmp,1)
    tmpl = (set_temp - 0.5)
    tmpl = round(tmpl,1)
    tmph = (set_temp + 0.5)
    tmph = round(tmph,1)
    if tmpl > act_tmp:#Fűtés bekapcsolása
        hat.set_pixel(6, 1, 0, 255, 0)
        hat.set_pixel(7, 1, 0, 0, 0)
        GPIO.setup(21, GPIO.HIGH)
        cooling = False
    else:#Szabályzási tartomány
        if (tmpl <= act_tmp) and (act_tmp <= tmph) and (GPIO.input(21)):
            hat.set_pixel(6, 1, 0, 255, 0)
            hat.set_pixel(7, 1, 0, 0, 0)  
            GPIO.setup(21, GPIO.HIGH)
        else:#Fűtés kikapcsolása
            hat.set_pixel(7, 1, 255, 0, 0)
            hat.set_pixel(6, 1, 0, 0, 0)
            GPIO.setup(21, GPIO.LOW)
            cooling = True        
      
#=============================================
#====================Body=====================
#=============================================
while cycle:
    #Tűzjelzés detektálás
    
    if GPIO.input(22): # van-e tűzjelzés (true: nincs, false:van) 
        hat.set_pixel(0, 0, 0, 255, 0)
        hat.set_pixel(1, 0, 0, 0, 0)
        hat.set_pixel(6, 0, 0, 255, 0)
        hat.set_pixel(7, 0, 0, 0, 0)
        GPIO.output(26, GPIO.HIGH)
        fire_al = False #Nincs tűzjelzés (flag)
    else:
        hat.set_pixel(1, 0, 255, 0, 0)
        hat.set_pixel(0, 0, 0, 0, 0)
        hat.set_pixel(7, 0, 255, 0, 0)
        hat.set_pixel(6, 0, 0, 0, 0)
        GPIO.output(26, GPIO.LOW)
        if not GPIO.input(22) and not fire_al:
            db_transfer_fire ()
        fire_al = True #Tűzjelzés van (flag)
        
    #Áramszünet detektálás
        
    if GPIO.input(5): # van-e áramszünet (true: nincs, false:van) 
        hat.set_pixel(0, 1, 0, 255, 0)
        hat.set_pixel(1, 1, 0, 0, 0)
        blackout=False #Nincs áramszünet (flag)
    else:
        hat.set_pixel(1, 1, 255, 0, 0)
        hat.set_pixel(0, 1, 0, 0, 0)
        if not GPIO.input(5) and not blackout:
            db_transfer_blackout ()
        blackout=True #Áramszünet van (flag)
    
    #Ajtó nyitás/zárás detektálás
        
    if GPIO.input(6): # bejárati ajtó zárva ven-e (true: nyitva, false:zárva) 
        hat.set_pixel(0, 2, 0, 255, 0)
        hat.set_pixel(1, 2, 0, 0, 0)
        if GPIO.input(6) and door_lck:
            door_state = False
            db_transfer_door (door_state)
        door_lck=False # Ajtó nyitva (flag)
    else:
        hat.set_pixel(1, 2, 255, 0, 0)
        hat.set_pixel(0, 2, 0, 0, 0)
        if not GPIO.input(6) and not door_lck:
            door_state = True
            db_transfer_door (door_state)
        door_lck=True # Ajtó zárva (flag)
    
    #Thermosztát vezérlés
    
    ticks2 = time.time()
    elapsed_time2 = ticks2 - actual_time2
    if elapsed_time2 > 10: #Fél óránkénti komfort adat frissítés
        actual_time2 = time.time()
        elapsed_time2 = 0
        db_transfer_thermo (set_temp)
    
    #1-es ablak nyitás/zárás detektálás
        
    if GPIO.input(12): # 1-es ablak bukóra nyitva ven-e (true: nyitva, false:zárva) 
        hat.set_pixel(0, 3, 0, 255, 0)
        hat.set_pixel(1, 3, 0, 0, 0)
        if GPIO.input(12) and win1_t:
            win1t_state = False
            db_transfer_win1t (win1t_state)
        win1_t=False # Ablak nyitva (flag)
    else:
        hat.set_pixel(1, 3, 255, 0, 0)
        hat.set_pixel(0, 3, 0, 0, 0)
        if not GPIO.input(12) and not win1_t:
            win1t_state = True
            db_transfer_win1t (win1t_state)
        win1_t=True # Ablak zárva (flag)
                
    if GPIO.input(13): # 1-es ablak nyitva van-e (true: nyitva, false:zárva) 
        hat.set_pixel(0, 4, 0, 255, 0)
        hat.set_pixel(1, 4, 0, 0, 0)
        if GPIO.input(13) and win1_o:
            win1o_state = False
            db_transfer_win1o (win1o_state)
        win1_o=False #Nitva (flag)
    else:
        hat.set_pixel(1, 4, 255, 0, 0)
        hat.set_pixel(0, 4, 0, 0, 0)
        if not GPIO.input(13) and not win1_o:
            win1o_state = True
            db_transfer_win1o (win1o_state)
        win1_o=True #Zárva (flag)

    #2-es ablak nyitás/zárás detektálás

    if GPIO.input(19): # 2-es ablak bukóra nyitva van-e (true: nyitva, false:zárva) 
        hat.set_pixel(0, 5, 0, 255, 0)
        hat.set_pixel(1, 5, 0, 0, 0)
        if GPIO.input(19) and win2_t:
            win2t_state = False
            db_transfer_win2t (win2t_state)
        win2_t=False #Nitva (flag)
    else:
        hat.set_pixel(1, 5, 255, 0, 0)
        hat.set_pixel(0, 5, 0, 0, 0)
        if not GPIO.input(19) and not win2_t:
            win2t_state = True
            db_transfer_win2t (win2t_state)
        win2_t=True #Zárva (flag)
                
    if GPIO.input(16): # 2-es ablak nyitva van-e (true: nyitva, false:zárva) 
        hat.set_pixel(0, 6, 0, 255, 0)
        hat.set_pixel(1, 6, 0, 0, 0)
        if GPIO.input(16) and win2_o:
            win2o_state = False
            db_transfer_win2o (win2o_state)
        win2_o=False #Nitva (flag)
    else:
        hat.set_pixel(1, 6, 255, 0, 0)
        hat.set_pixel(0, 6, 0, 0, 0)
        if not GPIO.input(16) and not win2_o:
            win2o_state = True
            db_transfer_win2o (win2o_state)
        win2_o=True #Zárva (flag)
        
    # Komfort adatok adatbázisba mentése

    ticks = time.time()
    elapsed_time = ticks - actual_time
    if elapsed_time > 300: #Fél óránkénti komfort adat frissítés(1800)
        actual_time = time.time()
        elapsed_time = 0
        db_transfer_datas ()
         