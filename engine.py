# ---------------- Importing Dependencies: --------------
from functions import *

speak("INITIALIZING JARVIS...")

# ----------------- User Initialization: ---------------
try:
    user = storage('return-data')[0]
except:
    user = ''

if 'user = ' in user:
    greet(user.split()[2])
else:
    speak('Hi, my name is JARVIS, what is your name?')
    username = input('Your name> ')
    print('\n')
    storage('add-data', f'user = {username}')
    user = storage('return-data')[0]
    greet(user.split()[2])

# ----------------- Primary Brain: ----------------

while True:
    query = command()

    if query is None:
        print('')

    # ------------------ Logic: ----------------
    # search wikipedia:

    elif 'wikipedia' in query.lower():
        speak('Searching Wikipedia...')
        query = query.split()
        try:
            results = wikipedia.summary(filter_query(query), sentences=5)
        except:
            results = f'Sorry, could not find results regarding {filter_query(query)}'
        speak(results)

    # open a website using google:

    elif 'open' in query.lower() and ('.' in query.lower() or 'dot' in query.lower()) and 'google' in query.lower():
        """this function is very specific on what format you say, you must start with: 
        open (whatever website with domain-name) in google"""
        speak(f"Is this the URL:\n\t{query.split()[1]}")
        res = input("(y/n)> ")
        url = query.split()[1]
        if res.lower() == 'n':
            for i in range(2):
                speak("What URL would you like to open?")
                query = command()
                while query is None:
                    query = command()
                speak(f"Is this the URL:\n\t{query}")
                res = input("(y/n)> ")
                if res.lower() == 'y':
                    break
            speak("Can you please type your desired URL?")
            url = input("> ")

        speak(f'Opening {url}...')
        try:
            browse(url)
        except:
            speak(f"Sorry, cant open {url}")

    # add people's email in contacts:

    elif 'add' in query.lower() and 'contacts' in query.lower():
        speak("Please type in an email address:")
        email = input('> ')
        speak("Give a convenient name to that email by saying it:")
        while True:
            nickname = command()
            speak('Is this what you would like to name it?')
            next = command()
            if next.lower() == 'yes':
                speak('ok')
                break
            if next.lower() == 'no':
                speak("Give a convenient name to that email by saying it:")
        storage('add-data', f'{nickname} {email}')

    # show saved contacts:

    elif 'show' in query.lower() and 'contacts' in query.lower():
        for i in show_contacts():
            speak(i)

    # send emails via gmail:

    elif 'send' in query.lower() and 'mail' in query.lower():
        not_in_contacts = None
        speak('Who would you like to send an email? Please type it out:')
        who = input('(use nicknames from contacts)> ')
        contacts = show_contacts()
        for i in contacts:
            counter = 0
            if who in i:
                send_to = contacts[counter].split()[1]
                not_in_contacts = False
                break
            counter += 1
        if not_in_contacts is None:
            send_to = who

        speak('Your body:')
        body = command().capitalize() + '.'

        speak('Your subject:')
        subject = command()

        send_mail(send_to, body, subject)

    # tell the current time:

    elif 'the time' in query.lower():
        speak(f"Its currently {current_time()}")

    # open pycharm:

    elif 'open vs code' in query.lower() or 'open code' in query.lower() or 'code editor' in query.lower() or 'ide' in query.lower():
        speak("Opening VS Code...")
        os.system("code")
    
    # pause the system:

    elif 'pause' in query.lower():
        speak("Pausing System...")
        input("Press Enter to Resume...")
        speak("Resuming System...")

    # exit Jarvis:

    elif 'exit' in query.lower() or 'quit' in query.lower() or 'shut down' in query.lower() or 'die' in query.lower():
        speak('Exiting JARVIS...')
        break
