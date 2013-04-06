def foo(x):
    return int(round(((((((x/360.0)+(0.25))-1))*360)),0))

def foo2(x):
    if (((x/360.0)+(0.25))-1)*360 <0 or (((x/360.0)+(0.25))-1)*360 >360 :
        return 360 - ((((x/360.0)+(0.25)))*360)
    else:
        return (((x/360.0)+(0.25)))*360

def foo3(x, y):
    if y +x > 360:
        return y+x - 360
    else:
        return y+x
##foo(30)
##foo(600)
##foo(120)
##foo(180)

for i in range(0,360):
    print str(i) +' ' + str(foo3(30,i))
