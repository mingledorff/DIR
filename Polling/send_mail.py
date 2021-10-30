from typing import List
import os

import yagmail

def parse_data(filename:str) -> List:
    ''' Return a list of Tuples: (name, email, language)

        filename: Name of file. 
        return: List of tuples.
    '''

    data = []

    with open(filename, 'r') as f:
        lines = f.read().splitlines()
        
        for line in lines:
            words = line.split(';')
            user = words[0]
            name = user[:user.find(' ')]
            email = user[user.find('<')+1: -1]
            language = words[-1]

            data.append((name, email, language))

    return data

def send_mail(data:List, boildplate) -> None:
    ''' Send mail to the users. 

        data: List of Tuples (name, email, language)
        return: None
    '''
    my_address = "fdac2021@gmail.com"
    pin = "tulsgdlrvkrdpdsi"
    to = "dlomaxpersonal@gmail.com"
    subject = "Quick poll"

    with open(boilerplate, 'r') as f:
        s = f.read()
        
        for d in data:
            message = s
            name, email, language = d[0], d[1], d[2]

            message = message.replace("USERNAME", name)
            message = message.replace("LANGUAGE", language)

            with yagmail.SMTP(my_address, pin) as yag:
                yag.send(email, subject, message)
                print('Sent email successfully')

if __name__ == "__main__":
    datafile = os.path.abspath(os.path.dirname(__file__)) + "/Authors/test.txt"
    boilerplate = os.path.abspath(os.path.dirname(__file__)) + "/boilerplate.txt"
    data = parse_data(datafile)

    send_mail(data, boilerplate)