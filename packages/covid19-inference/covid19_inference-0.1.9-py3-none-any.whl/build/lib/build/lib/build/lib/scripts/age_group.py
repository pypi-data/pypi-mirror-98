import datetime
import copy
import sys

import pymc3 as pm
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

try:
    import covid19_inference as cov19
except ModuleNotFoundError:
    sys.path.append("../")
    import covid19_inference as cov19

"""
Range for the plots starting at 3.8. because there is
a lot of missing data beforehand
"""
bd = datetime.datetime(2020, 3, 8)
ed = datetime.datetime.today()-datetime.timedelta(days=1)

""" ## Retrieve Rki data
"""
rki = cov19.data_retrieval.RKI(True)

""" ## Get filtered data
    Once for normal Meldedatum and once using Refdatum.
"""

new = dict()
new["total_meldedatum"] = rki.get_new(
    data_begin=bd,
    data_end=ed,
    date_type="date")
new["kita_meldedatum"] = rki.get_new(
    data_begin=bd,
    data_end=ed,
    age_group="A00-A04",
    date_type="date")

new["total_refdatum"] = rki.get_new(
    data_begin=bd,
    data_end=ed,
    date_type="date_ref")
new["kita_refdatum"] = rki.get_new(
    data_begin=bd,
    data_end=ed,
    age_group="A00-A04",
    date_type="date_ref")

""" Create plot
"""
fig, axes = plt.subplots(3,1,figsize=(10,6),constrained_layout=True)
clr_kita = "tab:blue"
clr_total = "tab:red"



# Plot it
# Meldedatum
ax1 = axes[0]
ax2 = ax1.twinx() #Using two y axis in one subfigure
cov19.plot._timeseries(x=new["total_meldedatum"].index,y=new["total_meldedatum"],what="model",ax=ax1,label="All ages combined",color=clr_total)
cov19.plot._timeseries(x=new["kita_meldedatum"].index,y=new["kita_meldedatum"],what="model",ax=ax2,label="Age 0 to 4",color=clr_kita)

# Refdatum
ax3 = axes[1]
ax4 = ax3.twinx()
cov19.plot._timeseries(x=new["total_refdatum"].index,y=new["total_refdatum"],what="model",ax=ax3,label="All ages combined",color=clr_total)
cov19.plot._timeseries(x=new["kita_refdatum"].index,y=new["kita_refdatum"],what="model",ax=ax4,label="Age 0 to 4",color=clr_kita)

#Fraction
ax5 = axes[2]
ax6 = ax5.twinx()
cov19.plot._timeseries(x=new["total_meldedatum"].index,y=new["kita_meldedatum"]/new["total_meldedatum"],what="model",ax=ax5,label="Fraction age 0 to 4 (Meldedatum)",color="tab:green",ls="--")
cov19.plot._timeseries(x=new["total_refdatum"].index,y=new["kita_refdatum"]/new["total_refdatum"],what="model",ax=ax6,label="Fraction age 0 to 4 (Refdatum)",color="tab:purple",ls="--")






# Titles and labels
ax1.set_title("Epi curve using rki data (Meldedatum)")
ax1.set_ylabel("New cases\ntotal",color=clr_total)
ax2.set_ylabel("New cases\nage 0 to 4",color=clr_kita)
ax2.set_ylim(0,70)
ax1.set_ylim(0,7000)
ax2.tick_params(axis='y',labelcolor=clr_kita)
ax1.tick_params(axis='y',labelcolor=clr_total)

ax3.set_title("Epi curve using rki data (Refdatum)")
ax3.set_ylabel("New cases\ntotal",color=clr_total)
ax4.set_ylabel("New cases\nage 0 to 4",color=clr_kita)
ax4.set_ylim(0,55)
ax3.set_ylim(0,5500)
ax4.tick_params(axis='y',labelcolor=clr_kita)
ax3.tick_params(axis='y',labelcolor=clr_total)

ax5.set_title("Fraction age 0 to 4 of total new cases")
ax5.set_ylabel(f"Fraction\nusing Meldedatum",color="tab:green")
ax6.set_ylabel(f"Fraction\nusing Refdatum",color="tab:purple")
ax5.set_ylim(0,0.15)
ax6.set_ylim(0,0.15)
ax5.tick_params(axis='y',labelcolor="tab:green")
ax6.tick_params(axis='y',labelcolor="tab:purple")


plt.tight_layout()
plt.savefig("epi_age_0_4.pdf",dpi=300,transparent=True)



# Correlation
#from scipy.stats.stats import pearsonr
#print(f"Pearson correlation coefficient r = {pearsonr(total,total_kita)[0]}")
