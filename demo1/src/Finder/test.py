from Finder import Finder

f = Finder()
f.start()

while(True):
    cmd = input("Type 'q' to quit, anything else to read data: ")
    if cmd == 'q':
        break
    
    res = f.markers
    for key in res:
        print(key, res[key])

f.stop()