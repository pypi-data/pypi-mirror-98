import sys, os
import numpy as np
import osgeo.gdal as gdal

from hylite.hyimage import HyImage
from .headers import matchHeader, makeDirs, loadHeader, saveHeader

# ignore GDAL warnings
gdal.PushErrorHandler('CPLQuietErrorHandler')

def loadWithGDAL(path, dtype=np.float32, mask_zero = True):
    """
    Load an image using gdal.

    *Arguments*:
     - path = file path to the image to load
     - mask_zero = True if zero values should be masked (replaced with nan). Default is true.
    *Returns*:
     - a hyImage object
    """

    #parse file format
    _, ext = os.path.splitext(path)
    if len(ext) == 0 or 'hdr' in ext.lower() or 'dat' in ext.lower(): #load ENVI file?
        header, image = matchHeader(path)
    elif 'tif' in ext.lower() or 'png' in ext.lower() or 'jpg' in ext.lower(): #standard image formats
        image = path
        header = None
    else:
        assert False, "Error - %s is an unknown/unsupported file format." % ext

    # load header
    if not header is None:
        header = loadHeader(header)

    #load image
    try:
        raster = gdal.Open(image)  # open image
    except:
        print( "Could not load image at '%s'" % image )
        return None

    #create image object
    data = raster.ReadAsArray().T
    pj = raster.GetProjection()
    gt = raster.GetGeoTransform()
    img = HyImage(data, projection=pj, affine=gt, header=header, dtype=dtype)

    if mask_zero and img.dtype == np.float:
            img.data[img.data == 0] = np.nan #note to self: np.nan is float...

    return img


# noinspection PyUnusedLocal
def saveWithGDAL(path, image, writeHeader=True, interleave='BSQ'):
    """
    Write this image to a file.

    *Arguments*:
     - path = the path to save to.
     - image = the image to write.
     - writeHeader = true if a .hdr file will be written. Default is true.
     - interleave = data interleaving for ENVI files. Default is 'BSQ', other options are 'BIL' and 'BIP'.
    """

    # make directories if need be
    makeDirs( path )

    path, ext = os.path.splitext(path)

    if "hdr" in str.lower(ext):
        ext = ".dat"

    #get image driver
    driver = 'ENVI'
    if '.tif' in str.lower(ext):
        driver = 'GTiff'

    #todo - add support for png and jpg??

    #set byte order
    if 'little' in sys.byteorder:
        image.header['byte order'] = 0
    else:
        image.header['byte order'] = 1

    #parse data type from image array
    data = image.data
    dtype = gdal.GDT_Float32
    image.header["data type"] = 4
    image.header["interleave"] = str.lower(interleave)
    if image.data.dtype == np.int or image.data.dtype == np.int32:
        dtype = gdal.GDT_Int32
        image.header["data type"] = 3
    if image.data.dtype == np.int16:
        dtype = gdal.GDT_Int16
        image.header["data type"] = 2
    if image.data.dtype == np.uint8:
        data = np.array(image.data, np.dtype('b'))
        dtype = gdal.GDT_Byte
        image.header["data type"] = 1
    if image.data.dtype == np.uint or image.data.dtype == np.uint32:
        dtype = gdal.GDT_UInt32
        image.header["data type"] = 13
    if image.data.dtype == np.uint16:
        dtype = gdal.GDT_UInt16
        image.header["data type"] = 12

    #write
    if driver == 'GTiff':
        output = gdal.GetDriverByName(driver).Create( path + ext, image.xdim(), image.ydim(), image.band_count(), dtype)
    else:
        output = gdal.GetDriverByName(driver).Create( path + ext, image.xdim(), image.ydim(), image.band_count(), dtype, ['INTERLEAVE=%s'%interleave] )

    #write bands
    for i in range(image.band_count()):
         rb = output.GetRasterBand(i+1)
         rb.WriteArray(data[:, :, i].T)
         rb = None #close band
    output = None #close file

    if writeHeader and not image.header is None: #write .hdr file
        image.push_to_header()
        saveHeader(path + ".hdr", image.header)

    # save geotransform/project information
    output = gdal.Open(path + ext, gdal.GA_Update)
    output.SetGeoTransform(image.affine)
    if not image.projection is None:
        output.SetProjection(image.projection.ExportToPrettyWkt())
    output = None  # close file

