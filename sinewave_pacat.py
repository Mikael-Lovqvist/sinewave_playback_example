import subprocess
import numpy as np
import math

f = 440 # Hz
a = 0.1 # amplitude
p = 0 # phase offse (0 .. 2π)

buffersize = 256 # samples
latency = 100 # ms
rate = 48000 # Hz

timestep = f * math.tau / rate # you can recaulcate this in the generator loop if you want to modulate the frequency

sound_buffer = np.array([0.0] * buffersize, np.float32) # this sound buffer can be reused over and over

# output sound using Pulseaudio using Pacat and stdin
output_sound = subprocess.Popen(('pacat', f'--latency-msec={latency}', '--format=float32ne', '--channels=1', f'--rate={rate}'), stdin=subprocess.PIPE)


accumulator = p	#starting phase
while True:
	#Update buffer
	for i in range(buffersize):
		sound_buffer[i] = np.sin(accumulator) * a
		accumulator = (accumulator + timestep) % math.tau

	#Play buffer (blocking)
	output_sound.stdin.write(sound_buffer.tobytes()) #write buffer to stdin