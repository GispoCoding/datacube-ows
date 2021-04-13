# pylint: skip-file

# THIS IS A TESTING FILE
# Please refer to datacube_ows/ows_cfg_example.py for EXAMPLE CONFIG

def read_date_range(product: str) -> (int, int):
    """ Read min and max dates from a product """
    from datacube import Datacube
    dc = Datacube(app="ows_config_file")
    ds = dc.load(product=product, resolution=(10, -10), output_crs='EPSG:4326', dask_chunks={})
    t0 = ds.time.values[0].astype("datetime64[D]").astype("uint16")
    t1 = ds.time.values[-1].astype("datetime64[D]").astype("uint16")
    return t0, t1

# REUSABLE CONFIG FRAGMENTS - Band alias maps
bands_cloudless = {
    "B01": ["red"],
    "B02": ["green"],
    "B03": ["blue"],
    "B04": ["recentness"],
}

bands_s2 = {
    "B02": ["red"],
    "B03": ["green"],
    "B04": ["blue"],
}

# REUSABLE CONFIG FRAGMENTS - Style definitions
# Examples of styles which are linear combinations of the available spectral bands.
style_rgb = {
    # Machine readable style name. (required.  Must be unique within a layer.)
    "name": "simple_rgb",
    # Human readable style title (required.  Must be unique within a layer.)
    "title": "Simple RGB",
    # Abstract - a longer human readable style description. (required. Must be unique within a layer.)
    "abstract": "Simple true-colour image, using the red, green and blue bands",
    # Components section is required for linear combination styles.
    # The component keys MUST be "red", "green" and "blue" (and optionally "alpha")
    "components": {
        "red": {
            # Band aliases may be used here.
            # Values are multipliers.  The should add to 1.0 for each component to preserve overall brightness levels,
            # but this is not enforced.
            "red": 1.0
        },
        "green": {
            "green": 1.0
        },
        "blue": {
            "blue": 1.0
        }
    },
    # The raw band value range to be compressed to an 8 bit range for the output image tiles.
    # Band values outside this range are clipped to 0 or 255 as appropriate.
    "scale_range": [0.0, 2000.0],
}

cloudless_mosaic_style = {
    "name": "cloudless_mosaic_style",
    "title": "Cloudless mosaic",
    "abstract": "Cloudless RGB mosaic",
    "components": {
        "red": {
            "B01": 1.0
        },
        "green": {
            "B02": 1.0
        },
        "blue": {
            "B03": 1.0
        }
    },
    "scale_range": [100.0, 2000.0],
}
s2cloudless_recentness_style = {
    "name": "s2cloudless_recentness",
    "title": "s2cloudless recentness",
    "abstract": "Recentness of cloudless RGB mosaic with s2cloudless masks",
    "index_function": {
        "function": "datacube_ows.band_utils.single_band",
        "kwargs": {
            "band": "B04",
        },
    },
    "needed_bands": ["B04"],
    "range": read_date_range("s2cloudless_mosaic"),
}
fmask_recentness_style = {
    "name": "fmask_recentness",
    "title": "fmask recentness",
    "abstract": "Recentness of cloudless RGB mosaic with fmask masks",
    "index_function": {
        "function": "datacube_ows.band_utils.single_band",
        "kwargs": {
            "band": "B04",
        },
    },
    "needed_bands": ["B04"],
    "range": read_date_range("fmask_mosaic"),
}
s2_style = {
    "name": "s2_style",
    "title": "s2 image style",
    "abstract": "some test style",
    "components": {
        "red": {
            "B02": 1.0
        },
        "green": {
            "B03": 1.0
        },
        "blue": {
            "B04": 1.0
        }
    },
    "scale_range": [100.0, 2000.0],
}

# REUSABLE CONFIG FRAGMENTS - resource limit declarations

standard_resource_limits = {
    "wms": {
        "zoomed_out_fill_colour": [150,180,200,160],
        "min_zoom_factor": 35.0,
        "max_datasets": 16,  # Defaults to no dataset limit
    },
    "wcs": {
        # "max_datasets": 16, # Defaults to no dataset limit
    }
}

# MAIN CONFIGURATION OBJECT

ows_cfg = {
    # Config entries in the "global" section apply to all services and all layers/coverages
    "global": {
        # These HTML headers are added to all responses
        # Optional, default {} - no added headers
        "response_headers": {
            "Access-Control-Allow-Origin": "*",  # CORS header (strongly recommended)
        },
        # Which web service(s) should be implemented by this instance
        # Optional, defaults: wms,wmts: True, wcs: False
        "services": {
            "wms": True,
            "wmts": True,
            "wcs": True
        },
        # Service title - appears e.g. in Terria catalog (required)
        "title": "Open web-services for the Open Data Cube",
        # Service URL.
        # A list of fully qualified URLs that the service can return
        # in the GetCapabilities documents based on the requesting url
        "allowed_urls": [
            "http://cfsi-dev.gispocoding.fi/",
            "http://127.0.0.1:8000/",
            "http://127.0.0.1:5000/",
            "http://localhost/odc_ows",
            "https://localhost/odc_ows",
            "https://alternateurl.domain.org/odc_ows",
        ],
        # URL that humans can visit to learn more about the service(s) or organization
        # should be fully qualified
        "info_url": "http://opendatacube.org",
        # Abstract - longer description of the service (Note this text is used for both WM(T)S and WCS)
        # Optional - defaults to empty string.
        "abstract": """This web-service serves georectified raster data from our very own special Open Datacube instance.""",
        # Keywords included for all services and products
        # Optional - defaults to empty list.
        "keywords": [
            "Sentinel-2",
            "satellite",
            "cloudless",
            "mosaic",
        ],
        # Contact info.
        # Optional but strongly recommended - defaults to blank.
        "contact_info": {
            "person": "Mikael Vaaltola",
            "organisation": "Gispo Ltd.",
            "position": "",
            "address": {
                "type": "",
                "address": "",
                "city": "",
                "state": "",
                "postcode": "",
                "country": "Finland",
            },
            "telephone": "",
            "fax": "",
            "email": "mikael@gispo.fi",
        },
        # Supported co-ordinate reference systems. Any coordinate system supported by GDAL and Proj.4J can be used.
        # At least one CRS must be included.  At least one geographic CRS must be included if WCS is active.
        # Web Mercator (EPSG:3857) and WGS-84 (EPSG:4326) are strongly recommended, but not required.
        "published_CRSs": {
            "EPSG:3857": {  # Web Mercator
                "geographic": False,
                "horizontal_coord": "x",
                "vertical_coord": "y",
            },
            "EPSG:4326": {  # WGS-84
                "geographic": True,
                "vertical_coord_first": True
            },
            "I-CANT-BELIEVE-ITS-NOT-EPSG:4326": {
                "alias": "EPSG:4326"
            },
            "EPSG:3577": {  # GDA-94, internal representation
                "geographic": False,
                "horizontal_coord": "x",
                "vertical_coord": "y",
            },
            "EPSG:32635": {
               "geographic": False,
               "horizontal_coord": "lat",
               "vertical_coord": "long",
            },

        },
        # If True the new EXPERIMENTAL materialised views are used for spatio-temporal extents.
        # If False (the default), the old "update_ranges" tables (and native ODC search methods) are used.
        # DO NOT SET THIS TO TRUE unless you understand what this means and want to participate
        # in the experiment!
        "use_extent_views": False,
    },  # End of "global" section.

    # Config items in the "wms" section apply to the WMS service (and WMTS, which is implemented as a
    # thin wrapper to the WMS code unless stated otherwise) to all WMS/WMTS layers (unless over-ridden).
    "wms": {
        # Provide S3 data URL, bucket name for data_links in GetFeatureinfo responses
        # Note that this feature is currently restricted to data stored in AWS S3.
        # This feature is also fairly specialised to DEA requirements and may not be suited to more general use.
        # All Optional
        # "s3_url": "http://data.au",
        # "s3_bucket": "s3_bucket_name",
        # "s3_aws_zone": "ap-southeast-2",
        # Max tile height/width for wms.  (N.B. Does not apply to WMTS)
        # Optional, defaults to 256x256
        "max_width": 512,
        "max_height": 512,
        # Attribution. This provides a way to identify the source of the data used in a layer or layers.
        # This entire section is optional.  If provided, it is taken as the
        # default attribution for any layer that does not override it.
        "attribution": {
            # Attribution must contain at least one of ("title", "url" and "logo")
            # A human readable title for the attribution - e.g. the name of the attributed organisation
            "title": "Acme Satellites",
            # The associated - e.g. URL for the attributed organisation
            "url": "http://www.acme.com/satellites",
            # Logo image - e.g. for the attributed organisation
            "logo": {
                # Image width in pixels (optional)
                "width": 370,
                # Image height in pixels (optional)
                "height": 73,
                # URL for the logo image. (required if logo specified)
                "url": "https://www.acme.com/satellites/images/acme-370x73.png",
                # Image MIME type for the logo - should match type referenced in the logo url (required if logo specified.)
                "format": "image/png",
            }
        },
        # These define the AuthorityURLs.
        # They represent the authorities that define the "Identifiers" defined layer by layer below.
        # The spec allows AuthorityURLs to be defined anywhere on the Layer heirarchy, but datacube_ows treats them
        # as global entities.
        # Required if identifiers are to be declared for any layer.
        "authorities": {
            # The authorities dictionary maps names to authority urls.
            "auth": "https://authoritative-authority.com",
            "idsrus": "https://www.identifiers-r-us.com",
        }
    },  # End of "wms" section.

    # Config items in the "wcs" section apply to the WCS service to all WCS coverages
    # (unless over-ridden).
    "wcs": {
        # Must be a geographic CRS in the global published_CRSs list.
        # EPSG:4326 is recommended, but any geographic CRS should work.
        "default_geographic_CRS": "EPSG:4326",
        # Supported WCS formats
        # NetCDF and GeoTIFF work "out of the box".  Other formats will require writing a Python function
        # to do the rendering.
        "formats": {
            # Key is the format name, as used in DescribeCoverage XML
            "GeoTIFF": {
                # Renderer is the FQN of a Python function that takes:
                #   * A WCSRequest object
                #   * Some ODC data to be rendered.
                "renderers": {
                    "1": "datacube_ows.wcs1_utils.get_tiff",
                    "2": "datacube_ows.wcs2_utils.get_tiff",
                },
                # The MIME type of the image, as used in the Http Response.
                "mime": "image/geotiff",
                # The file extension to add to the filename.
                "extension": "tif",
                # Whether or not the file format supports multiple time slices.
                "multi-time": False
            },
            "netCDF": {
                "renderers": {
                    "1": "datacube_ows.wcs1_utils.get_netcdf",
                    "2": "datacube_ows.wcs2_utils.get_netcdf",
                },
                "mime": "application/x-netcdf",
                "extension": "nc",
                "multi-time": True,
            }
        },
        # The wcs:native_format must be declared in wcs:formats dict above.
        "native_format": "GeoTIFF",
    },  # End of "wcs" section

    # Products published by this datacube_ows instance.
    # The layers section is a list of layer definitions.  Each layer may be either:
    # 1) A folder-layer.  Folder-layers are not named and can contain a list of child layers.  Folder-layers are
    #    only used by WMS and WMTS - WCS does not support a hierarchical index of coverages.
    # 2) A mappable named layer that can be requested in WMS GetMap or WMTS GetTile requests.  A mappable named layer
    #    is also a coverage, that may be requested in WCS DescribeCoverage or WCS GetCoverage requests.
    "layers": [
        {
            "title": "s2cloudless",
            "name": "s2cloudless",
            "abstract": "cloudless s2cloudless mosaic",
            "product_name": "s2cloudless_mosaic",
            "bands": bands_cloudless,
            "resource_limits": standard_resource_limits,
            "image_processing": {
                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                "always_fetch_bands": [],
            },
            "wcs": {
               "native_crs": "EPSG:32635",
               "default_bands": ["B01", "B02", "B03"],
               "native_resolution": [10, -10],
            },
            "styling": {
                "default_style": "cloudless_mosaic_style",
                "styles": [
                    cloudless_mosaic_style,
                    s2cloudless_recentness_style,
                ]
            }
        },
        {
            "title": "fmask",
            "name": "fmask",
            "abstract": "cloudless fmask mosaic",
            "product_name": "fmask_mosaic",
            "bands": bands_cloudless,
            "resource_limits": standard_resource_limits,
            "image_processing": {
                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                "always_fetch_bands": [],
            },
            "wcs": {
               "native_crs": "EPSG:32635",
               "default_bands": ["B01", "B02", "B03"],
               "native_resolution": [10, -10],
            },
            "styling": {
                "default_style": "cloudless_mosaic_style",
                "styles": [
                    cloudless_mosaic_style,
                    fmask_recentness_style,
                ]
            }
        },
        {
            "title": "s2",
            "name": "s2",
            "abstract": "s2 images",
            "product_name": "s2_level1c_granule",
            "bands": bands_s2,
            "resource_limits": standard_resource_limits,
            "image_processing": {
                "extent_mask_func": "datacube_ows.ogc_utils.mask_by_val",
                "always_fetch_bands": [],
            },
            "wcs": {
               "native_crs": "EPSG:32635",
               "default_bands": ["B02", "B03", "B04"],
               "native_resolution": [ 10, -10 ],
            },
            "styling": {
                "default_style": "s2_style",
                "styles": [
                    s2_style,
                ]
            }
        },
    ]  # End of "layers" list.
}  # End of test configuration object
