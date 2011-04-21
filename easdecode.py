import math, struct, array, sys, time, re

if __name__ == "__main__":
    import wave

    file = wave.open('testfile-msg.wav', 'rb')
    samples = array.array('h', file.readframes( file.getnframes()))
    file.close()
    delay_length = int(divmod(44100, 520.5)[0] / 2.0)
    print delay_length
    out_data = ''
    last_val = 0
    zero_counter = 0
    bit_width_ctr = 0
    bitstream = ''
    message = ''

    for i in range(0, len(samples) - delay_length):
	#print samples[i + delay_length], samples[i]
	cor_val = (samples[i + delay_length] * samples[i]) / 1073676289.0
	#print cor_val

	if  cor_val > 0.02:
	    zero_counter = 0
	    out_data += struct.pack('<h', 16600)
	    if last_val == -16600:
		bit_width_ctr = 0
	    last_val = 16600

	elif cor_val < -0.02:
	    zero_counter = 0
	    out_data += struct.pack('<h', -16600)
	    if last_val == 16600:
		bit_width_ctr = 0
	    last_val = -16600

	else:
	    zero_counter += 1
	    if zero_counter > 16:
		out_data += struct.pack('<h', 0)
		bit_width_ctr = 0
	    else:
		out_data += struct.pack('h', last_val)
	out_data += struct.pack('<h', int(cor_val * 300767))
	bit_width_ctr += 1
	if bit_width_ctr == delay_length:
	    if last_val == -16600:
		bitstream += '0'
	    if last_val == 16600:
		bitstream += '1'
	if bit_width_ctr == (delay_length * 2):
	    bit_width_ctr = 0

    #print bitstream
    preamble = '11010101' * 16
    #msg_collection = re.findall(preamble, bitstream)
    start_index = 0
    msg_collection = []
    while True:
	try:
	    start_index = bitstream.index(preamble, start_index)
	    msg_collection.append(start_index)
	except ValueError:
	    print "Error"
	    break
	start_index += 128
	print start_index
    
    print msg_collection
    start_index = bitstream.find(preamble)
    #print msg_collection
    for i in range(start_index, len(bitstream), 8):
	byte = bitstream[i:i+8]
	letter = chr(int(byte[::-1], 2))
	sys.stdout.write(letter)
	message += letter
	#time.sleep(0.150)

    print repr(message)

    file = wave.open('correlated.wav', 'wb')
    file.setparams( (2, 2, 44100, 44100, 'NONE', '') )
    file.writeframes(out_data)
    file.close()

