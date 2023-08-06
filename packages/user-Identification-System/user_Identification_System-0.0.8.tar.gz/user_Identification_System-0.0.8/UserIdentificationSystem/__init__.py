import sqlite3
import secrets

def encryt(prompt):
    # The key and value
    key = ['>', '*', 's', 'z', 'E', '3', ';', 'f', '?', '0', 'U', 'N', '}', '"', '7', 'x', '=', '(', 'G', '$', 'L', 'K', 'O', ':', 'q', 'a', '1', '4', '!', 'X', '6', 'P', ',', '%', '|', 'b', 'I', 'y', 'g', "'", '2', 'd', 'S', 'u', 'V', 'H', '<', 'p', 'A', 'o', 'Z', 'Y', '-', 'e', 'B', '#', 'c', '`', 'D', 'M', '5', 'k', 'R', 'w', '+', '~', ' ', ']', 'T', '{', 'h', 'W', '&', '/', 'n', 'r', '\\', '_', 'i', 'm', 't', 'j', '[', 'v', 'J', '@', '^', 'Q', '8', '9', 'F', '.', ')', 'l', 'C']
    value = ['@', '&', "'", '0', '!', '7', '1', '}', 'B', 'I', '#', '2', '$', '.', 'A', '4', 'Y', '^', 'r', 'M', 'X', '/', 'g', 'c', 'y', '9', 'G', 'T', ']', 'p', '*', ')', 'D', 'O', 'Q', '6', 'q', 'z', 'o', '?', '-', '%', 'C', '<', '3', 'N', 's', '8', 'w', 'P', 'n', 'b', 'R', '"', '5', 'h', '>', 'm', 'L', 'W', 'i', ';', '=', 'x', '`', 'H', '_', 'd', 'J', 'k', ':', '~', 'a', 'E', 't', 'K', 'U', 'l', '{', 'F', 'e', 'f', ' ', 'S', ',', '[', '+', '|', 'u', 'v', 'Z', 'j', 'V', '\\', '(']    

    # Convert the prompt to list
    desire = list(prompt)

    # Make it encrypted
    encrypted_word = ""
    for i in desire:
        index = key.index(i)
        encrypted_letter = value[index]
        encrypted_word += encrypted_letter

    # Salt the encrypted word
    trick_index = len(prompt) % 2
    encrypted_word = list(encrypted_word)
    encrypted_word.insert(trick_index, "e")
    encrypted_word = "".join(encrypted_word)

    # Returns encrypted word
    return encrypted_word

class Basic():
    __connection = None
    __c = None

    def __init__(self, filename):
        self.username = None
        self.filename = filename

        global __connection
        global __c

        __connection = sqlite3.connect("{}.db".format(filename))
        __c = __connection.cursor()
        __c.execute("""CREATE TABLE IF NOT EXISTS account (
            username text,
            password text
        )
        """)
        __connection.commit()

    def signup(self, username=None, password=None, autotask=False):
        global __c
        global __connection

        if autotask == False:
            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()
            users = [i[0] for i in users]

            if username not in users:
                password = encryt(password)
                __c.execute("INSERT INTO account VALUES(?,?)", (username, password))
                __connection.commit()
                return True
            else:
                return False
        else:
            username1 = input("Please make a username: ")
            password1 = input("Please make a password for security: ")

            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            users = [i[0] for i in users]

            if username1 in users:
                while True:
                    username1 = input("The username you entered is already in use. Please make another one: ")
                    if username1 not in users:
                        break

            print("This username is perfect")

            password1 = encryt(password1)

            __c.execute("INSERT INTO account VALUES(?,?)", (username1, password1))
            __connection.commit()
            self.username = username1
            return True

    def login(self, username=None, password=None, autotask=False):
        global __c
        global __connection

        if not autotask:
            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            password = encryt(password)
            permission = False
            for i in users:
                if (i[0] == username) and (i[1] == password):
                    permission = True
                    break

            return permission
        else:
            username1 = input("Please enter your username: ")
            self.username = username1

            password1 = input("Please enter your password: ")
            password1 = encryt(password1)

            __c.execute("SELECT * FROM account")
            users = __c.fetchall()
            __connection.commit()

            permission = False
            for i in users:
                if (i[0] == username1) and (i[1] == password1):
                    permission = True
                    break

            return permission

    def deluser(self, username=None, password=None, autotask=False):
        global __c
        global __connection

        test = Basic(self.filename)
        if autotask == False:
            if test.login(username, password):
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()
                return True
            else:
                return False
        else:
            username = input("Please enter your username: ")
            self.username = username

            password = input("Please enter your password for confirmation: ")

            if test.login(username, password):
                password = input("Please enter your password again for confirmation: ")
                if test.login(username, password):
                    __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                    __connection.commit()
                    return True
                else:
                    return False
            else:
                return False
    
    def usernames(self):
        global __c
        global __connection

        __c.execute("SELECT * FROM account")
        lst = __c.fetchall()
        __connection.commit()

        lst = [i[0] for i in lst]
        return lst

    def username_exists(self, username):
        global __c
        global __connection

        __c.execute("SELECT username FROM account")
        lst = __c.fetchall()
        __connection.commit()
        lst = [i[0] for i in lst]
        
        if username in lst:
            return True
        else:
            return False

    def secure(self):
        global __connection
        __connection.close()

class ExtraPass():
    __connection = None
    __c = None

    def __init__(self, filename):
        self.filename = filename
        self.username = None

        global __connection
        global __c

        __connection = sqlite3.connect("{}.db".format(filename))
        __c = __connection.cursor()
        __c.execute("""CREATE TABLE IF NOT EXISTS account (
            username text,
            password text,
            extra text
        )""")

    def login(self, username=None, password=None, extra=None, autotask=False):
        global __connection
        global __c

        if autotask == False:
            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            password = encryt(password)
            extra = encryt(extra)

            permission = False
            for i in lst:
                if (i[0] == username) and (i[1] == password) and (i[2] == extra):
                    permission = True
                    break

            return permission
        else:
            username = input("Please enter your username: ")
            password = input("Please enter your password: ")
            extra = input("Please enter the extra layer of password you added: ")

            password = encryt(password)
            extra = encryt(extra)

            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            permission = False
            for i in lst:
                if (i[0] == username) and (i[1] == password) and (i[2] == extra):
                    permission = True
                    break
            if permission:
                self.username = username
            return permission

    def signup(self, username=None, password=None, extra=None, autotask=False):
        global __connection
        global __c

        if autotask == False:
            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            lst = [i[0] for i in lst]

            if username in lst:
                return False
            else:
                password = encryt(password)
                extra = encryt(extra)

                __c.execute("INSERT INTO account VALUES (?,?,?)", (username, password, extra))
                __connection.commit()
                return True
        else:
            username = input("Please make a username: ")
            password = input("Please make a password: ")
            extra = input("Please enter another password that can be different for extra layer of security: ")

            password = encryt(password)
            extra = encryt(extra)

            __c.execute("SELECT * FROM account")
            lst = __c.fetchall()
            __connection.commit()

            lst = [i[0] for i in lst]

            if username in lst:
                while True:
                    username = input("The username you entered is already in use. Please enter another one: ")
                    if username not in lst:
                        break
                    else:
                        continue
            print("This username is perfect!")

            __c.execute("INSERT INTO account VALUES (?,?,?)", (username, password, extra))
            __connection.commit()
            self.username = username
            return True


    def deluser(self, username=None, password=None, extra=None, autotask=False):
        global __c
        global __connection

        test = ExtraPass(self.filename)
        if autotask == False:
            if test.login(username, password, extra):
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()
                return True
            else:
                return False
        else:
            username = input("Please enter your username: ")
            password = input("Please enter your password for confirmation: ")
            extra = input("Please enter the password you gave for extra layer (Password 2): ")

            if test.login(username, password, extra):
                global username1
                username1 = username
                __c.execute("DELETE FROM account WHERE username = '{}'".format(username))
                __connection.commit()

                self.username = username
                return True
            else:
                return False

    def usernames(self):
        global __c
        global __connection

        __c.execute("SELECT * FROM account")
        lst = __c.fetchall()
        __connection.commit()

        lst = [i[0] for i in lst]
        return lst

    def username_exists(self, username):
        global __connection
        global __c

        __c.execute("SELECT username FROM account")
        lst = __c.fetchall()
        __connection.commit()
        lst = [i[0] for i in lst]
       
        if username in lst:
            return True
        else:
            return False

    def secure(self):
        global __connection
        __connection.close()

def passgen(length=10, caplock="mix"):
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "h", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    symbols = ["@", "#", "%", "!", "*", ">", "<", "$"]
    
    letter_loop = length - 5

    generartor = secrets.SystemRandom()
    result = []
    for i in range(letter_loop):
        a = generartor.choice(letters)
        if caplock == True:
            a = a.upper()
        elif caplock == False:
            a = a.lower()
        else:
            pass
        result.append(a)

    result.append(generartor.choice(symbols))

    for i in range(4):
        a = generartor.choice(numbers)
        result.append(a)


    result = [str(i) for i in result]

    return "".join(result)