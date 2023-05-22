import data

def display_menu():
    print('----- NFT generator -----')
    print('1. Create characters')
    print('2. Generate images')
    print('3. Generate Metadata')
    print('4. Generate summary')
    print('0. Exit')

def handle_option(option):
    if option == '1':
        option1()
    elif option == '2':
        option2()
    elif option == '3':
        option3()
    elif option == '4':
        option4()
    elif option == '0':
        print('Exiting...')
        return False
    else:
        print('Invalid option. Please try again.')

    return True

def option1():
    print('-- 1. Create characters --')
    print('How many do you want?')
    user_choice = int(input('How many characters do you want? >>> '))
    data.generate_json_files(user_choice, races=data.races, races_weights=data.races_weights, classes=data.classes, classes_weights=data.classes_weights, weapons=data.weapons, items=data.items)
    print(f'Success! Generated {user_choice} characters!')

def option2():
    print('-- 2. Generate images --')
    data.generate_images()
    print(f'Success! Generated images!')

def option3():
    print('-- 3. Generate Metadata --')
    data.generate_metadata()
    print(f'Success! Generated metadata!')

def option4():
    print('-- 4. Generate summary --')
    data.generate_summary()
    print(f'Success! Generated summary!')


def main():
    running = True
    while running:
        display_menu()
        option = input('Enter your choice (0-4): ')
        running = handle_option(option)

if __name__ == '__main__':
    main()