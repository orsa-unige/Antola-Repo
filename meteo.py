#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pyvantagepro import VantagePro2
from datetime import datetime, timedelta

meteo = VantagePro2.from_url("tcp:meteo.orsa.unige.net:5001")


current = meteo.get_current_data()
params0 = { k: current[k]  for k in current.keys() }

dewpoint = ( (params0['TempOut']-32)*5./9.) - ((100. - params0['HumOut'])/5.)


print(f"Datetime  {params0['Datetime'].isoformat()}")
print(f"Dew Point { dewpoint :.1f}°")
print(f"TempIn    {(params0['TempIn']-32)*5./9. :.1f}°")
print(f"TempOut   { (params0['TempOut']-32)*5./9. :.1f}°")
print(f"HumIn     { params0['HumIn']}%")
print(f"HumOut    { params0['HumOut']}%")
print(f"WindSpeed { params0['WindSpeed']*1.60934 :.1f} km/h")
print(f"Barometer { params0['Barometer']*33.8638 :.1f} hPa")


# import numpy as np
# from matplotlib import pyplot as plt
# now = datetime.now()
# older = now - timedelta(5) # max 5 days
# archive = meteo.get_archives(older, now) # takes some seconds
# params = { k: np.array([a[k] for a in archive ]) for k in archive[0].keys() }

# plt.plot(params["Datetime"], (params["TempOut"]-32)*5./9.)
# plt.plot(params["Datetime"], (params["TempIn"]-32)*5./9.)
# plt.show()

# plt.plot(params["Datetime"], params["HumOut"])
# plt.plot(params["Datetime"], params["HumIn"])
# plt.show()
