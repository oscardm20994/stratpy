import iris 
from eofs.iris import Eof as eoFs
from eofs.standard import Eof
def eofcube(cube):
	solver=eoFs(cube)
	eofs=solver.eofs(neofs=3)
	pcs=solver.pcs(npcs=2,pcscaling=1)
	frac=solver.varianceFraction(neigs=3)
	return eofs,pcs,frac


