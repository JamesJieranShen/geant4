import sys; sys.path.insert(0,sys.argv[1]); import warnings; warnings.filterwarnings("ignore")
import analyze as a, numpy as np, pandas as pd
from pathlib import Path
d=Path(sys.argv[2])/"data"; td="/home/jierans/work/dune/solar/G4TENDL1.4/Alpha/Inelastic"
for e in (5,10,20):
    ev,pr=a.load(d,f"corr_on_{e}"); pr["sp"]=a.species(pr); c=a.conservation(ev,pr)
    bad=((c.dZ!=0)|(c.dA!=0)|(c.dE.abs()>=1e-3)).sum()
    tab=a.tabulated(td,e); heavy={k:v for k,v in tab.items() if k>2004}; s=sum(heavy.values())
    n=len(c); chi=0;ndf=0;rows=[]
    for za,y in sorted(heavy.items(),key=lambda x:-x[1]):
        k=(pr.sp==str(za)).sum(); ex=n*y/s
        if ex>=20: chi+=(k-ex)**2/ex;ndf+=1; rows.append((za,round(y/s,6),k/n,round((k-ex)/ex**.5,1)))
    print(f"E={e} on: violating events={bad} of {n}, max|dE|={c.dE.abs().max():.3g} MeV; sum heavy yields={s:.5f}; chi2/ndf resid vs table(renorm)={chi:.1f}/{ndf}")
    for r in rows[:8]: print("   ",r)
    ev0,p0=a.load(d,f"corr_off_{e}"); p0["sp"]=a.species(p0)
    for sp in ("n","p","alpha"):
        A=p0[p0.sp==sp].kinetic.values;B=pr[pr.sp==sp].kinetic.values
        print("   ",sp,"off q50/90/99",np.round(np.percentile(A,[50,90,99]),3),"on",np.round(np.percentile(B,[50,90,99]),3))
    nn=pr[pr.sp=="n"].groupby("event").size()
    pn=pr[pr.sp=="n"].join(nn.rename("nn"),on="event")
    print("    on: mean n T by n count",pn.groupby("nn").kinetic.mean().round(3).to_dict(), "events",nn.value_counts().sort_index().to_dict())
