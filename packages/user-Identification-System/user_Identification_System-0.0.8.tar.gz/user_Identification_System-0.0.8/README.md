# User Identifier System (uis) 
_____________________________
User Identifier System is a tool you can use to create a cool and easy login and signup system.

## Why to use it?
1. It is really easy to use.
2. All of the users detail is stored safely so other people can't peek in easily. 

## Contant me
My email: **miskiacuberayaan2509@gmail.com**  
My YouTube channel: **[Ayaan Imran Saleem](https://www.youtube.com/channel/UCbC2N-Q_3pGLJMIiMniCutA)**

# Guide on using uis
User Identifier System is basically a tool to help you create a login and signup system!


# Basic system
## Import

```python
import UserIdentificationSystem as uis
```

## Functions 
### setup()
To start the setup, we need to create an instance of the Basic() class. In the Basic class, you need to pass in a filename witch will be storing your user's credentials.
```python
controller = uis.Basic("users")
```
**Note:** When you will run your programme, it will create a database file that will be stored in you current working directory

### Some details
1. **controller.username**  
This will allow you to get the user's name when you will use autotask feature (Which will be discussed later on)
2. **controller.filename**
This will give you the filename you have given to the database which stores the user's credentials

### controller.signup()
In the signup(), you have to pass the user's username and password. Then it will store it in the database. The signup() returns true if the process went well. You will get false when the username is already taken by some other user
```python
username = input("Please make a username: ")
password = input("Please make a passward for security: ")
if controller.signup(username, password):
    print("Account created")
```
if you don't want to make a signup system, you can enable autotask. This will take the username and password by itself and will also check that if the username is already in use; If it is then it will ask for the username again until the user gets a right one! It will return true at the end eventually:
```python
if controller.signup(autotask=True):
    print("Account created " + controller.username)
```

#### Output:
```commandline
>> Please make a username: Test
>> Please make a password: 1111
This username is perfect
Account created
```

#### Output (If the username is already taken):
```commandline
>> Please make a username: Test
>> Please make a password: 1111
>> The username you entered is already in use. Please make another one: Test2
This username is perfect
Account created
```

### controller.login()
In the login(), you have to pass the user's username and password. It will return true is the user is identified, or else it will return false 
```python
username = input("Please make a username: ")
password = input("Please make a passward for security: ")
if controller.login(username, password):
    print("Hello " + username)
else:
    print("Access denied")
```

If you don't want to manually make a username and password entry, you can enable auto task. Auto task will simply take the input and output byitself and will return true if the login details are matching
```python
if controller.login(autotask=True) == True:
    print("Hello " + controller.username)
else:
    print("Access denied")
```
#### Output:
```commandline
>> Please enter your username: Ayaan 
>> Please enter your password: 1111
Hello Ayaan
```

### controller.deluser()
The `deluser()` function allows you to delete a user's account. You need to pass in the username and password for confirmation. It will return True if it is deleted and False if it didn't go well.  
**Note:** Once it is deleted, there is no turning back
```python
username = input("Please enter your username: ")
password = input("Please enter your password: ")
if controller.deluser(username, password) == True:
    print("Hello " + username)
else:
    print("Error occured")
```
If the `deluser()` returns false: 
1. It maybe because the username or password don't match
2. The account doesn't exist
3. There was some error in the deletion process (This is rare case)

Like in all the other functions, this has an `autotask`
```python
if controller.deluser(autotask=True):
    print("Bye " + controller.username)
else:
    print("Error ocurred")
```

#### Output
```commandline
>> Please enter your username: Test
>> Please enter your password for confirmation: 1111
>> Please enter your password again for confirmation: 1111
Bye Test
```

### usernames()
The `username()` function will return a list of usernames who already signup in your system
```python
print(controller.usernames())
```
**output**
```commandline
["test", "test2"]
```

### username_exists()
This is a helpful function when for some reason you want to check if a username exists and is not in use by someone else.  
You have to pass in a usename that you want to check. It will return `True ` if the username exists and `False` if the username is valid and is not in use:

```python
print(controller.username_exists("Test"))
```
#### output:
```console
True
```

### secure()
You have to end your programme with this function so that everything is completely safe and secure
```
controller.secure()
```


## Example of a login and signup system

```python
import UserIdentificationSystem as uis

controller = uis.Basic("user")
mode = input("Do you want to login(1) or signup(2) or delete account(3): ")
if mode == "1":
    if controller.login(autotask=True):
        print("Welcome " + controller.username)
    else:
        print("Access denied")
elif mode == "2":
    if controller.signup(autotask=True):
        print("Account created " + controller.username)
    else:
        print("Account creation failed")
else:
    if controller.deluser(autotask=True):
        print("Account deleted. Bye {}. We were having a good time".format(controller.username))
    else:
        print("Error occurred!")

controller.secure()
```

#### Output
Case 1
```commandline
>> Do you want to login(1) or signup(2) or delete account(3): 2
>> Please make a username: uis_learner
>> Please make a password for security: 1111
This username is perfect
Account created uis_learner
```

Case 2
```commandline
>> Do you want to login(1) or signup(2) or delete account(3): 1
>> Please enter your username: uis_learner
>> Please enter your password: 1111
Welcome uis_learner
```

Case 3
```commandline
>> Do you want to login(1) or signup(2) or delete account(3): 3
>> Please enter your username: uis_learner
>> Please enter your password for confirmation: 1111
>> Please enter your password again for confirmation: 1111
Account deleted. Bye uis_learner we were having a good time 
```

# Sophisticated system
## Import

```python
import UserIdentificationSystem as uis
```

## Functions 
### setup()
To start the setup, we need to create an instance of the ExtraPass() class. In the ExtraPass class, you need to pass in a filename witch will be storing your user's credentials.
```python
controller = uis.ExtraPass("users")
```
**Note:** When you will run your programme, it will create a database file that will be stored in you current working directory

### Some details
1. **controller.username**  
This will allow you to get the user's name when you will use autotask feature (Which will be discussed)
2. **controller.filename**
This will give you the filename you have given to the database which stores the user's credentials

### controller.signup()
In the signup(), you have to pass the user's username, password and an extra password. Then it will store it in the database. The signup() returns true if the process went well. You will get false when the username is already taken by some other user
```python
username = input("Please make a username: ")
password = input("Please make a password: ")
extra = input("Please make an extra password for security")

if controller.signup(username, password, extra):
    print("Account created")
else:
    print("Username is already in use")
```
if you don't want to make a signup system, you can enable autotask. This feature will take the username and password and extra password by itself and will also check that if the username is already in use; If it is then it will ask for the username again until the user gets a right one! It will return true at the end eventually:
```python
if uis.signup(autotask=True):
    print("Account created " + controller.username)
```

#### Output:
```commandline
>> Please make a username: Test
>> Please make a password: 1111
>> Please enter another password that can be different for extra layer of security: 2222
This username is perfect
Account created
```

#### Output (If the username is already taken):
```commandline
>> Please make a username: Test
>> Please make a password: 1111
>> Please enter another password that can be different for extra layer of security: 2222
>> The username you entered is already in use. Please make another one: Test2
This username is perfect
Account created
```

### controller.login()
In the login(), you have to pass the user's username, password and their extra password. It will return true is the user is identified, or else it will return false 
```python
username = input("Please enter your username: ")
password = input("Please enter your password: ")
extra_password = input("Please enter your extra password: ")

if controller.login(username, password, extra_password):
    print("Hello " + username)
else:
    print("Access denied")
```

If you don't want to manually make a username and password entry, you can enable auto task. Auto task will simply take the input and output byitself and will return true if the login details are matching
```python
if controller.login(autotask=True) == True:
    print("Hello " + controller.username)
else:
    print("Access denied")
```
#### Output:
```commandline
>> Please enter your username: Test 
>> Please enter your password: 1111
>> Please enter the extra layer of password you added: 2222
Hello Test
```

### controller.deluser()
The `deluser()` function allows you to delete a user's account. You need to pass in the username, password and extra password for confirmation. It will return True if it is deleted and False if it didn't go well.  
**Note:** Once it is deleted, there is no turning back
```python
username = input("Please enter your username: ")
password = input("Please enter your password: ")
extra = input("Please enter your extra password: ")

if controller.deluser(username, password, extra) == True:
    print("Hello " + username)
else:
    print("Error occured")
```
If the `deluser()` returns false: 
1. It maybe because the username or password don't match
2. The account doesn't exist
3. There was some error in the deletion process (This is rare case)

Like in all the other functions, this has an **autotask**
```python
if controller.deluser(autotask=True):
    print("Bye " + controller.username)
else:
    print("Error ocurred")
```

#### Output
```commandline
>> Please enter your username: Test
>> Please enter your password for confirmation: 1111
>> Please enter your password again for confirmation: 1111
>> Please enter the password you gave for extra layer (Password "2"): 2222
Bye Test
```
### usernames()
The `username()` function will return a list of usernames who already signup in your system
```python
print(controller.usernames())
```
**output**
```commandline
["test", "test2"]
```

### username_exists()
This is a helpful function when for some reason you want to check if a username exists and is not in use by someone else.  
You have to pass in a usename that you want to check. It will return `True ` if the username exists and `False` if the username is valid and is not in use:

```python
print(controller.username_exists("Test"))
```
#### output:
```console
True
```

### secure()
You have to end your programme with this function so that everything is completely safe and secure!
```python
controller.secure()
```


## Example of a login and signup system

```python
import UserIdentificationSystem as uis

controller = uis.ExtraPass("user")
mode = input("Do you want to login(1) or signup(2) or delete account(3): ")
if mode == "1":
    if controller.login(autotask=True):
        print("Welcome " + controller.username)
    else:
        print("Access denied")
elif mode == "2":
    if controller.signup(autotask=True):
        print("Account created " + controller.username)
    else:
        print("Account creation failed")
else:
    if controller.deluser(autotask=True):
        print("Account deleted. Bye {}. We were having a good time".format(controller.username))
    else:
        print("Error occurred!")

controller.secure()
```
or

```python
import UserIdentificationSystem as uis

controller = uis.ExtraPass("user")

mode = input("Do you want to login(1) or signup(2) or delete account(3): ")
if mode == "1":
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    extra_password = input("Please enter your extra password: ")

    if controller.login(username, password, extra_password):
        print("Hello " + username)
    else:
        print("Access denied")
elif mode == "2":
    username = input("Please make a username: ")
    password = input("Please make a password: ")
    extra_password = input("Please make an extra password: ")

    if controller.signup(username, password, extra_password):
        print("Welcome " + username)
    else:
        print("So error occurred")
else:
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    extra_password = input("Please enter your extra password: ")

    if controller.deluser(username, password, extra_password):
        print("Bye " + username)
    else:
        print("So error occurred")

controller.secure()
```

#### Output
Case 1
```commandline
>> Please make a username: uis_learner
>> Please make a password: 1111
>> Please enter another password that can be different for extra layer of security: 2222
This username is perfect
Account created
```

Case 2
```commandline
>> Please enter your username: uis_learner 
>> Please enter your password: 1111
>> Please enter the extra layer of password you added: 2222
Hello uis_learner
```

Case 3
```commandline
>> Please enter your username: uis_learner
>> Please enter your password for confirmation: 1111
>> Please enter your password again for confirmation: 1111
>> Please enter the password you gave for extra layer (Password "2"): 2222
Bye uis_learner
```

# Useful functions
### Importing
We need to import the uis file
```python
import UserIdentificationSystem as uis
```

### Generate random password
This feature will allow you to generate strong passwords with customizable feature  
To start, you have to use this function
```python
password = uis.passgen()
```
**output**
```commandline
OJrtetawrI!6547
```
**Note**: The default length of this function is set to 10, which will increase the length of the password. It is also set to mode of mix will be explained later

You can customize it my passing few parameters  
1. You can pass in the len parameter which will make your password lengthy
```python
password = uis.passgen(len=12)
```

**output**
```commandline
jTFTbHKrGrEd!5209
```
2. You can change the mode to be capitalised or lowercase. The default is set to mix, which means that it contains both capital and lower-case words
```python
password = uis.passgen(caplock=True) # You do this for making everything capital
```

```commandline
GIHEMOLBTL@5694
```
___
```python
password = uis.passgen(caplock=False) # You do this for making everything lowercase
```

```commandline
fjztungvje$9320
```

### Encryting strings
This feature will allow you to encrypt strings. Use the `uis.encrypt()` funtion, You have to pass in the string you want to encrypt

```python
uis.encrypt("Come to my house at 9:00 am")
```
**output**
```commandline
(ePF"_eP_Fz_:P<'"_9e_vcII_9F
```

**NOTE**: There is no decryting function as this same encryption is used for protecting your passwords in the database