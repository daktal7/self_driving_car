i = 0
while True:
    f = open("~/Desktop/light.txt","w")
    if i%2:
        f.write('g')
        print("g")
    else:
        f.write('r')
        print("r")
    i = i+1
    f.close()