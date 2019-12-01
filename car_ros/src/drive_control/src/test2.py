while True:
    f = open("foo.txt", "r")
    c = f.read(1)
    print(c)
    f.close()