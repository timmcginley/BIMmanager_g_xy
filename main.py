import ifcopenshell

import analyst_gr10.rules
import analyst_gr11.rules


model = ifcopenshell.open('somefile.ifc')

result1 = analyst_gr10.rules.doorCheck.doCheck(model)
result2 = analyst_gr11.rules.foobarCheck.doCheck(model)

print(result1)
print(result2)
