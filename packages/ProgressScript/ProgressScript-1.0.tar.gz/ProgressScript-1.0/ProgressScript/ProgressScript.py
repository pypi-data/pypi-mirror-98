#0.1 BETA

# Modules

import time
from tqdm import * # TQDM INITIALIZED FOR BEAUTIFUL AND ADDITIONAL PO
from colorama import Fore, init

# Color Init

init()

# Pause Time

pause = 1

# Trying

try:

    # Funcs

    class PyProgress:
            def points(speed, one, two, three):
                a = "." + " " + str(one) + "%"
                b = a * 2 + " " + str(two) + "%"
                c = a * 3 + " " + str(three) + "%"
                print(a)
                time.sleep(speed)
                print(b)
                time.sleep(speed)
                print(c)
                time.sleep(pause)

            def slash(speed, one, two, three):
                a = "/" + " " + str(one) + "%"
                b = "/" * 2 + " " + str(two) + "%"
                c = "/" * 3 + " " + str(three) + "%"
                print(a)
                time.sleep(speed)
                print(b)
                time.sleep(speed)
                print(c)
                time.sleep(pause)

            def stars(speed, one, two, three):
                a = "*" + " " + str(one) + "%"
                b = "*" * 2 + " " + str(two) + "%"
                c = "*" * 3 + " " + str(three) + "%"
                print(a)
                time.sleep(speed)
                print(b)
                time.sleep(speed)
                print(c)
                time.sleep(pause)

            def num(num, speed, one, two, three):
                a = str(num) + " " + str(one) + "%"
                b = str(num) * 2 + " " + str(two) + "%"
                c = str(num) * 3 + " " + str(three) + "%"
                print(a)
                time.sleep(speed)
                print(b)
                time.sleep(speed)
                print(c)
                time.sleep(pause)

            def bar(speed, update, total, range1):
                with tqdm(total=int(total)) as pbar:
                    for i in range(int(range1)):
                        time.sleep(int(speed))
                        pbar.update(int(update))

            #def None():
                #pass (UPDATE)

            def guide():
                print(
                    " \n POINTS: \n First, specify the download speed, then specify the download percentages. Done! Example: PyProgress.points(1, 25, 50, 100)."
                    " \n SLASH: \n First, specify the download speed, then specify the download percentages. Done! Example: PyProgress.slash(1, 25, 50, 100)."
                    " \n STARS: \n First, specify the download speed, then specify the download percentages. Done! Example: Example: PyProgress.stars(h, 1, 25, 50, 100)."
                    " \n NUM: \n To start, specify the number that you will fill in, then specify the download speed, and then the download percentage. Done! Example: PyProgress.num(1, 1, 25, 50, 100)."
                    " \n BAR: \n To start, specify the speed, then update the download. Then specify the 'total' amount after which range number (10 default). Example: PyProgress.bar(1, 10, 100, 10)."
                )

# Excepting

except ValueError:
   print( Fore.RED )
   print("[ValueError] Check Your Values")
except NameError:
   print( Fore.RED )
   print("[Error] Check Your Command")
except TypeError:
   print( Fore.RED )
   print("[TypeError] Check Your Code")
except Warning:
   print( Fore.RED )
   print("[Warning] Warning Code Is Poorly Functioning")
except SyntaxError:
   print( Fore.RED )
   print("[NoneType] Detected Banned Symbol")
except KeyboardInterrupt:
    print( Fore.RED )
    print("[KeyboardInterrupt] Operation Canceled")
except:
    print( Fore.RED )
    print("[Unknown] Unknown Error")

"Settings"

print("Module Started")
time.sleep(1)

# Your Code Here

print("Module Stopped Working")
time.sleep(1)