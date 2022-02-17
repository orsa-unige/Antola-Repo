#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import sys
from astropy.time import Time
from urllib.parse import urlencode
import time

URL = "http://orsa-windows.orsa.unige.net:533/api/v1"
CAM = "http://ccd-sbig.orsa.unige.net/api"
PARK = 57

def check_errors(func):
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.exceptions.HTTPError as err:
            print(f"Not found : {err}")
            return
        except requests.exceptions.Timeout:
            print("Timeout!")
            return
        except requests.exceptions.TooManyRedirects:
            print("Bad request!")
            return
        except requests.exceptions.ConnectionError as e:
            print(f"Connection refused! {e}")
            return
        except AttributeError as e:
            print(f"No data! {e}")
            return
        except requests.exceptions.RequestException as e:
            raise SystemExit(e)
    return inner_function


class Device:
    def __init__(self, dev):
        self.url = URL
        self._dev = dev # switch, dome, telescope etc.
        self.sim = 0
        self.addr = self.addr

    @property
    def addr(self):
         return f"{self.url}/{self._dev}/{self.sim}"

    @addr.setter
    def addr(self, a):
        self._addr = a

    @check_errors
    def get(self, method, params={}):
        res = requests.get(f"{self.addr}/{method}",
                           params=urlencode(params))
        res.raise_for_status()
        value = res.json()["Value"]
        return value

    @check_errors
    def put(self, method, data={}):
        res = requests.put(f"{self.addr}/{method}", data=data)
        res.raise_for_status()
        try:
            value = res.json()["Value"]
            return value
        except AttributeError as e:
            return res
        except KeyError as e:
            return res

    @property
    def actions(self):
        res = self.get("supportedactions")
        return res

    @property
    def name(self):
        res = self.get("name")
        return res

    @property
    def connection(self):
        res = self.get("connected")
        self._connection = res
        return self._connection

    @connection.setter
    def connection(self, b):
        data = {"connected":b}
        res = self.put("connected", data=data)
        self._connection = self.connection


class Switch(Device):
    def __init__(self, id=3):
        super().__init__(dev="switch")
        self.id = id

    @property
    def description(self):
        params = {"id":self.id}
        res = self.get("getswitchname", params=params)
        return res

    @property
    def state(self):
        params = {"id":self.id}
        res = self.get("getswitch", params=params)
        self._state = True if res else False
        return self._state

    @state.setter
    def state(self, s):
        data = {"id":self.id, "state": s}
        res = self.put("setswitch", data=data)
        self._state = self.state


class Dome(Device):
    def __init__(self):
        super().__init__(dev="dome")

    def park(self):
        self.slave = False
        self.azimuth = PARK

    @property
    def is_parked(self):
        res = self.get("atpark")
        self._is_parked = res
        return self._is_parked

    @property
    def is_moving(self):
        res = self.get("slewing")
        self._is_moving = res
        return self._is_moving

    @property
    def azimuth(self):
        res = self.get("azimuth")
        self._azimuth = res
        return self._azimuth

    @azimuth.setter
    def azimuth(self, a):
        data = {"azimuth": a}
        res = self.put("slewtoazimuth", data=data)
        self._azimuth = res

    @property
    def open(self):
        res = self.get("shutterstatus")
        self._open = res
        return self._open

    @open.setter
    def open(self, b):
        if b:
            res = self.put("openshutter")
        else:
            res = self.put("closeshutter")
            self._open = self.open

    @property
    def slave(self):
        res = self.get("slaved")
        self._slave = res
        return self._slave

    @slave.setter
    def slave(self, b):
         data = {"slaved": b}
         res = self.put("slaved", data=data)
         self._slave = self.slave


class Telescope(Device):
    def __init__(self):
        super().__init__(dev="telescope")

    def track(self):
        self.tracking = True
        res = self.put("slewtotarget")

    def abort(self):
        res = self.put("abortslew")

    def command(self, val, cmd="commandstring"):
        data = {"Command":val, "Raw":False}
        res = self.put(cmd, data=data)
        value = res # res.json()["Value"]
        if type(value) in [bool,int]:
            return value
        else:
            try:
                float(value)
                return float(value)
            except:
                return value
            
    def commandblind(self, val):
        value = self.command(val, cmd="commandblind")

    @property
    def is_moving(self):
        res = self.get("slewing")
        self._is_moving = res
        return self._is_moving

    @property
    def temperature(self):
        res1 = self.command("AUXILIARY.SENSOR[2].VALUE")
        res2 = self.command("AUXILIARY.SENSOR[3].VALUE")
        res3 = self.command("AUXILIARY.SENSOR[4].VALUE")
        return [round(float(res1),2),
                round(float(res2),2),
                round(float(res3),2)]

    @property
    def status(self):
        res = self.command("TELESCOPE.STATUS.LIST")
        return res

    def clear(self, n):
        res = self.command(f"TELESCOPE.STATUS.CLEAR_ERROR={n}")
        return res

    @property
    def time(self):
        res = self.command("POSITION.LOCAL.UTC")
        time = Time(res, format="unix")
        return time.isot


    
    @property
    def cover(self):
        res = self.command("AUXILIARY.COVER.REALPOS")
        self._cover = res
        return self._cover
    
    @property
    def open(self):
        res = self.cover        
        if res == 1.0 :
            self._open = True
        elif res == 0.0 :
            self._open = False
        else:
            self._open = None
        return self._open

    @open.setter
    def open(self, b):
        pos = 1.0 if b else 0.0
        res = self.commandblind(f"AUXILIARY.COVER.TARGETPOS={pos}")
        time.sleep(0.2)
        status = [int(s) for s in self.status if s.isdigit()][0]
        print(f"Error {status}")

        self._open = self.open

    @property
    def park(self):
        res = self.get("atpark")
        self._park = True if res else False
        return self._park

    @park.setter
    def park(self, b):
        if b:
            res = self.put("park")
        else:
            res = self.put("unpark")
            res = self._park
            self._park = self.park

    @property
    def altaz(self):
        alt = self.get("altitude")
        az = self.get("azimuth")
        # alt = self.command("POSITION.HORIZONTAL.alt")
        # az = self.command("POSITION.HORIZONTAL.az")
        self._altaz = [alt, az]
        return self._altaz

    @altaz.setter
    def altaz(self, a):
        self.tracking = False
        data = {"Altitude":a[0], "Azimuth": a[1]}
        res = self.put("slewtoaltazasync", data=data)
        self._altaz = self.altaz

    @property
    def targetradec(self):
        ra = self.get("targetrightascension")
        dec = self.get("targetdeclination")
        self._targetradec = [ra, dec]
        return self._targetradec

    @targetradec.setter
    def targetradec(self, a):
        data = {"targetrightascension":a[0]}
        ra = self.put("targetrightascension", data=data)
        data = {"targetdeclination":a[1]}
        dec = self.put("targetdeclination", data=data)
        self._targetradec = self.targetradec

    @property
    def radec(self):
        ra = self.get("rightascension")
        dec = self.get("declination")
        # ra = self.command("POSITION.EQUATORIAL.RA_J2000")
        # dec = self.command("POSITION.EQUATORIAL.DEC_J2000")
        self._radec = [ra, dec]
        return self._radec

    @radec.setter
    def radec(self, a):
        self.tracking = True
        data = {"RightAscension":a[0], "Declination": a[1]}
        res = self.put("slewtocoordinatesasync", data=data)
        self._radec = self.radec

    @property
    def tracking(self):
        res = self.get("tracking")
        self._tracking = res
        return self._tracking

    @tracking.setter
    def tracking(self, b):
        data = {"tracking": b}
        res = self.put("tracking", data=data)
        self._tracking = self.tracking


class Focuser(Device):
    def __init__(self):
        super().__init__(dev="focuser")

    @property
    def is_moving(self):
        res = self.get("ismoving")
        self._moving = res
        return self._moving

    @property
    def position(self):
        res = self.get("position")
        self._position = res
        return self._position

    @position.setter
    def position(self, s): # 0-34500=micron?
        data = {"position": s}
        res = self.put("move", data=data)
        self._position = self.position


class Rotator(Device):
    def __init__(self):
        super().__init__(dev="rotator")

    @property
    def is_moving(self):
        res = self.get("ismoving")
        self._moving = res
        return self._moving

    @property
    def position(self):
        res = self.get("position")
        self._position = res
        return self._position

    @position.setter
    def position(self, s): # 0-34500=micron?
        data = {"position": s}
        res = self.put("moveabsolute", data=data)
        self._position = self.position


class Camera:
    def __init__(self):
        self.url = CAM
        self.addr = self.url

    @check_errors
    def get(self, method, params=[]):
        res = requests.get(f"{self.addr}/{method}.cgi",
                           params="&".join(params))
        res.raise_for_status()
        value = res.text.split("\r\n")
        if not value[-1]:
            value = value[:-1]
        if len(value) == 1:
            value = value[0]

        try:
            int(value)
            return int(value)
        except:
            try:
                float(value)
                return float(value)
            except:
                return value

    def put(self, method, params={}):
        res = requests.get(f"{self.addr}/{method}.cgi",
                           params=urlencode(params))
        res.raise_for_status()
        text = res.text.split("\r\n")
        if not text[-1]:
            text = text[:-1]
        if len(text) == 1:
            text = text[0]
        return text


    def start(self, duration, frametype, datetime=Time.now().isot):
        params = {"Duration":duration,
                  "FrameType":frametype,
                  "DateTime":datetime}
        self.put("ImagerStartExposure", params=params)

    def abort(self):
        self.put("ImagerAbortExposure")

    def download(self):
        res = requests.get(f"{self.addr}/Imager.FIT")
        with open('temp.fits', 'wb') as f:
            f.write(res.content)
        #return fits.ImageHDU.fromstring(res.content)

    def full_frame(self):
        res = self.max_range
        self.xrange = [0, res[0]]
        self.yrange = [0, res[1]]
        return self.xrange, self.yrange

    @property
    def version(self):
        res = self.get("VersionNumbers")
        return res

    @property
    def description(self):
        res = self.get("Description")
        return res

    @property
    def state(self):
        res = self.get("ImagerState")
        return res

    @property
    def ready(self):
        res = self.get("ImagerImageReady")
        return res

    @property
    def all(self):
        params = ["AmbientTemperature",
                  "CCDTemperatureSetpoint",
                  "CCDTemperature",
                  "CoolerState",
                  "CameraXSize",
                  "CameraYSize",
                  "BinX", "BinY",
                  "StartX", "StartY",
                  "NumX", "NumY"]
        res = self.get("ImagerGetSettings", params=params)
        all_dict = dict(zip(params,res))

        x_start = int(all_dict["StartX"])//int(all_dict["BinX"])
        x_end =  int(all_dict["NumX"])//int(all_dict["BinX"]) + int(all_dict["StartX"])
        all_dict["xrange"] = [x_start, x_end]

        y_start = int(all_dict["StartY"])//int(all_dict["BinY"])
        y_end =  int(all_dict["NumY"])//int(all_dict["BinY"]) + int(all_dict["StartY"])
        all_dict["yrange"] = [y_start, y_end]

        return all_dict

    @property
    def ambient(self):
        params = ["AmbientTemperature"]
        res = self.get("ImagerGetSettings", params=params)
        return res

    @property
    def max_range(self):
        params = ["CameraXSize", "CameraYSize"]
        res = self.get("ImagerGetSettings", params=params)
        res = list(map(int, res))
        binning = self.binning
        return [r//b for r,b in zip(res, binning)]

    @property
    def is_moving(self):
        res = self.get("FilterState")
        self._is_moving = res
        return self._is_moving

    @property
    def filter(self):
        params = ["CurrentFilter", "CurrentFilterName"]
        res = self.get("GetFilterSetting", params=params)
        self._filter = res
        return self._filter

    @filter.setter
    def filter(self, n):
        params =  {"NewPosition": n}
        res = self.put("ChangeFilter", params=params)
        self._filter = self.filter

    @property
    def binning(self):
        params = ["BinX", "BinY"]
        res = self.get("ImagerGetSettings", params=params)
        self.binning = list(map(int, res))
        return self._binning

    @binning.setter
    def binning(self, b):
        params =  {"BinX":b[0], "BinY":b[1]}
        res = self.put("ImagerSetSettings", params=params)
        self._binning = b

    @property
    def temperature(self):
        params = ["CCDTemperature"]
        res = self.get("ImagerGetSettings", params=params)
        #self.temperature = res
        return res #self._temperature

    @temperature.setter
    def temperature(self, t):
        params =  {"CCDTemperatureSetpoint": t}
        res = self.put("ImagerSetSettings", params=params)
        #self._temperature = str(t)

    @property
    def cooler(self):
        params = ["CoolerState"]
        res = self.get("ImagerGetSettings", params=params)
        self.cooler = True if res else False
        return self._cooler

    @cooler.setter
    def cooler(self, b):
        s = "1" if b else "0"
        params =  {"CoolerState":s}
        res = self.put("ImagerSetSettings", params=params)
        self._cooler = b

    @property
    def xrange(self):
        params = ["StartX", "NumX", "BinX"] #start=20, width=100 (binning=1)
        startx,numx,binx = self.get("ImagerGetSettings", params=params)
        #binx = self.binning[0] # binning is 2
        x_start = int(startx)//int(binx)
        x_end =  int(numx)//int(binx) + x_start
        self.xrange = [x_start, x_end] # start=10, end=60
        return self._xrange

    @xrange.setter
    def xrange(self, b): # start=10, end=60
        binx = self.binning[0] # binning is 2
        startx = b[0]*binx # start: 10*2=20
        numx =  b[1]*binx - startx # width: 60*2-startx=100
        params =  {"StartX":startx, "NumX":numx}
        res = self.put("ImagerSetSettings", params=params)
        self._xrange = b

    @property
    def yrange(self):
        params = ["StartY", "NumY", "BinY"] #start=20, height=100 (binning=1)
        starty,numy,biny = self.get("ImagerGetSettings", params=params)
        #biny = self.binning[1] # binning is 2
        y_start = int(starty)//int(biny)
        y_end =  int(numy)//int(biny) + y_start
        self.yrange = [y_start, y_end] # start=10, end=60
        return self._yrange

    @yrange.setter
    def yrange(self, b): # start=10, end=60
        biny = self.binning[1] # binning is 2
        starty = b[0]*biny # start: 10*2=20
        numy =  b[1]*biny - starty # height: 60*2-starty=100
        params =  {"StartY":starty, "NumY":numy}
        res = self.put("ImagerSetSettings", params=params)
        self._yrange = b


tel = Telescope()
tel.sim = 1 # 0: AstelOS, 1: Hub
foc = Focuser()
rot = Rotator()
lamp = Switch(2) # Flat lamp
light = Switch(3) # Dome light
dom = Dome()
dom.sim = 1 # 0: Ricerca, 1: Hub
cam = Camera()

if __name__ == '__main__':
    import sys

    dev = sys.argv[1]
    met = sys.argv[2]
    if len(sys.argv) < 4:
        try:
            res = globals()[dev]()
        except TypeError as e:
            try:
                res = getattr(globals()[dev], met)
                print(res)
            except:
                log.error(e)
    else:
        val = sys.argv[3]
        res = setattr(globals()[dev], met, val)
        print(res)
