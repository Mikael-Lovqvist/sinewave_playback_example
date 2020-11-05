import subprocess
import numpy as np
import math

f = 3 # frequency in hz (incorrect, need to modify code for accurate timing.)
a = 0.1 # amplitude
p = 0 # phase
t = 0 # time step

buffersize = 1024 * 4 # size of sound buffer
current_time = math.pi*2 / buffersize

latency = buffersize * 8 # latency in number of bytes
pacatbuffer = bytearray()

# output sound using Pulseaudio using Pacat and stdin
output_sound = subprocess.Popen(('pacat', '--latency', str(latency),  '--format', 'float32ne', '--channels', '1'), stdin=subprocess.PIPE)

while True:
	for i in range(buffersize):
		t = t+current_time
		sinewave = math.sin((math.pi*2)*(f*t)+p)*a
		sample = np.float32(sinewave) # Python float to Numpy float32
		sample.tobytes() # convert sound sample to bytes
		pacatbuffer += bytearray(sample) # add bytes to buffer
	output_sound.stdin.write(pacatbuffer) #write buffer to stdin
	pacatbuffer = bytearray() # empty buffer