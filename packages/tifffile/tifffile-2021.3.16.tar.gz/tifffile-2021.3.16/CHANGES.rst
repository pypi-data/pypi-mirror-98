Revisions
---------
2021.3.16
    Pass 4391 tests.
    TIFF is no longer a defended trademark.
    Add method to export fsspec ReferenceFileSystem from ZarrTiffStore (#56).
2021.3.5
    Preliminary support for EER format (#68).
    Do not warn about unknown compression (#68).
2021.3.4
    Fix reading multi-file, multi-series OME-TIFF (#67).
    Detect ScanImage 2021 files (#46).
    Shape new version ScanImage series according to metadata (breaking).
    Remove Description key from TiffFile.scanimage_metadata dict (breaking).
    Also return ScanImage version from read_scanimage_metadata (breaking).
    Fix docstrings.
2021.2.26
    Squeeze axes of LSM series by default (breaking).
    Add option to preserve single dimensions when reading from series (WIP).
    Do not allow appending to OME-TIFF files.
    Fix reading STK files without name attribute in metadata.
    Make TIFF constants multi-thread safe and pickleable (#64).
    Add detection of NDTiffStorage MajorVersion to read_micromanager_metadata.
    Support ScanImage v4 files in read_scanimage_metadata.
2021.2.1
    Fix multi-threaded access of ZarrTiffStores using same TiffFile instance.
    Use fallback zlib and lzma codecs with imagecodecs lite builds.
    Open Olympus and Panasonic RAW files for parsing, albeit not supported.
    Support X2 and X4 differencing found in DNG.
    Support reading JPEG_LOSSY compression found in DNG.
2021.1.14
    Try ImageJ series if OME series fails (#54)
    Add option to use pages as chunks in ZarrFileStore (experimental).
    Fix reading from file objects with no readinto function.
2021.1.11
    Fix test errors on PyPy.
    Fix decoding bitorder with imagecodecs >= 2021.1.11.
2021.1.8
    Decode float24 using imagecodecs >= 2021.1.8.
    Consolidate reading of segments if possible.
2020.12.8
    Fix corrupted ImageDescription in multi shaped series if buffer too small.
    Fix libtiff warning that ImageDescription contains null byte in value.
    Fix reading invalid files using JPEG compression with palette colorspace.
2020.12.4
    Fix reading some JPEG compressed CFA images.
    Make index of SubIFDs a tuple.
    Pass through FileSequence.imread arguments in imread.
    Do not apply regex flags to FileSequence axes patterns (breaking).
2020.11.26
    Add option to pass axes metadata to ImageJ writer.
    Pad incomplete tiles passed to TiffWriter.write (#38).
    Split TiffTag constructor (breaking).
    Change TiffTag.dtype to TIFF.DATATYPES (breaking).
    Add TiffTag.overwrite method.
    Add script to change ImageDescription in files.
    Add TiffWriter.overwrite_description method (WIP).
2020.11.18
    Support writing SEPARATED color space (#37).
    Use imagecodecs.deflate codec if available.
    Fix SCN and NDPI series with Z dimensions.
    Add TiffReader alias for TiffFile.
    TiffPage.is_volumetric returns True if ImageDepth > 1.
    Zarr store getitem returns numpy arrays instead of bytes.
2020.10.1
    Formally deprecate unused TiffFile parameters (scikit-image #4996).
2020.9.30
    Allow to pass additional arguments to compression codecs.
    Deprecate TiffWriter.save method (use TiffWriter.write).
    Deprecate TiffWriter.save compress parameter (use compression).
    Remove multifile parameter from TiffFile (breaking).
    Pass all is_flag arguments from imread to TiffFile.
    Do not byte-swap JPEG2000, WEBP, PNG, JPEGXR segments in TiffPage.decode.
2020.9.29
    Fix reading files produced by ScanImage > 2015 (#29).
2020.9.28
    Derive ZarrStore from MutableMapping.
    Support zero shape ZarrTiffStore.
    Fix ZarrFileStore with non-TIFF files.
    Fix ZarrFileStore with missing files.
    Cache one chunk in ZarrFileStore.
    Keep track of already opened files in FileCache.
    Change parse_filenames function to return zero-based indices.
    Remove reopen parameter from asarray (breaking).
    Rename FileSequence.fromfile to imread (breaking).
2020.9.22
    Add experimental zarr storage interface (WIP).
    Remove unused first dimension from TiffPage.shaped (breaking).
    Move reading of STK planes to series interface (breaking).
    Always use virtual frames for ScanImage files.
    Use DimensionOrder to determine axes order in OmeXml.
    Enable writing striped volumetric images.
    Keep complete dataoffsets and databytecounts for TiffFrames.
    Return full size tiles from Tiffpage.segments.
    Rename TiffPage.is_sgi property to is_volumetric (breaking).
    Rename TiffPageSeries.is_pyramid to is_pyramidal (breaking).
    Fix TypeError when passing jpegtables to non-JPEG decode method (#25).
2020.9.3
    Do not write contiguous series by default (breaking).
    Allow to write to SubIFDs (WIP).
    Fix writing F-contiguous numpy arrays (#24).
2020.8.25
    Do not convert EPICS timeStamp to datetime object.
    Read incompletely written Micro-Manager image file stack header (#23).
    Remove tag 51123 values from TiffFile.micromanager_metadata (breaking).
2020.8.13
    Use tifffile metadata over OME and ImageJ for TiffFile.series (breaking).
    Fix writing iterable of pages with compression (#20).
    Expand error checking of TiffWriter data, dtype, shape, and tile arguments.
2020.7.24
    Parse nested OmeXml metadata argument (WIP).
    Do not lazy load TiffFrame JPEGTables.
    Fix conditionally skipping some tests.
2020.7.22
    Do not auto-enable OME-TIFF if description is passed to TiffWriter.save.
    Raise error writing empty bilevel or tiled images.
    Allow to write tiled bilevel images.
    Allow to write multi-page TIFF from iterable of single page images (WIP).
    Add function to validate OME-XML.
    Correct Philips slide width and length.
2020.7.17
    Initial support for writing OME-TIFF (WIP).
    Return samples as separate dimension in OME series (breaking).
    Fix modulo dimensions for multiple OME series.
    Fix some test errors on big endian systems (#18).
    Fix BytesWarning.
    Allow to pass TIFF.PREDICTOR values to TiffWriter.save.
2020.7.4
    Deprecate support for Python 3.6 (NEP 29).
    Move pyramidal subresolution series to TiffPageSeries.levels (breaking).
    Add parser for SVS, SCN, NDPI, and QPI pyramidal series.
    Read single-file OME-TIFF pyramids.
    Read NDPI files > 4 GB (#15).
    Include SubIFDs in generic series.
    Preliminary support for writing packed integer arrays (#11, WIP).
    Read more LSM info subrecords.
    Fix missing ReferenceBlackWhite tag for YCbCr photometrics.
    Fix reading lossless JPEG compressed DNG files.
2020.6.3
    Support os.PathLike file names (#9).
2020.5.30
    Re-add pure Python PackBits decoder.
2020.5.25
    Make imagecodecs an optional dependency again.
    Disable multi-threaded decoding of small LZW compressed segments.
    Fix caching of TiffPage.decode method.
    Fix xml.etree.cElementTree ImportError on Python 3.9.
    Fix tostring DeprecationWarning.
2020.5.11
    Fix reading ImageJ grayscale mode RGB images (#6).
    Remove napari reader plugin.
2020.5.7
    Add napari reader plugin (tentative).
    Fix writing single tiles larger than image data (#3).
    Always store ExtraSamples values in tuple (breaking).
2020.5.5
    Allow to write tiled TIFF from iterable of tiles (WIP).
    Add method to iterate over decoded segments of TiffPage (WIP).
    Pass chunks of segments to ThreadPoolExecutor.map to reduce memory usage.
    Fix reading invalid files with too many strips.
    Fix writing over-aligned image data.
    Detect OME-XML without declaration (#2).
    Support LERC compression (WIP).
    Delay load imagecodecs functions.
    Remove maxsize parameter from asarray (breaking).
    Deprecate ijmetadata parameter from TiffWriter.save (use metadata).
2020.2.16
    Add method to decode individual strips or tiles.
    Read strips and tiles in order of their offsets.
    Enable multi-threading when decompressing multiple strips.
    Replace TiffPage.tags dictionary with TiffTags (breaking).
    Replace TIFF.TAGS dictionary with TiffTagRegistry.
    Remove TIFF.TAG_NAMES (breaking).
    Improve handling of TiffSequence parameters in imread.
    Match last uncommon parts of file paths to FileSequence pattern (breaking).
    Allow letters in FileSequence pattern for indexing well plate rows.
    Allow to reorder axes in FileSequence.
    Allow to write > 4 GB arrays to plain TIFF when using compression.
    Allow to write zero size numpy arrays to nonconformant TIFF (tentative).
    Fix xml2dict.
    Require imagecodecs >= 2020.1.31.
    Remove support for imagecodecs-lite (breaking).
    Remove verify parameter to asarray method (breaking).
    Remove deprecated lzw_decode functions (breaking).
    Remove support for Python 2.7 and 3.5 (breaking).
2019.7.26
    Fix infinite loop reading more than two tags of same code in IFD.
    Delay import of logging module.
2019.7.20
    Fix OME-XML detection for files created by Imaris.
    Remove or replace assert statements.
2019.7.2
    Do not write SampleFormat tag for unsigned data types.
    Write ByteCount tag values as SHORT or LONG if possible.
    Allow to specify axes in FileSequence pattern via group names.
    Add option to concurrently read FileSequence using threads.
    Derive TiffSequence from FileSequence.
    Use str(datetime.timedelta) to format Timer duration.
    Use perf_counter for Timer if possible.
2019.6.18
    Fix reading planar RGB ImageJ files created by Bio-Formats.
    Fix reading single-file, multi-image OME-TIFF without UUID.
    Presume LSM stores uncompressed images contiguously per page.
    Reformat some complex expressions.
2019.5.30
    Ignore invalid frames in OME-TIFF.
    Set default subsampling to (2, 2) for RGB JPEG compression.
    Fix reading and writing planar RGB JPEG compression.
    Replace buffered_read with FileHandle.read_segments.
    Include page or frame numbers in exceptions and warnings.
    Add Timer class.
2019.5.22
    Add optional chroma subsampling for JPEG compression.
    Enable writing PNG, JPEG, JPEGXR, and JPEG2K compression (WIP).
    Fix writing tiled images with WebP compression.
    Improve handling GeoTIFF sparse files.
2019.3.18
    Fix regression decoding JPEG with RGB photometrics.
    Fix reading OME-TIFF files with corrupted but unused pages.
    Allow to load TiffFrame without specifying keyframe.
    Calculate virtual TiffFrames for non-BigTIFF ScanImage files > 2GB.
    Rename property is_chroma_subsampled to is_subsampled (breaking).
    Make more attributes and methods private (WIP).
2019.3.8
    Fix MemoryError when RowsPerStrip > ImageLength.
    Fix SyntaxWarning on Python 3.8.
    Fail to decode JPEG to planar RGB (tentative).
    Separate public from private test files (WIP).
    Allow testing without data files or imagecodecs.
2019.2.22
    Use imagecodecs-lite as a fallback for imagecodecs.
    Simplify reading numpy arrays from file.
    Use TiffFrames when reading arrays from page sequences.
    Support slices and iterators in TiffPageSeries sequence interface.
    Auto-detect uniform series.
    Use page hash to determine generic series.
    Turn off TiffPages cache (tentative).
    Pass through more parameters in imread.
    Discontinue movie parameter in imread and TiffFile (breaking).
    Discontinue bigsize parameter in imwrite (breaking).
    Raise TiffFileError in case of issues with TIFF structure.
    Return TiffFile.ome_metadata as XML (breaking).
    Ignore OME series when last dimensions are not stored in TIFF pages.
2019.2.10
    Assemble IFDs in memory to speed-up writing on some slow media.
    Handle discontinued arguments fastij, multifile_close, and pages.
2019.1.30
    Use black background in imshow.
    Do not write datetime tag by default (breaking).
    Fix OME-TIFF with SamplesPerPixel > 1.
    Allow 64-bit IFD offsets for NDPI (files > 4GB still not supported).
2019.1.4
    Fix decoding deflate without imagecodecs.
2019.1.1
    Update copyright year.
    Require imagecodecs >= 2018.12.16.
    Do not use JPEG tables from keyframe.
    Enable decoding large JPEG in NDPI.
    Decode some old-style JPEG.
    Reorder OME channel axis to match PlanarConfiguration storage.
    Return tiled images as contiguous arrays.
    Add decode_lzw proxy function for compatibility with old czifile module.
    Use dedicated logger.
2018.11.28
    Make SubIFDs accessible as TiffPage.pages.
    Make parsing of TiffSequence axes pattern optional (breaking).
    Limit parsing of TiffSequence axes pattern to file names, not path names.
    Do not interpolate in imshow if image dimensions <= 512, else use bilinear.
    Use logging.warning instead of warnings.warn in many cases.
    Fix numpy FutureWarning for out == 'memmap'.
    Adjust ZSTD and WebP compression to libtiff-4.0.10 (WIP).
    Decode old-style LZW with imagecodecs >= 2018.11.8.
    Remove TiffFile.qptiff_metadata (QPI metadata are per page).
    Do not use keyword arguments before variable positional arguments.
    Make either all or none return statements in a function return expression.
    Use pytest parametrize to generate tests.
    Replace test classes with functions.
2018.11.6
    Rename imsave function to imwrite.
    Readd Python implementations of packints, delta, and bitorder codecs.
    Fix TiffFrame.compression AttributeError.
2018.10.18
    Rename tiffile package to tifffile.
2018.10.10
    Read ZIF, the Zoomable Image Format (WIP).
    Decode YCbCr JPEG as RGB (tentative).
    Improve restoration of incomplete tiles.
    Allow to write grayscale with extrasamples without specifying planarconfig.
    Enable decoding of PNG and JXR via imagecodecs.
    Deprecate 32-bit platforms (too many memory errors during tests).
2018.9.27
    Read Olympus SIS (WIP).
    Allow to write non-BigTIFF files up to ~4 GB (fix).
    Fix parsing date and time fields in SEM metadata.
    Detect some circular IFD references.
    Enable WebP codecs via imagecodecs.
    Add option to read TiffSequence from ZIP containers.
    Remove TiffFile.isnative.
    Move TIFF struct format constants out of TiffFile namespace.
2018.8.31
    Fix wrong TiffTag.valueoffset.
    Towards reading Hamamatsu NDPI (WIP).
    Enable PackBits compression of byte and bool arrays.
    Fix parsing NULL terminated CZ_SEM strings.
2018.8.24
    Move tifffile.py and related modules into tiffile package.
    Move usage examples to module docstring.
    Enable multi-threading for compressed tiles and pages by default.
    Add option to concurrently decode image tiles using threads.
    Do not skip empty tiles (fix).
    Read JPEG and J2K compressed strips and tiles.
    Allow floating-point predictor on write.
    Add option to specify subfiletype on write.
    Depend on imagecodecs package instead of _tifffile, lzma, etc modules.
    Remove reverse_bitorder, unpack_ints, and decode functions.
    Use pytest instead of unittest.
2018.6.20
    Save RGBA with unassociated extrasample by default (breaking).
    Add option to specify ExtraSamples values.
2018.6.17 (included with 0.15.1)
    Towards reading JPEG and other compressions via imagecodecs package (WIP).
    Read SampleFormat VOID as UINT.
    Add function to validate TIFF using 'jhove -m TIFF-hul'.
    Save bool arrays as bilevel TIFF.
    Accept pathlib.Path as filenames.
    Move 'software' argument from TiffWriter __init__ to save.
    Raise DOS limit to 16 TB.
    Lazy load LZMA and ZSTD compressors and decompressors.
    Add option to save IJMetadata tags.
    Return correct number of pages for truncated series (fix).
    Move EXIF tags to TIFF.TAG as per TIFF/EP standard.
2018.2.18
    Always save RowsPerStrip and Resolution tags as required by TIFF standard.
    Do not use badly typed ImageDescription.
    Coerce bad ASCII string tags to bytes.
    Tuning of __str__ functions.
    Fix reading 'undefined' tag values.
    Read and write ZSTD compressed data.
    Use hexdump to print bytes.
    Determine TIFF byte order from data dtype in imsave.
    Add option to specify RowsPerStrip for compressed strips.
    Allow memory-map of arrays with non-native byte order.
    Attempt to handle ScanImage <= 5.1 files.
    Restore TiffPageSeries.pages sequence interface.
    Use numpy.frombuffer instead of fromstring to read from binary data.
    Parse GeoTIFF metadata.
    Add option to apply horizontal differencing before compression.
    Towards reading PerkinElmer QPI (QPTIFF, no test files).
    Do not index out of bounds data in tifffile.c unpackbits and decodelzw.
2017.9.29
    Many backward incompatible changes improving speed and resource usage:
    Add detail argument to __str__ function. Remove info functions.
    Fix potential issue correcting offsets of large LSM files with positions.
    Remove TiffFile sequence interface; use TiffFile.pages instead.
    Do not make tag values available as TiffPage attributes.
    Use str (not bytes) type for tag and metadata strings (WIP).
    Use documented standard tag and value names (WIP).
    Use enums for some documented TIFF tag values.
    Remove 'memmap' and 'tmpfile' options; use out='memmap' instead.
    Add option to specify output in asarray functions.
    Add option to concurrently decode pages using threads.
    Add TiffPage.asrgb function (WIP).
    Do not apply colormap in asarray.
    Remove 'colormapped', 'rgbonly', and 'scale_mdgel' options from asarray.
    Consolidate metadata in TiffFile _metadata functions.
    Remove non-tag metadata properties from TiffPage.
    Add function to convert LSM to tiled BIN files.
    Align image data in file.
    Make TiffPage.dtype a numpy.dtype.
    Add 'ndim' and 'size' properties to TiffPage and TiffPageSeries.
    Allow imsave to write non-BigTIFF files up to ~4 GB.
    Only read one page for shaped series if possible.
    Add memmap function to create memory-mapped array stored in TIFF file.
    Add option to save empty arrays to TIFF files.
    Add option to save truncated TIFF files.
    Allow single tile images to be saved contiguously.
    Add optional movie mode for files with uniform pages.
    Lazy load pages.
    Use lightweight TiffFrame for IFDs sharing properties with key TiffPage.
    Move module constants to 'TIFF' namespace (speed up module import).
    Remove 'fastij' option from TiffFile.
    Remove 'pages' parameter from TiffFile.
    Remove TIFFfile alias.
    Deprecate Python 2.
    Require enum34 and futures packages on Python 2.7.
    Remove Record class and return all metadata as dict instead.
    Add functions to parse STK, MetaSeries, ScanImage, SVS, Pilatus metadata.
    Read tags from EXIF and GPS IFDs.
    Use pformat for tag and metadata values.
    Fix reading some UIC tags.
    Do not modify input array in imshow (fix).
    Fix Python implementation of unpack_ints.
2017.5.23
    Write correct number of SampleFormat values (fix).
    Use Adobe deflate code to write ZIP compressed files.
    Add option to pass tag values as packed binary data for writing.
    Defer tag validation to attribute access.
    Use property instead of lazyattr decorator for simple expressions.
2017.3.17
    Write IFDs and tag values on word boundaries.
    Read ScanImage metadata.
    Remove is_rgb and is_indexed attributes from TiffFile.
    Create files used by doctests.
2017.1.12 (included with scikit-image 0.14.x)
    Read Zeiss SEM metadata.
    Read OME-TIFF with invalid references to external files.
    Rewrite C LZW decoder (5x faster).
    Read corrupted LSM files missing EOI code in LZW stream.
2017.1.1
    Add option to append images to existing TIFF files.
    Read files without pages.
    Read S-FEG and Helios NanoLab tags created by FEI software.
    Allow saving Color Filter Array (CFA) images.
    Add info functions returning more information about TiffFile and TiffPage.
    Add option to read specific pages only.
    Remove maxpages argument (breaking).
    Remove test_tifffile function.
2016.10.28
    Improve detection of ImageJ hyperstacks.
    Read TVIPS metadata created by EM-MENU (by Marco Oster).
    Add option to disable using OME-XML metadata.
    Allow non-integer range attributes in modulo tags (by Stuart Berg).
2016.6.21
    Do not always memmap contiguous data in page series.
2016.5.13
    Add option to specify resolution unit.
    Write grayscale images with extra samples when planarconfig is specified.
    Do not write RGB color images with 2 samples.
    Reorder TiffWriter.save keyword arguments (breaking).
2016.4.18
    TiffWriter, imread, and imsave accept open binary file streams.
2016.04.13
    Fix reversed fill order in 2 and 4 bps images.
    Implement reverse_bitorder in C.
2016.03.18
    Fix saving additional ImageJ metadata.
2016.2.22
    Write 8 bytes double tag values using offset if necessary (bug fix).
    Add option to disable writing second image description tag.
    Detect tags with incorrect counts.
    Disable color mapping for LSM.
2015.11.13
    Read LSM 6 mosaics.
    Add option to specify directory of memory-mapped files.
    Add command line options to specify vmin and vmax values for colormapping.
2015.10.06
    New helper function to apply colormaps.
    Renamed is_palette attributes to is_indexed (breaking).
    Color-mapped samples are now contiguous (breaking).
    Do not color-map ImageJ hyperstacks (breaking).
    Towards reading Leica SCN.
2015.9.25
    Read images with reversed bit order (FillOrder is LSB2MSB).
2015.9.21
    Read RGB OME-TIFF.
    Warn about malformed OME-XML.
2015.9.16
    Detect some corrupted ImageJ metadata.
    Better axes labels for 'shaped' files.
    Do not create TiffTag for default values.
    Chroma subsampling is not supported.
    Memory-map data in TiffPageSeries if possible (optional).
2015.8.17
    Write ImageJ hyperstacks (optional).
    Read and write LZMA compressed data.
    Specify datetime when saving (optional).
    Save tiled and color-mapped images (optional).
    Ignore void bytecounts and offsets if possible.
    Ignore bogus image_depth tag created by ISS Vista software.
    Decode floating-point horizontal differencing (not tiled).
    Save image data contiguously if possible.
    Only read first IFD from ImageJ files if possible.
    Read ImageJ 'raw' format (files larger than 4 GB).
    TiffPageSeries class for pages with compatible shape and data type.
    Try to read incomplete tiles.
    Open file dialog if no filename is passed on command line.
    Ignore errors when decoding OME-XML.
    Rename decoder functions (breaking).
2014.8.24
    TiffWriter class for incremental writing images.
    Simplify examples.
2014.8.19
    Add memmap function to FileHandle.
    Add function to determine if image data in TiffPage is memory-mappable.
    Do not close files if multifile_close parameter is False.
2014.8.10
    Return all extrasamples by default (breaking).
    Read data from series of pages into memory-mapped array (optional).
    Squeeze OME dimensions (breaking).
    Workaround missing EOI code in strips.
    Support image and tile depth tags (SGI extension).
    Better handling of STK/UIC tags (breaking).
    Disable color mapping for STK.
    Julian to datetime converter.
    TIFF ASCII type may be NULL separated.
    Unwrap strip offsets for LSM files greater than 4 GB.
    Correct strip byte counts in compressed LSM files.
    Skip missing files in OME series.
    Read embedded TIFF files.
2014.2.05
    Save rational numbers as type 5 (bug fix).
2013.12.20
    Keep other files in OME multi-file series closed.
    FileHandle class to abstract binary file handle.
    Disable color mapping for bad OME-TIFF produced by bio-formats.
    Read bad OME-XML produced by ImageJ when cropping.
2013.11.3
    Allow zlib compress data in imsave function (optional).
    Memory-map contiguous image data (optional).
2013.10.28
    Read MicroManager metadata and little-endian ImageJ tag.
    Save extra tags in imsave function.
    Save tags in ascending order by code (bug fix).
2012.10.18
    Accept file like objects (read from OIB files).
2012.8.21
    Rename TIFFfile to TiffFile and TIFFpage to TiffPage.
    TiffSequence class for reading sequence of TIFF files.
    Read UltraQuant tags.
    Allow float numbers as resolution in imsave function.
2012.8.3
    Read MD GEL tags and NIH Image header.
2012.7.25
    Read ImageJ tags.
    ...