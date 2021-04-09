def initial_user_input():
    while True:
        print("East or West database: ")
        user_input = input()
        if user_input.lower() == 'west' or user_input.lower() == 'east':
            return user_input
            break
        else:
            print("The request contains a typo or database doesn't exist")
            continue


def choose_next_move():
    while True:
        print("Choose East or West database or shutdown: ")
        user_input = input()
        if user_input.lower() == 'west' or user_input.lower() == "east" or user_input.lower() == "shutdown":
            return user_input
            break
        else:
            print("The request contains a typo or database doesn't exist")
            continue


def choose_location():
    while True:
        print("Choose city: West- Bergen or Stavanger. East- Oslo: (Bergen, Stavanger, Oslo) ")
        user_input = input()
        if user_input.lower() == "bergen" or user_input.lower() == "stavanger" or user_input.lower() == "oslo":
            return user_input
            break
        else:
            print("The request contains a typo or city doesn't exist")
            continue


def choose_amount():
    while True:
        print("Do you wish to retrieve all data or data for a period? (all/period) ")
        user_input = input()
        if user_input.lower() == "all" or user_input.lower() == "period":
            return user_input
            break
        else:
            print("The request contains a typo or city doesn't exist")
            continue


def period(start_stop):
    while True:
        print("Enter %s date (YYYY-MM-DD) " % start_stop)
        user_input = input()
        print("user inp ", user_input)
        print(user_input[:4]+"-"+user_input[5:7]+"-"+user_input[-2:])
        if user_input == user_input[:4]+"-"+user_input[5:7]+"-"+user_input[-2:]:
            return user_input
            break
        else:
            print("The request contains a typo ")
            continue
