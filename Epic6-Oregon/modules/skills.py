def list_of_skills():
    print("Available Skills")
    m1 = "1.) Programming"
    m2 = "2.) Carpentry"
    m3 = "3.) Photography"
    m4 = "4.) Microsoft Excel"
    m5 = "5.) Learn Spanish"
    m6 = "6.) Exit"
    print(m1)
    print(m2)
    print(m3)
    print(m4)
    print(m5)
    print(m6)
    while True:
        try:
            option = int(input("Please enter your option (1-5): "))
            if option == 1:
                return [option, m1]
            elif option == 2:
                return [option, m2]
            elif option == 3:
                return [option, m3]
            elif option == 4:
                return [option, m4]
            elif option == 5:
                return [option, m5]
            elif option == 6:
                return [option, m6]
            return [option, 'Invalid']
        except ValueError:
            print("Input has to be an integer")