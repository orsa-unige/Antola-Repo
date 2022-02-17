
from astropy.modeling import models, fitting
from matplotlib import pyplot as plt
from astropy.stats import sigma_clip

from astropy.io import fits
import numpy as np

#line = models.Linear1D(slope=0, intercept=950, fixed={"slope":True})
line = models.Const1D(amplitude=950)
moffat1d = models.Moffat1D(amplitude=1000)
gaussian1d = models.Gaussian1D(amplitude=1000)

#surface = models.Polynomial2D(degree=0)
surface = models.Const2D(amplitude=950)
moffat2d = models.Moffat2D(amplitude=1000)
gaussian2d = models.Gaussian2D(amplitude=1000)

fit_g = fitting.LevMarLSQFitter()


def box_image(img, x, y, box=75):
    data = fits.getdata(img)
    boxed = data[y-box//2:y+box//2,
                 x-box//2:x+box//2]
    return boxed


def sum_xy(box):
    sum_x = np.average(box, axis=0)
    sum_y = np.average(box, axis=1)
    return sum_x, sum_y


def fit_profile1d(y, model="gaussian"):

    x = np.arange(-len(y)//2+1, len(y)//2+1)

    if model == "moffat":
        f_init = line + moffat1d
    else:
        f_init = line + gaussian1d

    f_fit = fit_g(f_init, x, y)

    return f_fit


def fit_profile2d(z, model="gaussian",plot = True):

    y, x = np.mgrid[-z.shape[0]//2+1:z.shape[0]//2+1,
                    -z.shape[1]//2+1:z.shape[1]//2+1]

    if model == "moffat":
        f_init = surface + moffat2d
    else:
        f_init = surface + gaussian2d

    f_init

    print(x.shape, y.shape, z.shape)

    f_fit = fit_g(f_init, x, y, z)

    if(plot==True):
        # Plot the data with the best-fit model
        plt.figure(figsize=(8, 2.5))
        plt.subplot(1, 3, 1)
        plt.imshow(z)
        plt.title("Data")
        plt.subplot(1, 3, 2)
        plt.imshow(f_fit(x, y))
        plt.title("Model")
        plt.subplot(1, 3, 3)
        plt.imshow(z - f_fit(x, y))
        plt.title("Residual")
        plt.show()

    return f_fit

def fit_box1d(img, x=947, y=2262, box=50, model="moffat"):
    #box = box_image(img, x=x, y=y, box=box)
    x_profile, y_profile = sum_xy(img) # sum ALL the box
    x_fit = fit_profile1d(x_profile, model=model)
    y_fit = fit_profile1d(y_profile, model=model)

    if model=="moffat":
        x_fit.fwhm = 2*np.abs(x_fit.gamma_1)*np.sqrt(2**(1/x_fit.alpha_1)-1)
        y_fit.fwhm = 2*np.abs(y_fit.gamma_1)*np.sqrt(2**(1/y_fit.alpha_1)-1)
    else:
        x_fit.fwhm = 2*np.sqrt(2*np.log(2))*x_fit.stddev_1
        y_fit.fwhm = 2*np.sqrt(2*np.log(2))*y_fit.stddev_1

    plot1d(x_fit, x_profile, y_fit, y_profile)

    return x_fit, y_fit


def fit_box2d(img, model="moffat"):
    #box = box_image(img, x=x, y=y, box=box)
    xy_fit = fit_profile2d(img, model=model)

    if model=="moffat":
        fwhm = 2*np.abs(xy_fit.gamma_1)*np.sqrt(2**(1/xy_fit.alpha_1)-1)
    else:
        fwhm = 2*np.sqrt(2*np.log(2))*(xy_fit.x_stddev_1)

    xy_fit.fwhm = fwhm

    print(xy_fit)

    return xy_fit


def plot1d(x_fit, xx, y_fit, yy):
    x = np.arange(-len(xx)//2+1, len(xx)//2+1)
    y = np.arange(-len(yy)//2+1, len(yy)//2+1)

    # generate best-fit curve
    xfit = (np.linspace(x.min(),x.max(),100))
    xxfit = x_fit(xfit)

    yfit = (np.linspace(y.min(),y.max(),100))
    yyfit = y_fit(yfit)

    # plot
    fig,ax=plt.subplots()
    ax.plot(x,xx,'ob')
    ax.plot(xfit,xxfit);
    ax.plot(y,yy,'or')
    ax.plot(yfit,yyfit);
    plt.show()



## focus algorithm
def get_focus(duration=10, x=None, y=None, repeat=7, step=50, box=80, model="moffat"):

    #original_binning = devices.cam.binning
    original_xrange = devices.cam.xrange
    original_yrange = devices.cam.yrange
    original_foc = devices.foc.position

    if x is None:
        x = (original_xrange[1]-original_xrange[0])//2
    if y is None:
        y = (original_yrange[1]-original_yrange[0])//2

    devices.cam.xrange = [x-box//2, x+box//2]
    devices.cam.yrange = [y-box//2, y+box//2]

    m2 = []
    fwhm = []

    for rep in range(0, repeat):
        log.info(f"Step {rep} of {repeat-1}")
        testimage("focus", duration=duration, frametype=1, save=False)

        m2.append(devices.foc.position)

        img = fits.getdata(temp_fits)

        fitted = fit_box2d(img, model=model)
        fwhm.append(fitted.fwhm)

        log.info(f"moving focus to {devices.foc.position}")
        devices.foc.position += step

    log.info("Setting back original binning, range and focus")
    devices.cam.xrange    = original_xrange
    devices.cam.yrange    = original_yrange
    devices.foc.position  = original_foc

    print(m2, fwhm)

    plt.plot(m2, fwhm)
    plt.show()
