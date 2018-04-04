import time

struct_time = time.strptime("2000-03-07 06:51:36", "%Y-%m-%d %H:%M:%S")
print "returned tuple: %s " % struct_time