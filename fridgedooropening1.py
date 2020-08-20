import conf, json, time, math, statistics
from boltiot import Sms, Bolt, Email


def compute_bounds(history_data,frame_size,factor):
    if len(history_data)<frame_size :
        return None

    if len(history_data)>frame_size :
        del history_data[0:len(history_data)-frame_size]
    Mn=statistics.mean(history_data)
    Variance=0
    for data in history_data :
        Variance += math.pow((data-Mn),2)
    Zn = factor * math.sqrt(Variance / frame_size)
    High_bound = history_data[frame_size-1]+Zn
    Low_Bound = history_data[frame_size-1]-Zn
    return [High_bound,Low_Bound]

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)
sms_whatsapp = Sms(conf.SSID, conf.AUTH_TOKEN, conf.TO_WHATSAPP, conf.FROM_WHATSAPP)
mailer = Email(conf.MAILGUN_API_KEY, conf.SANDBOX_URL, conf.SENDER_EMAIL, conf.RECIPIENT_EMAIL)
history_data=[]

while True:
    response = mybolt.analogRead('A0')
    response1 = mybolt.analogRead('A0')
    response2 = mybolt.analogRead('A0')
    data = json.loads(response)
    if data['success'] != '1':
        print("There was an error while retriving the data.")
        print("This is the error:"+data['value'])
        time.sleep(5)
        continue

    sensor_value1 = int(data['value'])
    sensor_value1 = sensor_value1/10.24
    print ("The current Temparature of your Refrigarator is "+ str(sensor_value1)+" degree celsious. And the Sensor Value is "+data['value'])
    sensor_value=0
    try:
        sensor_value = int(data['value'])
    except e:
        print("There was an error while parsing the response: ",e)
        continue

    bound = compute_bounds(history_data,conf.FRAME_SIZE,conf.MUL_FACTOR)
    if not bound:
        required_data_count=conf.FRAME_SIZE-len(history_data)
        print("Not enough data to compute Z-score. Need ",required_data_count," more data points")
        history_data.append(int(data['value']))
        time.sleep(5)
        continue

    try:
        if sensor_value > bound[0] :
            sensor_value1 = sensor_value/10.24
            print ("The Temparature level has been INCREASED suddenly.Sending SMS")
            response = sms.send_sms("Someone Opened the fridge door. The Current temperature is " + str(sensor_value1)+ " degree celsious")
            response1 = mailer.send_email("RED Alert", "Someone opened the fridge door. Because The Temparature of your Refrigarator has been INCREASED suddenly. The Current temperature is " + str(sensor_value1)+" degree celsious")
            response2 = sms_whatsapp.send_sms("Someone opened the fridge door. Because The Temparature of your Refrigarator has been INCREASED suddenly. The Current temperature sensor value is " + str(sensor_value1)+ " degree celsious")
            print("This is the response for SMS ",response)
            print("This is the response for EMAIL ",response1)
            print("This is the response for WHATSAPP ",response2)
        history_data.append(sensor_value);
    except Exception as e:
        print ("Error",e)
    
