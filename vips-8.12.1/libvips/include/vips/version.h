/* Macros for the header version.
 */

#ifndef VIPS_VERSION_H
#define VIPS_VERSION_H

#define VIPS_VERSION		"8.12.1"
#define VIPS_VERSION_STRING	"8.12.1-Wed Nov 24 15:41:04 UTC 2021"
#define VIPS_MAJOR_VERSION	(8)
#define VIPS_MINOR_VERSION	(12)
#define VIPS_MICRO_VERSION	(1)

/* The ABI version, as used for library versioning.
 */
#define VIPS_LIBRARY_CURRENT	(56)
#define VIPS_LIBRARY_REVISION	(1)
#define VIPS_LIBRARY_AGE	(14)

#define VIPS_CONFIG		"enable debug: no, enable deprecated library components: yes, enable modules: no, use fftw3 for FFT: no, accelerate loops with orc: yes, ICC profile support with lcms: no, zlib: yes, text rendering with pangocairo: no, font file support with fontconfig: , RAD load/save: yes, Analyze7 load/save: yes, PPM load/save: yes, GIF load:  yes, EXIF metadata support with libexif: no, JPEG load/save with libjpeg: yes (pkg-config), JXL load/save with libjxl: no (dynamic module: no), JPEG2000 load/save with libopenjp2: no, PNG load with libspng: no, PNG load/save with libpng: no, quantisation to 8 bit: no, TIFF load/save with libtiff: no, image pyramid save: no, HEIC/AVIF load/save with libheif: no (dynamic module: no), WebP load/save with libwebp: no, PDF load with PDFium:  no, PDF load with poppler-glib: no (dynamic module: no), SVG load with librsvg-2.0: no, EXR load with OpenEXR: no, OpenSlide load: no (dynamic module: no), Matlab load with matio: no, NIfTI load/save with niftiio: no, FITS load/save with cfitsio: no, GIF save with cgif: no, Magick package: none (dynamic module: no), Magick API version: none, load with libMagickCore: no, save with libMagickCore: no"

/** 
 * VIPS_SONAME:
 *
 * The name of the shared object containing the vips library, for example
 * "libvips.so.42", or "libvips-42.dll".
 */

#include "soname.h"

/* Not really anything to do with versions, but this is a handy place to put
 * it.
 */
#define VIPS_EXEEXT ""
#define VIPS_ENABLE_DEPRECATED 1

#endif /*VIPS_VERSION_H*/
