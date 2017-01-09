# main.py

"""
This Hamming encoder and decoder program has been written in Python and should be run using Python 2.7. 
The program successfully encodes and decodes a binary word in order to simulate the 
encoding and decoding process that happens in data transmission.
   
Implemented only to simulate single-bit error correction/detection
"""
__author__ = "Zach Clark"
__course__ = "CS 445 - George Thomas"
__email__ = "zclark14@apu.edu"
__version__ = "1.0"
import itertools

def compute_r(data):
    for r in range(data):
        if data <= 2**r - 1 - r:
            return r
        
def compute_parity_bits(bits, r, n):
    # checks to see if it has already been computed before filling parity bits with 0 place-holders
    if(len(bits) != n):
        
        # insert 0 as place holder for parity check bits
        for i in range(r):
            bits.insert(2**i - 1, 0)
        
    # insert values for parity check bits        
    for x in range(r):
        parity = 0
        curr = 2**x - 1
        temp = []
        
        for y in range(len(bits)):      
            if curr >= len(bits):       # break if at the end of the list
                break
            temp.append(bits[curr : curr + 2**x])   # grabs number of bits based on current parity position (x)
            
            curr += 2**(x+1)        # skip however many indices to get to the next subset of bits
        
        temp = list(itertools.chain(*temp))   # break up the ugly 2D lists
        
        parity = sum(temp) % 2      # this adds up all the parity bits and takes MOD 2
        bits[2**x - 1] = parity     
        
    return bits
      
      

""""1.) Get n, m, r""" 
print "-------------------------------------------"
print "--------------Hamming Encoding-------------"
print "-------------------------------------------"
m = raw_input("Enter how many bits (m), are to be encoded: ")
m = int(m)

""""2.) Compute and print shortened Hamming code."""
r = compute_r(m)
n = m + r
code = (n, m)
print code

bits = []
errored_bits = []

#Insert into array
bits = raw_input("Enter %d bits: " % m)
if len(bits) != m:
    bits = []
    bits = raw_input("Enter ONLY %d bits: " % m)

bits = [int(x) for x in bits]

# Save copy of old list
original_bits = list(bits)

""""3-4.) This method computes and inserts necessary parity bits."""
bits = compute_parity_bits(bits, r, n)
print "bits: ", bits

errored_bits = raw_input("\nEnter which bits should be in error separated by spaces (e.g. 5 6 10): ")
errored_bits = errored_bits.split()
errored_bits = [int(x) for x in errored_bits]#.replace(',', '')]

""""5.) Flip the specified bits."""
for i in errored_bits:
    bits[i - 1] = (bits[i - 1] + 1) % 2
    
print "bits: ", bits, "\n"

""""6.) Recompute parity bits.""" 
print "-------------------------------------------"
print "--------------Hamming Decoding-------------"
print "-------------------------------------------"  

# Using temporary list here so I don't mess up the values of the original list
temp = list(bits)
temp = compute_parity_bits(temp, r, n)
  
error_location = 0
for i in range(r):
    if temp[2**i - 1] == 1:
        error_location += 2**i        
          
print "Error in bit: ", error_location

""""7.) Fix the erroneous bit"""
bits[error_location - 1] = (bits[error_location - 1] + 1) % 2

""" 8.) Drop the parity bits and retain the remaining word."""
parity_idx = []
for i in range(r):
    parity_idx.append(2**i - 1)

# List comprehension removes fixed parity indices
bits = [i for j, i in enumerate(bits) if j not in parity_idx]

""" 9.) Compare with the original m-bit word and see how many errors are still there, if any. """
print "Original code:  ", original_bits
print "Corrected code: ", bits
