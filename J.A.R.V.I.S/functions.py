# ---------------- Dependency Startups: ------------

try:
    import pyttsx3
    import speech_recognition as sr
    import datetime
    import wikipedia
    import webbrowser
    import os
    import smtplib
    import private
    from email.message import EmailMessage
except Exception as e:
    print("Cannot operate without dependencies, please\n"
          "install:\n"
          "-> pyttsx3\n"
          "-> speechRecognition\n"
          "-> datetime\n"
          "-> wikipedia\n"
          "-> webbrowser\n"
          "-> os\n"
          "-> smtplib\n"
          "-> PyAudio (using pipwin)\n"
          "-> email\n"
          ""
          "please install all these python modules in your\n"
          "envoirment.")
    result = input("may I install for you? (y/n): ")
    if result.lower() == 'y':
        # install proccess:
        import os
        os.system("pip install pipwin")
        os.system("pipwin install PyAudio")
        os.system("pip install pyttsx3 speechRecognition wikipedia webbrowser")
        email = input("please enter your email: (needed for emailing feature): ")
        password = input("please enter your password: (so that I can mail on behalf of you): ")
        print("Dont worry, ill keep your password safe, I promise.")
        print("Can you also please check your accounts to be usable with smtp mail? it will save alot of headaches later.")
        f = open("private.py", "w")
        f.write(f"""\
email = {email}
password = {password}        
""")
        f.close()

    exit(0)

# -------------- Initialization: ---------------
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# -------------- Primary Functions: ----------------


def speak(text):
    """ The speak function in our application will pronounce this "text" string """
    print(str(text) + '\n')
    engine.say(text)
    engine.runAndWait()


def storage(action, new_data=''):
    """ This Function is there to store permanent storage for varios tasks of the assistant"""
    if action == 'return-data':
        storage = open('storage.txt', 'r')
        return storage.readlines()
    if action == 'add-data':
        storage = open('storage.txt', 'a')
        storage.write(str(new_data) + '\n')
        storage.close()


def current_date():
    """ This function is here to tell the current date to JARVIS """
    num_to_month = {
        '1': 'January',
        '2': 'February',
        '3': 'March',
        '4': 'April',
        '5': 'May',
        '6': 'June',
        '7': 'July',
        '8': 'August',
        '9': 'September',
        '10': 'October',
        '11': 'November',
        '12': 'December',
    }
    now = str(datetime.datetime.now()).split()[0]
    date = f'{num_to_month[now[5:7]]} {now[8:10]}, {now[0:4]}'
    return date


def greet(user):
    """ This function greet's the user when called """
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak(f'Good Morning, {user}')
    elif 12 <= hour < 18:
        speak(f'Good Afternoon, {user}')
    else:
        speak(f'Good Evening, {user}')

    speak(f"Today's {current_date()}")
    speak(f'What would you like me to do today?')


def current_time():
    now = datetime.datetime.now()
    return now.strftime('%I:%M')


def command():
    """ This function takes command from the user and outputs a string for JARVIS to use """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('|---->')
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language='en-us')
        print(f'> {query}')
    except:
        speak("Sorry, what did you say?")
        query = None

    return query


def filter_query(query):
    """ This function filters a query given to JARVIS, and then gets rid of useless words """
    list = []
    for i in query:
        if i.lower() == 'wikipedia':
            list.append('')
        elif i.lower() == 'jarvis':
            list.append('')
        elif i.lower() == 'search':
            list.append('')
        elif i.lower() == 'up':
            list.append('')
        elif i.lower() == 'on':
            list.append('')
        elif i.lower() == 'hey':
            list.append('')
        else:
            list.append(i)
    string = ' '.join(list)

    return string


def browse(url):
    """ Browse google for a url given """
    path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(path).open(url)


def show_contacts():
    """ Show all the contacts of the user """
    file = open('storage.txt', 'r')
    return_list = []
    for i in file:
        if i.split()[0] != 'user':
            return_list.append(f'{i.split()[0]}: {i.split()[1]}')
    return return_list


def send_mail(send_to, body, subject):
    """ Send a mail to a specified gmail on Google """
    server = smtplib.SMTP("SMTP.gmail.com", 587)
    server.starttls()
    server.login(private.email, private.password)
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = private.email
    msg['To'] = send_to
    msg.set_content(body)

    speak("Sending Message...")
    server.send_message(msg)
    speak("Message Sent.")
