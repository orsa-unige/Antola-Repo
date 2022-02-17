#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## generic
import itertools
import signal
import shutil
import sys
import numpy as np
from time import sleep

## astropy
from astropy.coordinates import SkyCoord
from astropy.coordinates.name_resolve import NameResolveError
from astropy.modeling import models, fitting
from astropy import log
from astropy.io import fits
from astropy.time import Time

## library
import devices
import cabinet
import calibration
#from focus import fit_box2d  <- ho spostato get focus a parte.

from constants import pixscale, temp_fits, lat, lon, alt
from constants import camera_state, filter_state, filter_name


## exposure
def testimage(objname, duration=0, frametype=1, filt=None, binning=None, save=True):

    if type(objname) != str:
        raise TypeError("Insert Object name")

    ## se viene dato un filtro lo cambia
    if filt:
        devices.cam.filter = filt
        while devices.cam.is_moving != 0:
            status = devices.cam.is_moving
            log.warning(f"Filter {filter_state[status]}")
            sleep(1)

    ## se viene dato un binning lo imposta
    if binning:
        devices.cam.binning = binning

    ## RA, DEC, ALT, AZ, UTC are asked to cabinet
    ## simultaneously in order to avoid latency.
    log.info(f"Asking cabinet time and coordinates")
    cab = cabinet.ask()
    gps = Time(cab["utc"], format="unix")
    now1 = Time.now()
    log.info(f"Started counting seconds from {now1}")
    #elapsed = 0

    ## taking exposure
    devices.cam.start(duration, frametype, datetime=gps.isot)
    while devices.cam.state != 0:
        status = int(devices.cam.state)
        log.warning(f"Camera {camera_state[status]}")
        sleep(0.5)
    log.info(f"Elapsed {(Time.now()-now1).sec:.2f}")

    ##downloading image from camera
    log.info(f"Downloading frame as {temp_fits}")
    devices.cam.download()
    log.info(f"Elapsed {(Time.now()-now1).sec:.2f}")

    ## updating the .fits header
    log.info("Updating the FITS header")

    with fits.open(temp_fits, 'update') as h:
        for hdu in h:

            log.warning(f"Header Start Elapsed {(Time.now()-now1).sec:.2f}")

            hdu.header['object'] = (objname, "Object name")
            hdu.header['latitude'] = (lat, "[deg] Telescope latitude N")
            hdu.header['longitud'] = (lon, "[deg] Telescope longitude E from Greeenwich")
            hdu.header['altitude'] = (alt, "[m] Telescope height from sea level")
            hdu.header['alt'] = (cab["alt"], "[deg] Altitude at start")
            hdu.header['az'] = (cab["az"], "[deg] Azimuth clockwise from N at start")
            hdu.header['ra'] = (cab["ra"]*15.0, "[deg] Right ascension J2000 at start")
            hdu.header['dec'] = (cab["dec"], "[deg] Declination J2000 at start")
            hdu.header['equinox'] = ("J2000", "Equinox")
            hdu.header['mjd-obs'] = (gps.mjd, "[day] (MJD) Date the exposure was started")
            hdu.header['date'] = (Time.now().isot, "(UTC) Date the file was written")

            log.warning(f"Header end Coordinates Elapsed {(Time.now()-now1).sec:.2f}")

            if save and devices.tel.park == True:
                log.error(f"Telescope connection is False, could not update header")
            else:
                hdu.header['telfocus'] = (devices.foc.position, "[um] M2 position")
                hdu.header['hierarch TEL COVER'] = (devices.tel.open, "M1 cover. 1.0 if full open, 0.0 if close")
                hdu.header['hierarch TEL PARKED'] = (devices.tel.park, "True if telescope is parked")
                hdu.header['hierarch TEL ROT'] = (devices.rot.position, "[deg] Rotator position angle")
                hdu.header['hierarch TEL TEMP'] = (devices.tel.command("AUXILIARY.SENSOR[2].VALUE"), "[C] Telescope temperature")
                hdu.header['hierarch TEL M1 TEMP'] = (devices.tel.temperature[0], "[C] M1 temperature")
                hdu.header['hierarch TEL M2 TEMP'] = (devices.tel.temperature[1], "[C] M2 temperature")
                hdu.header['hierarch TEL M3 TEMP'] = (devices.tel.temperature[2], "[C] M3 temperature")

            log.warning(f"Header end Telescope Elapsed {(Time.now()-now1).sec:.2f}")

            hdu.header['hierarch DOM AZIMUTH'] = (devices.dom.azimuth, "[deg] Dome Azimuth clockwise from N")
            hdu.header['hierarch DOM LAMP'] = (devices.lamp.state, "Flat lamp. True if on, False if off")
            hdu.header['hierarch DOM LIGHT'] = (devices.light.state, "Dome light. True if on, False if off")
            hdu.header['hierarch DOM SHUTTER'] = (devices.dom.open, "Dome Shutter. False if close, True if open")
            hdu.header['hierarch DOM SLAVED'] = (devices.dom.slave, "True if dome slaved to telescope at start")

            log.warning(f"Header end Dome Elapsed {(Time.now()-now1).sec:.2f}")

            ca = devices.cam.all
            hdu.header['hierarch CAM AMBIENT'] = (ca["AmbientTemperature"], "[C] Camera ambient temperature")
            hdu.header['hierarch CAM COOLER'] = (ca["CoolerState"], "Camera cooler. True if on, False if off")
            hdu.header['hierarch CAM TEMP'] = (ca["CCDTemperature"], "[C] Camera temperature")
            hdu.header['hierarch CAM XPIXSCALE'] = round(pixscale*int(ca["BinX"]),2), "[arcsec/px] X scale of pixels in current binning"
            hdu.header['hierarch CAM YPIXSCALE'] = round(pixscale*int(ca["BinY"]),2), "[arcsec/px] Y scale of pixels in current binning"
            hdu.header['hierarch CAM XRANGE'] = (str(ca["xrange"]), "[x_start, x_end] in current binning")
            hdu.header['hierarch CAM YRANGE'] = (str(ca["yrange"]), "[y_start, y_end] in current binning")

            log.warning(f"Header end Camera Elapsed {(Time.now()-now1).sec:.2f}")

            log.info(f"Elapsed {(Time.now()-now1).sec:.2f}")

    ## saving image into namefile
    if save:
        log.info(f"Saved as OARPAF.{gps.isot}.fits")
        shutil.copy2("temp.fits", f"OARPAF.{gps.isot}.fits")

    log.info(f"Elapsed {(Time.now()-now1).sec:.2f}")

    filename = "Saved as OARPAF." + gps.isot + ".fits"
    return filename

## conversion to radec
def to_radec(string):
    try:
        coor = SkyCoord(string, unit=("hourangle","deg"), equinox=Time.now())
        return [coor.ra.hourangle, coor.dec.degree]
    except ValueError as e:
        log.warning(f"Cannot resolve coordinates, trying with name {e}")
        try:
            coor = SkyCoord.from_name(string)
            log.warning(f"Found catalog name")
            return [coor.ra.hourangle, coor.dec.degree]
        except NameResolveError as e:
            log.error(f"Cannot resolve name: {e}")

## get target and start track
def acquire(target):

    if(devices.tel.connection != True):
        log.warning(f"Telescope is not connected!")

    devices.dom.slave = True
    if(devices.dom.slave != True):
        log.warning(f"Dome not slaved!")

    if "radec" in target:
        devices.tel.targetradec = to_radec(target["radec"])
        devices.tel.track()
    elif "altaz" in target:
        devices.tel.altaz = to_radec(target["altaz"])
    else:
        raise KeyError

    while devices.tel.is_moving:
        log.info(f"Telescope is tracking? {devices.tel.tracking}")
        log.warning(f"radec: {devices.tel.radec}, altaz: {devices.tel.altaz}")
        sleep(0.5)

    log.info(f"Telescope tracking? {devices.tel.tracking}")

## estimate time needed for target
def estimate(target):
    rate = 1.8*10**6 # 1.8MHz Hz readout speed
    over = 2.3 # Minimum seconds
    xsize = target["xran"][1]-target["xran"][0]
    ysize = target["yran"][1]-target["yran"][0]
    bits = 4

    ob_time = 0
    print(f"{target['obj']}")
    for bin in target["bins"]:
        pxnum = xsize*ysize /bin**2
        readout_time = over+pxnum/rate
        weight = pxnum*bits/1024/2024
        download_time = weight/1.84 #Mb/s
        total_time = (readout_time + download_time)*target["ndit"]*len(target["filts"])
        total_dits = sum(target["dits"])*target["ndit"]*len(target["filts"])
        total = (total_dits + total_time) /60.0
        ob_time += total
        print(f"Size: {xsize//bin}x{ysize//bin}px in bin {bin}")
        print(f"Readout/image: {readout_time:.2f}s")
        print(f"Download/image: {download_time:.2f}s")
        print(f"Image weight: {weight:.1f}MB")
        print(f"Total in bin {bin}: {total:.0f}'")
        print("------------")

    print(f"Total time for this OB: {ob_time:.0f}'")

## observe target following dictionary data
def observe(target, frametype=1):

    current_binning = devices.cam.binning

    log.warning("Filters are looped first as they are the slowest")

    for filt, bin, dit, exp in itertools.product(target["filts"],
                                                 target["bins"],
                                                 target["dits"],
                                                 range(target["ndit"])):

        devices.cam.binning = [bin,bin]

        if "xran" in target:
            devices.cam.xrange = target["xran"]
        else:
            devices.cam.full_frame()

        log.info("**** ---------------------------------------")
        log.info(f"**** Filt {filter_name[filt]}, Bin {bin}, Texp {dit}, exp {exp+1}/{target['ndit']}")
        try:
            log.info("**** Calling testimage with following parameters:")
            filename = testimage(target["obj"], duration=dit, frametype=frametype, filt=filt)
        except KeyboardInterrupt as e:
            devices.cam.abort()
            signal.signal(signal.SIGINT, signal.default_int_handler)
            log.error(e)
            sys.exit(1)


    return filename

## camera initialization
def camera_init():

    status = devices.cam.state
    log.info(f"Camera state: {camera_state[status]}")

    while devices.cam.state != 0:
        status = int(devices.cam.state)
        log.warning(f"Camera {camera_state[status]}")
        sleep(1)

    log.info(f"Camera init: complete.")

## camera cooling algorithm
def camera_cooling(temperature=-35):

    camera_init()

    log.info(f"Camera temperature is {devices.cam.temperature}.")

    while devices.cam.cooler != True:
        log.info(f"Switching on cooler.")
        devices.cam.cooler = True
        sleep(0.5)

    log.info(f"Set camera temperature to {temperature}.")
    devices.cam.temperature = temperature
    camtemp = devices.cam.temperature
    trigger = 1 # degrees less than target temp. change with %?
    while camtemp-trigger >= temperature:
        log.info(f"Cooling to {temperature}: {camtemp}")
        camtemp = devices.cam.temperature
        sleep(3)

    log.info(f"Camera cooling: complete.")

## camera warming algorithm
def camera_warming(steps=5):

    camera_init()

    status = devices.cam.state
    log.info(f"Camera state: {camera_state[status]}")

    while devices.cam.state != 0:
        status = int(devices.cam.state)
        log.warning(f"Camera {camera_state[status]}")
        sleep(1)

    log.info(f"Cooling down camera softly in {steps} steps.")

    ambient = devices.cam.ambient
    camtemp = devices.cam.temperature
    log.info(f"Ambient temperature  is {ambient}.")
    for temperature in np.linspace(camtemp, ambient, steps)[1:-1]:
        log.info(f"Step: warm to {temperature}")
        devices.cam.temperature = temperature
        trigger = 3 # degrees more than target temp. change with %?
        while camtemp+trigger <= temperature:
            log.info(f"Cooling to {temperature}: {camtemp}")
            camtemp = devices.cam.temperature
            sleep(3)


    while devices.cam.cooler == True:
        log.info(f"Switching off cooler.")
        devices.cam.cooler = False
        sleep(0.5)

    log.info(f"Camera warming: complete.")

## make bias algorithm
def make_biases(target_list=calibration.bias_list):

    if type(target_list) is not list:
        target_list = [target_list]

    frametype = 2 # 2 means Bias

    for target in target_list:
        target["filts"] = [1] # U is the blinder
        target["dits"] = [0.0]
        observe(target, frametype=frametype)

##make flats algorithm
def make_flats(target_list=calibration.flat_BVRI_binning_1):

    if type(target_list) is not list:
        target_list = [target_list]

    frametype = 3 # 3 means Flat

    for target in target_list:
        observe(target, frametype=frametype)



if __name__ == '__main__':
    globals()[sys.argv[1]]()
