def extractdata():
    
    import bs4
    from urllib.request import Request, urlopen
    import numpy as np

    tsawebsite = 'https://www.tsa.gov/coronavirus/passenger-throughput'

    # Read data from TSA Website
    webpage = Request(tsawebsite, headers={'User-Agent': 'Mozilla/5.0 Chrome/28.0.1464.0'})
    sauce = str(urlopen(webpage).read())
    sauce = sauce.encode('utf-8', 'ignore').decode('utf-8')
    soup = bs4.BeautifulSoup(sauce,'html.parser')

    # Parse data looking for relevant table
    data = soup.find('table')
    data = data.find_all('td')
    data = [element.get_text() for element in data]
    data = data[3:]

    # Isolate the 3 relevant columns of the table
    dates = data[0::3]
    now = [int(element.replace(',','')) for element in data[1::3]]
    before = [int(element.replace(',','')) for element in data[2::3]]

    # Make variables for results
    today = now[0]
    oneyearago = before[0]
    yesterday = now[1]
    percent_1yrago = round((int(today)/int(oneyearago))*100,2)
    weekly_average = int(np.mean(now[0:6]))
    last_7daystotal = sum(now[0:6])
    previous_7daystotal = sum(now[7:13])
    weekly_change = round(((last_7daystotal/previous_7daystotal)-1)*100,2)
    week_highest = np.max(now[0:6])
    week_lowest = np.min(now[0:6])
    highest = np.max(now)
    lowest = np.min(now)

    # Final message to be sent
    string_result = 'TSA Flier Analysis \n Today: {:,} fliers\n Yesterday: {:,} fliers\n 1 Year Ago: {:,} fliers\n Percent from 1r ago: {}%\n Weekly Average: {:,} fliers\n Last 7 days: {:,} fliers\n Prev 7 days: {:,} fliers\n Weekly Change: {}%\n Week Highest: {:,} fliers\n Week Lowest: {:,} fliers\n Total Highest: {:,} fliers\n Total Lowest: {:,} fliers'.format(today,yesterday,oneyearago,percent_1yrago,weekly_average,last_7daystotal,previous_7daystotal,weekly_change,week_highest, week_lowest, highest,lowest)

    sendtext(string_result)

def sendtext(textcontent):

    from twilio.rest import Client
    import os 

    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    auth_token = os.environ['TWILIO_AUTH_TOKEN']
    phone_number = os.environ['TWILIO_PHONE_NUMBER']
 
    client = Client(account_sid, auth_token) 
    
    message = client.messages.create( 
                                from_=phone_number,  
                                body=textcontent,      
                                to=os.environ['MY_PHONE_NUMBER'] 
                            ) 
    
    print('Message Sent')

extractdata()




