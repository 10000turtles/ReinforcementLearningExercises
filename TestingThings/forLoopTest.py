import time

start = time.time()
j = 0
iterations = 10**9
for i in range(iterations):
  j += 1
  if(i % 10000000 == 0):
    print(str(float(i/(iterations)*100)) + "% Complete")
print(j)
seconds = time.time()-start
minutes = seconds/60
hours = minutes/60
print("Seconds: "+str(seconds*10000))
print("Minutes: "+str(minutes*10000))
print("Hours: "+str(hours*10000))
