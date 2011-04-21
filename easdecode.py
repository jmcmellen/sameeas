import math, struct, array

if __name__ == "__main__":
    import wave

    file = wave.open('testfile-noise-filtered.wav', 'rb')
    samples = array.array('h', file.readframes( file.getnframes()))
    file.close()
    delay_length = int(divmod(44100, 520.5)[0] / 2.0)
    print delay_length
    out_data = ''
    last_val = 0
    zero_counter = 0

    for i in range(0, len(samples) - delay_length):
	#print samples[i + delay_length], samples[i]
	cor_val = (samples[i + delay_length] * samples[i]) / 1073676289.0
	#print cor_val

	if  cor_val > 0.02:
	    zero_counter = 0
	    out_data += struct.pack('<h', 16600)
	    last_val = 16600

	elif cor_val < -0.02:
	    zero_counter = 0
	    out_data += struct.pack('<h', -16600)
	    last_val = -16600

	else:
	    zero_counter += 1
	    if zero_counter > 16:
		out_data += struct.pack('<h', 0)
	    else:
		out_data += struct.pack('h', last_val)
	out_data += struct.pack('<h', int(cor_val * 300767))


    file = wave.open('correlated.wav', 'wb')
    file.setparams( (2, 2, 44100, 44100, 'NONE', '') )
    file.writeframes(out_data)
    file.close()

