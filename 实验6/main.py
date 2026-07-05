from data import *
from Caculator import *

standard_r = 14.72
foreign_radius = (average(foreign.repeatibility)+average(foreign.reoccurbility))/2
foreign_rep = uncertainty_average(foreign.repeatibility)
foreign_reo = uncertainty_average(foreign.reoccurbility)
foreign_error = abs(standard_r - foreign_radius) / standard_r

domestic_radius = (average(domestic.repeatibility)+average(domestic.reoccurbility))/2
domestic_rep = uncertainty_average(domestic.repeatibility)
domestic_reo = uncertainty_average(domestic.reoccurbility)
domestic_error = abs(standard_r - domestic_radius) / standard_r

print("")
print(f"Foreign Instrument:{foreign_radius:.2f}")
print(f"error:{foreign_error*100:.2f}%, repeatibility:{foreign_rep:.3e}, reoccurbility:{foreign_reo:.3e}")
print(f"domestic Instrument:{domestic_radius:.2f}")
print(f"error:{domestic_error*100:.2f}%, repeatibility:{domestic_rep:.3e}, reoccurbility:{domestic_reo:.3e}")
