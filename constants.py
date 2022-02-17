
# Telescope
lat = 44.5912
lon = 9.2034
alt = 1469
flat_position = [24,240]


shutter_state = {
    0 : "Open",
    1 : "Closed",
    2 : "Opening",
    3 : "Closing",
    4 : "Error"
}

# Camera
xmax = [0,4145]
ymax = [0,4126]

pixscale = 0.29 # arcsec/px in binning 1

temp_fits = "temp.fits"

filter_state = {
    0 : "Idle",
    1 : "Moving",
    2 : "Error",
}

filter_name = {
    1: "U",
    2: "B",
    3: "V",
    4: "R",
    5: "I",
    6: "Halpha",
    7: "Free",
}

camera_state = {
    0 : "Idle",
    2 : "Exposing",
    3 : "Readout",
    5 : "Error",
}

frame_type = {
    0 : "Dark",
    1 : "Light",
    2 : "Bias",
    3 : "Flat",
}
