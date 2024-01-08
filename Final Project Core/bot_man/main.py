from colorama import Fore, Style, init
from b_logic import  show_logo, load, fun_name, analyze_fun, helps

init()


def main():
    """
    Логіка роботи бота помічника
    
    """
    show_logo()
    load()

    while True:
        user_input = input(
            f"{Fore.GREEN}Введіть будь ласка команду: (або використай команду{Style.RESET_ALL} {Fore.RED}help{Style.RESET_ALL}{Fore.GREEN}){Style.RESET_ALL}\n").lower()
        if not user_input:
            print(helps())
        else:    
            fun, args = analyze_fun(user_input)
            # print(fun, '-------', args)
            text = fun_name(fun)(args)
            print(text)


if __name__ == "__main__":
    main()
