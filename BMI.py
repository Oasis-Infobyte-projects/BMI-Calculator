import math
from time import strftime
from tkinter import *
import tkinter.messagebox as tm
import datetime
import os
import re

root = Tk()


def entryscreen():
    """
    Displays a TKinter window that allows a user to enter there name.

    The user enters there name and clicks Go for the name to be sent for validation.
    If the click quit, the window closes and the program ends.
    This window is the main window so if this one closes, all others do too.
    """

    global name
    root.title('Please enter your name')

    fr1 = Frame(root)
    name = StringVar(fr1)

    Label(fr1, text='Name').grid()
    Entry(fr1, width=20, textvariable=name).grid(row=0, column=1)

    Button(fr1, text='Quit', command=root.quit).grid(row=1)
    Button(fr1, text='Go', command=verifynameinput).grid(row=1, column=1)

    fr1.pack()
    fr1.mainloop()


def verifynameinput():
    """
    This method takes the name given above and validates it

    It stores the name in the global variable user as it may make some changes to the name,
    eg. if name is entered with preceding or trailing whitespace, this method will get rid of that.
    It checks the name against a regex I have created that allows certain characters such as a dash and apostrophe.
    It also allows whitespace if the user wants to enter their first and last name.
    If the name does not match the regex an error is shown, it does not destroy the window though and allows the user
    to try again if they want.
    If the name matches the regex the program proceeds to the imperial or metric method.
    """

    global user
    user = name.get()
    regex = "^[A-Za-z ,.'-]+$"
    user = user.strip()

    match = re.match(regex, user)

    if match is None:
        tm.showerror('Error!', 'The name should only contain letters and should not be left blank, please try again')
    else:
        imperialormetric()


def imperialormetric():
    """
    Displays a window allowing the user to choose if they want to enter their values in imperial or metric

    This, and every window after this, is a transient window, so when the original window is closed or minimized, these
    all follow suit
    :return:
    """

    t = Toplevel(root)
    t.transient(root)
    t.title('Imperial or Metric?')

    frame1 = Frame(t)

    Label(frame1, text='Please choose a system').pack()
    Button(frame1, text='Imperial', height=2, width=30, command=imperial).pack()
    Button(frame1, text='Metric', height=2, width=30, command=metric).pack()

    frame1.pack()

    root.mainloop()


def metric():
    """
    This window allows the user to use sliders to enter their details.

    The sliders give loads of options for both height and weight to match all types of user.
    The sliders allow for me to limit the amount of errors that could happen as the user doesn't have to enter any
    values, they simply use the sliders to find their details.
    If the user hits the quit button, this window will close and the user will be taken back to the preceding window
    allowing them to chose imperial or metric again if they have made a wrong decision.
    Once they have chosen their height and weight and clicked the calculate button, they will be taken to the bmi
    calculator.
    :return:
    """

    t = Toplevel(root)
    t.transient(root)
    t.title('BMI Calculator')

    fr1 = Frame(t)
    fr2 = Frame(t)
    fr3 = Frame(t)
    global metresval
    global kgsval
    metresval = DoubleVar(t)
    kgsval = DoubleVar(t)
    opt = {'fill': BOTH, 'side': LEFT, 'padx': 2, 'pady': 3}

    Label(fr1, text='Please enter your height in metres').pack()
    Scale(fr1, from_=0.54, to=2.72, digits=3, resolution=0.01, length=200,
          variable=metresval, orient=HORIZONTAL).pack(opt)

    Label(fr2, text='Please enter your weight in kgs').pack()
    Scale(fr2, from_=2, to=250, length=200, variable=kgsval,
          orient=HORIZONTAL).pack(opt)

    Button(fr3, text='Quit', command=root.quit).pack(fill=BOTH, side=LEFT)
    Button(fr3, text='Calculate', command=bmicalculator).pack(fill=BOTH, side=RIGHT)

    fr1.pack()
    fr2.pack()
    fr3.pack()


def imperial():
    """
    This window is different to the metric window in that the user actually gets to enter their own desired values.

    The user is given the freedom to put in whatever value they want, within reason.
    The values of all inputs are originally taken as Strings as it would throw an error before I even get to validate
    if the user has entered a string in one of the boxes and the variable was looking for an int.
    Because the user gets to input their own values, this time when they press calculate it takes the given answers
    and runs them through a validator to make sure all answers are appropriate.
    All four values given are stored in global variables as they are needed when displaying messages later on in the
    program.
    :return:
    """

    t = Toplevel(root)
    t.transient(root)
    t.title('BMI Calculator')

    fr1 = Frame(t)
    fr2 = Frame(t)
    global feetval
    global inchesval
    global stoneval
    global poundsval
    feetval = StringVar(t)
    inchesval = StringVar(t)
    stoneval = StringVar(t)
    poundsval = StringVar(t)

    Label(fr1, text='Please enter your height in Feet and Inches').grid(column=1, pady=10)

    Label(fr1, text='Feet:').grid(row=1)
    Entry(fr1, width=5, textvariable=feetval).grid(row=1, column=1)

    Label(fr1, text='Inches:').grid(row=2)
    Entry(fr1, width=5, textvariable=inchesval).grid(row=2, column=1)

    Label(fr2, text='Please enter your weight in Stones and Pounds').grid(column=1, pady=10)

    Label(fr2, text='Stone:').grid(row=1)
    Entry(fr2, width=5, textvariable=stoneval).grid(row=1, column=1)

    Label(fr2, text='Pounds:').grid(row=2)
    Entry(fr2, width=5, textvariable=poundsval).grid(row=2, column=1)

    Button(fr2, text='Quit', command=root.quit).grid(row=3, pady=30)
    Button(fr2, text='Calculate', command=imperial_metric).grid(row=3, column=1)

    fr1.pack()
    fr2.pack()


def imperial_metric():
    """
    This function changes the imperial values given into the metric system before sending them to the BMI calculator.

    Again, required variables are global as they will be needed later on in the program.
    In this function there is a flag called metric that is False, this is used later on in the program when I have to
    find out which values the user used so I can add them to the CSV file.
    Here the values given by the user are sent off to a different function to be tested.
    Once the validated values come back from that function they are converted to metres and kilos and rounded to 2
    decimal places.
    They are then sent to the BMI calculator to find out the BMI
    :return:
    """

    global metric
    global heightmetre
    global weightkilos

    metric = False

    inches = inchesval.get()
    pounds = poundsval.get()
    feet = feetval.get()
    stone = stoneval.get()
    try:
        inchandpound = verifyimperialinput(inches, pounds, feet, stone)

        heightmetre = round(inchandpound[0] / 39.37, 2)
        weightkilos = round(inchandpound[1] / 2.205, 2)

        bmicalculator()

    except TypeError:
        tm.showerror('ERROR!', 'Please revise your answers')



def verifyimperialinput(inches, pounds, feet, stone):
    """
    This function takes in all the values provided by the user and checks them to make sure they are appropriate.

    The feet and stone values are sent through a separate regex function to inches and pounds.
    For feet and stone to pass the first validation they need to be integers, anything else will throw an error message.
    For inches and pounds to pass the first validation they can be either whole numbers or decimal numbers as a lot of
    people know that they are half a pound or half an inch also.
    Again, anything other that digits will throw an error.
    Now that we have made sure that all values given are digits we can now assign them to int and float variables to
    help validate them some more.
    This is still not bulletproof as if someone has not entered any value then they will pass the first validation
    but it will throw an exception at the second validation.
    I added a try, except block here to catch an errors, it does not destroy the windows, it allows the user to re-enter
    another value.
    In the second validation the values are checked to see if they are too big/small/heavy/light.
    Once these validations have been passed, the inches and pounds are sent back to the imperial_metric function to
    change them into metric.
    :param inches:
    :param pounds:
    :param feet:
    :param stone:
    :return:
    """

    global inchesnew
    global poundsnew
    flag = True
    regex = '^[0-9]*$'
    regex2 = '^\d*\.?\d*$'

    match = re.match(regex, feet)
    if match is None:
        tm.showerror('Error!', 'Feet and Stone values can only be integers')

    match = re.match(regex, stone)
    if match is None:
        tm.showerror('Error!', 'Feet and Stone values can only be integers')

    match = re.match(regex2, inches)
    if match is None:
        tm.showerror('Error!', 'Inches and Pounds value may only contain integer or decimal numbers,'
                               ' no special characters are allowed')
    match = re.match(regex2, pounds)
    if match is None:
        tm.showerror('Error!', 'Inches and Pounds value may only contain integer or decimal numbers,'
                               ' no special characters are allowed')

    try:
        feet = int(feet)
        inches = float(inches)
        stone = int(stone)
        pounds = float(pounds)
        inchesnew = inches + (feet * 12)
        poundsnew = pounds + (stone * 14)

        if inches >= 12:
            tm.showerror('Error!', 'There are only 12 inches in a foot, please revise your answers')
            flag = False
        elif pounds >= 14:
            tm.showerror('Error!', 'There are only 14 pounds in a stone, please revise your answers')
            flag=False
        elif inchesnew >= 107:
            tm.showerror('Error!',
                         "The tallest person that ever lived was 2.72m (8 ft 11.1 in), you think you're taller? I don't"
                         " think so.")
            flag = False
        elif inchesnew <= 21:
            tm.showerror("Error!",
                         "The smallest person ever recorded was 0.54m (1 ft 10 in), you think you're smaller? I don't "
                         "think so.")
            flag = False
        elif poundsnew >= 1400:
            tm.showerror("Error!",
                         "The heaviest person ever was 635 kg (100 stone), you think you're heavier? I don't think so.")
            flag = False
        elif poundsnew <= 5:
            tm.showerror("Error!",
                         "The lightest person ever was only 2.1 kg (4.7 lbs), you think you're lighter? "
                         "I don't think so.")
            flag = False

        if flag:
            return inchesnew, poundsnew


    except ValueError:
        tm.showerror('Error!', 'Field left blank, please fill in all fields')


def bmicalculator():
    """
    This function calculates the user's BMI and displays it on the screen alongside their height and weight in both
    imperial and metric.

    At the start the flag is checked to see what system the user used to submit their values.
    If they used metric then the values are sent to a different function designed to give back the exact height of
    the user in imperial so it can also be displayed.
    The inches are used to find the exact height of the user in feet and inches.
    The metric values are used to find out the user's BMI, it then figures out if the user is
    underweight/healthy weight/overweight/obese.
    It also tell those who are not healthy weight, how much they have to lose/gain to be a healthy weight.
    Once all this is found, the program then displays all this info on an info window.
    The main data is then sent to a function to save the data to a CSV file.
    :return:
    """

    if not metric:
        heightmtr = heightmetre
        weightkgs = weightkilos
        inches = inchesnew
        pounds = poundsnew
    else:
        heightmtr = metresval.get()
        weightkgs = kgsval.get()
        imperialnums = metric_imperial(heightmtr, weightkgs)
        pounds = imperialnums[0]
        inches = imperialnums[1]

    inch = inches % 12
    feet = math.floor(inches / 12)
    inch = round(inch, 1)

    feetandinches = (str(feet) + 'ft' + str(inch) + '"')

    header = 'BMI Results'
    loseorgain = ''
    bmi = (weightkgs / (heightmtr * heightmtr))
    bmi = round(bmi, 1)

    if bmi <= 18.5:
        result = 'underweight'
        loseorgain = 'gain'
    elif 18.5 < bmi <= 24.9:
        result = 'healthy weight'
    elif 24.9 < bmi <= 29.9:
        result = 'overweight'
        loseorgain = 'lose'
    else:
        result = 'obese'
        loseorgain = 'lose'

    if result == 'healthy weight':
        tm.showinfo(header, 'You are ' + result + ': ' + str(bmi) + '\nCongratulations keep it up!' + '\n'
                            'Metric height and weight:\t\t' + str(heightmtr) + 'mtr\t' +
                            str(weightkgs) + 'kgs' + '\nImperial height and weight:\t\t' + feetandinches +
                             '\t' + str(pounds) + 'lbs')
    else:
        change = tohealthyweight(weightkgs, heightmtr, loseorgain)
        tm.showinfo(header, 'You are ' + result + ': ' + str(bmi) + '\nYou need to ' + loseorgain + ' weight!\n' +
                    'You have to ' + loseorgain + ' ' + str(change) + ' kgs to be at a healthy weight!' + '\n' +
                    'Metric height and weight:\t\t' + str(heightmtr) + 'mtr\t' +
                    str(weightkgs) + 'kgs' + '\nImperial height and weight:\t\t' + feetandinches +
                    '\t' + str(pounds) + 'lbs')

    savedata(bmi, result, feetandinches, pounds)


def metric_imperial(metres, kgs):
    """
    This methods takes in metric values and changes them to imperial values and returns the imperial values
    :param metres:
    :param kgs:
    :return:
    """

    weightpounds = round(kgs * 2.205, 1)
    heightinches = metres * 39.37

    return weightpounds, heightinches


def tohealthyweight(weightkgs, heightmtr, loseorgain):
    """
    This fucntion takes in the user's height and weight and determines how much they need to lose or gain.

    This function is only used if the user is not a healthy weight.
    It determines how much the user need to gain/lose for them to have the BMI of a healthy weight.
    This function uses the Broca Index to find the ideal body weight.
    :param weightkgs:
    :param heightmtr:
    :param loseorgain:
    :return:
    """

    heightcm = heightmtr * 100
    new_weight = ((heightcm - 100) - ((heightcm - 100) * .1))
    if loseorgain == 'gain':
        change = new_weight - weightkgs
    else:
        change = weightkgs - new_weight

    change = round(change, 2)

    return change


def savedata(bmi, result, feetandinches, pounds):
    """
    This function saves all the necessary data to a CSV file.

    The function gets the current date and time.
    It also creates a header to be put on the top of the CSV file.
    It then checks if the CSV file exists, if it doesn't, one is created with the below headers.
    It then writes the values of all the data to the CSV file.
    It writes the height and weight in the system the user provided but adds the unit of measurement beside it.
    If the user already has the file open while trying to write stuff to the file an error will be thrown.
    :param bmi:
    :param result:
    :param feetandinches:
    :param pounds:
    :return:
    """

    file = 'savedata.csv'
    counter = 1
    header = ['Date & Time', 'Name', 'Height (Feet / Metres)', 'Weight (Pounds / Kgs)', 'BMI', 'Result']
    datenow = datetime.datetime.now()
    datenow = strftime('%d-%b-%Y %H:%M')
    name = user
    if not metric:
        height = feetandinches
        weight = str(pounds) + 'lbs'
    else:
        height = str(metresval.get()) + 'mtr'
        weight = str(kgsval.get()) + 'kgs'

    data = [datenow, name, height, weight, bmi, result]

    if not os.path.isfile(file):
        with open(file, 'w') as f:
            for item in header:
                if counter == 6:
                    value_to_write = f'{item}\n'
                    counter = 1
                else:
                    value_to_write = f'{item},'
                    counter += 1

                f.write(value_to_write)

    try:
        with open(file, 'a') as f:
            for item in data:
                if counter == 6:
                    value_to_write = f'{item}\n'
                    counter = 1
                else:
                    value_to_write = f'{item},'
                    counter += 1

                f.write(value_to_write)


    except IOError:
        tm.showerror('ERROR WRITING TO FILE', 'Please close "' + file + '" before you run this program!')
        root.destroy()


entryscreen()

