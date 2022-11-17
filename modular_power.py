""" 
Function to calculate x**y mod p
"""
def modular_power(x, y, p):
    result = 1
    while y>0:
        if y&1>0:
            result = (result*x)%p
        y >>= 1
        x = (x*x)%p    
    return result