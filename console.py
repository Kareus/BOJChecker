import os
import platform
import urllib.request
import BOJParser

users = []
userData = dict()

def wait():
    try:
        os.system('pause') #windows
    except:
        os.system('read -p "Press any key to continue"') #linux
    return

def clear():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')\
    
def console_adduser():
    while True:
        clear()
        print('Current Users:',end=' ')
        for i in range(len(users) - 1):
            print(users[i], end=', ')

        if users:
            print(users[-1], '\n')
        else:
            print('\n')

        print("Input users to add. ex) 'username', 'username1,username2'  input '0' to exit")

        cnt = 0
        u = input("Users: ")
        if u == '0':
            break

        u = u.split(',')
        for name in u:
            if name == '0':
                print('Try exit code in single')
                continue

            if name in users:
                print(name,'is already in user list!')
                continue

            data = BOJParser.parseUser(name)
            if not data:
                print(name,'is not found!')
                continue

            users.append(name)
            userData[name] = data
            cnt += 1

        print(cnt, "users added\n")        
        wait()

    return True

def console_checkproblem():
    clear()
    print("Input problem numbers to check. ex) '1000', '1001,1002'  input '0' to exit")
    while True:
        ps = input("Problems: ")
        if ps == '0':
            break

        print()
        ps = ps.split(',')
        for problem in ps:
            if ps == '0':
                print('Try exit code in single')
                continue

            try:
                urllib.request.urlopen("https://www.acmicpc.net/problem/"+problem)
            except urllib.error.HTTPError:
                print("Problem", problem, "not found!")
                continue

            print('Problem:', problem, '\n')

            for u in users:
                if problem in userData[u]['problems']:
                    print(u, ':', 'O')
                else:
                    print(u, ':', 'X')

            print()

    return True

            
def console_main():
    clear()
    print('#Main menu')
    print('1: Add Users')
    print('2: Check problems')
    print('3: View User Profile')
    print('4: Remove All Users from lists')
    print('0: Exit\n')

    print('Current Users:',end=' ')
    for i in range(len(users) - 1):
        print(users[i], end=', ')

    if users:
        print(users[-1], '\n')
    else:
        print('\n')

    while True:
        try:
            command = int(input("Input: "))
        except:
            print("Wrong command")
            
        if command == 1:
            return console_adduser()
        elif command == 2:
            return console_checkproblem()
        elif command == 3:
            for u in users:
                print("Username:", u)
                print("Tier:",userData[u]['tier'])
                print("Problem Solved:", len(userData[u]['problems']),'\n')

            wait()
            return True
        elif command == 4:
            users.clear()
            return True
        elif command == 0:
            return False
        else:
            print("Wrong command")