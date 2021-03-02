import console

if __name__ == '__main__':
    console.loadClasses() #preload solved.ac classes

    while True:
        if not console.console_main():
            break