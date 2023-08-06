from io import BytesIO
from pathlib import Path

import dkist_fits_specifications
import numpy as np
import pytest
from astropy.io import fits

from dkist_header_validator import spec122_validator
from dkist_header_validator import Spec122ValidationException
from dkist_header_validator.exceptions import ReturnTypeException
from dkist_header_validator.exceptions import ValidationException


@pytest.fixture(scope="module")
def valid_spec_122_headers_validate(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    header tests below.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
        "HISTORY": "Old History",
        "COMMENT": "A comment",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr.fits": Path(file_name),
        "valid_spec_122_dict": valid_spec_122_dict,
        "valid_HDUList": valid_hdu_list,
        "valid header": valid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr.fits",
        "valid_spec_122_dict",
        "valid_HDUList",
        "valid header",
    ],
)
def valid_spec_122_header_validate(request, valid_spec_122_headers_validate):
    yield valid_spec_122_headers_validate[request.param]


@pytest.fixture(scope="module")
def valid_spec_122_headers_validate_and_translate(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    header tests below.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr.fits": Path(file_name),
        "valid_spec_122_dict": valid_spec_122_dict,
        "valid_HDUList": valid_hdu_list,
        "valid header": valid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr.fits",
        "valid_spec_122_dict",
        "valid_HDUList",
        "valid header",
    ],
)
def valid_spec_122_header_validate_and_translate(
    request, valid_spec_122_headers_validate_and_translate
):
    yield valid_spec_122_headers_validate_and_translate[request.param]


def test_spec122_valid(valid_spec_122_header_validate):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return validated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_spec_122_header_validate, extra=False)


def test_spec122_valid_return_dictionary(valid_spec_122_header_validate):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return validated dictionary and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_spec_122_header_validate, return_type=dict, extra=False)


def test_spec122_WAVELNTH_not_renamed(valid_spec_122_header_validate_and_translate):
    """
    Given: A valid schema definition
    When: Validating and translating the schema
    Then: Check that the rename of keywords is correctly being renamed
    """
    default_values = [-999.9, -999, "default"]

    spec214schema = list(dkist_fits_specifications.spec214.load_spec214().values())
    headers = spec122_validator.validate_and_translate(
        valid_spec_122_header_validate_and_translate, return_type=dict, extra=False
    )

    for section in spec214schema:
        for key, schema in section.items():
            if schema.get("rename") and key in headers and headers[key] == any(default_values):
                raise Spec122ValidationException


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr.fits",
    ],
)
def valid_spec_122_file(request, valid_spec_122_headers_validate):
    yield valid_spec_122_headers_validate[request.param]


def test_spec122_valid_return_BytesIO(valid_spec_122_file):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return validated BytesIO object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_spec_122_file, return_type=BytesIO, extra=False)


@pytest.fixture(
    scope="function",
    params=[
        "valid_spec_122_dict",
        "valid_HDUList",
        "valid header",
    ],
)
def valid_spec_122_header_fail_bytesio_and_file(request, valid_spec_122_headers_validate):
    yield valid_spec_122_headers_validate[request.param]


def test_spec122_valid_return_BytesIO_failure(valid_spec_122_header_fail_bytesio_and_file):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: Raise return type exception
    """
    # raises exception on failure
    with pytest.raises(ReturnTypeException):
        spec122_validator.validate(
            valid_spec_122_header_fail_bytesio_and_file, return_type=BytesIO, extra=False
        )


def test_spec122_valid_return_fits_header(valid_spec_122_header_validate):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return validated fits.header.Header object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(
        valid_spec_122_header_validate, return_type=fits.header.Header, extra=False
    )


def test_spec122_valid_return_file_failure(valid_spec_122_header_fail_bytesio_and_file):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: raise a return type exception
    """
    # raises exception on failure
    with pytest.raises(ReturnTypeException):
        spec122_validator.validate(
            valid_spec_122_header_fail_bytesio_and_file, return_type=Path, extra=False
        )


def test_spec122_valid_return_file(valid_spec_122_file):
    """
    Validates a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return validated file and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_spec_122_file, return_type=Path, extra=False)


def test_validate_and_translate_spec122(valid_spec_122_header_validate_and_translate):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header_validate_and_translate)


def test_validate_and_translate_spec122_return_dictionary(
    valid_spec_122_header_validate_and_translate,
):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated dictionary and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(
        valid_spec_122_header_validate_and_translate, return_type=dict
    )


def test_validate_and_translate_spec122_return_BytesIO(valid_spec_122_file):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated BytesIO object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_file, return_type=BytesIO)


def test_validate_and_translate_spec122_return_fits_header(
    valid_spec_122_header_validate_and_translate,
):
    """
    Validates and tries to translate a fits header against the SPEC-122 schema
    Given: A valid SPEC-122 fits header
    When: Validating headers
    Then: return translated fits.header.Header object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(
        valid_spec_122_header_validate_and_translate, return_type=fits.header.Header
    )


def test_validate_and_translate_spec122_return_file(valid_spec_122_file):
    """
    Validates and tries to translate a fits file against the SPEC-122 schema
    Given: A valid SPEC-122 fits file
    When: Validating file
    Then: return translated file object and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_file, return_type=Path)


@pytest.fixture(scope="module")
def valid_spec_122_headers_extrakeys(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers to be used in successful
    header tests below with extra keys.
    """
    valid_spec_122_dict_extrakeys = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
        "XTRAKEY1": "ABCDEFG",
        "XTRAKEY2": "HIJKLMN",
        "XTRAKEY3": "OPQRSTU",
        "XTRAKEY4": "VWXYZAB",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_extrakeys_temp")
    file_name = temp_dir.join("tmp_fits_file_extrakeys.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu_extrakeys = fits.PrimaryHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict_extrakeys.items():
        valid_hdu_extrakeys.header[key] = value
    valid_hdu_list_extrakeys = fits.HDUList([valid_hdu_extrakeys])
    valid_hdu_list_extrakeys.writeto(str(file_name))

    yield {
        "valid_dkist_hdr_extrakeys.fits": Path(file_name),
        "valid_spec_122_dict_extrakeys": valid_spec_122_dict_extrakeys,
        "valid_HDUList_extrakeys": valid_hdu_list_extrakeys,
        "valid header_extrakeys": valid_hdu_extrakeys.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr_extrakeys.fits",
        "valid_spec_122_dict_extrakeys",
        "valid_HDUList_extrakeys",
        "valid header_extrakeys",
    ],
)
def valid_spec_122_header_extrakeys(request, valid_spec_122_headers_extrakeys):
    yield valid_spec_122_headers_extrakeys[request.param]


def test_spec122_valid_extrakeys(valid_spec_122_header_extrakeys):
    """
    Validates a fits header against the SPEC-0122 schema
    Given: A valid SPEC-0122 fits header with extra keys
    When: Validating headers
    Then: return HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header_extrakeys)


def test_spec122_valid_extrakeysfalse(valid_spec_122_header_extrakeys):
    """
    Validates a fits header against the SPEC-0122 schema
    Given: A valid SPEC-0122 fits header with extra keys
    When: Validating headers
    Then: Raise a Spec122ValidationException
    """
    with pytest.raises(Spec122ValidationException):
        spec122_validator.validate_and_translate(valid_spec_122_header_extrakeys, extra=False)


def test_spec122_valid_translate(valid_spec_122_header_validate_and_translate):
    """
    Validates a fits header against the SPEC-0122 schema
    then translates SPEC-0122 fits headers to SPEC-122 headers
    Given: A valid SPEC-0122 fits header
    When: Validating headers
    Then: return validated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_spec_122_header_validate_and_translate)


@pytest.fixture(scope="module")
def invalid_spec_122_headers(tmpdir_factory):
    """
    Create a dict of invalid spec 122 headers to be used in failing
    header tests below.
    """
    invalid_spec_122_dict = {
        "NAXIS": 2,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "WAVELNTH": "NOTSUPPOSEDTOBEASTRING",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
    }

    temp_dir = tmpdir_factory.mktemp("invalid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    invalid_hdu = fits.PrimaryHDU(temp_array)
    # Use the invalid_spec_122_dict from above to overwrite the default header
    for (key, value) in invalid_spec_122_dict.items():
        invalid_hdu.header[key] = value
    invalid_hdu_list = fits.HDUList([invalid_hdu])
    invalid_hdu_list.writeto(str(file_name))

    yield {
        "invalid_dkist_hdr.fits": Path(file_name),
        "invalid_spec_122_dict": invalid_spec_122_dict,
        "invalid_HDUList": invalid_hdu_list,
        "invalid header": invalid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "invalid_dkist_hdr.fits",
        "invalid_spec_122_dict",
        "invalid_HDUList",
        "invalid header",
    ],
)
def invalid_spec_122_header(request, invalid_spec_122_headers):
    yield invalid_spec_122_headers[request.param]


def test_validate_invalid(invalid_spec_122_header):
    """
    Validates an invalid fits header against the SPEC-0122 schema
    Given: A invalid SPEC-0122 fits header
    When: Validating headers
    Then: raise a Spec122ValidationException
    """

    with pytest.raises(Spec122ValidationException):
        spec122_validator.validate(invalid_spec_122_header)


@pytest.fixture(scope="module")
def invalid_file_params(tmpdir_factory):
    """
    Create a dict of invalid file params to be used in failing
    tests below.
    """
    temp_dir = tmpdir_factory.mktemp("invalid_file_params_temp")
    non_existent_file_name = temp_dir.join("tmp_fits_file.fits")
    non_fits_file_name = temp_dir.join("tmp_this_is_not_a_fits_file.dat")
    temp_array = np.ones(1, dtype=np.int16)
    temp_array.tofile(str(non_fits_file_name))
    yield {"file not found": non_existent_file_name, "file_not_fits": non_fits_file_name}


@pytest.fixture(scope="function", params=["file not found", "file_not_fits"])
def invalid_file_param(request, invalid_file_params):
    yield invalid_file_params[request.param]


def test_validate_file_errors(invalid_file_param):
    """
    Validates an invalid file spec
    Given: A invalid file specification: non-existent file or non-fits file
    When: Validating headers
    Then: raise a Spec122ValidationException
    """

    with pytest.raises(ValidationException):
        spec122_validator.validate(invalid_file_param)


@pytest.fixture(scope="module")
def max_headers(tmpdir_factory):
    headers = {
        "SIMPLE": True,
        "BITPIX": 16,
        "NAXIS": 3,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "BUNIT": "adu",
        "DATE": "2017-05-30T17:28:21.996",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "DATE-BGN": "2017-05-30T00:46:13.618",
        "DATE-END": "2017-05-30T00:46:13.718",
        "ORIGIN": "National Solar Observatory",
        "TELESCOP": "Daniel K. Inouye Solar Telescope",
        "OBSERVAT": "Haleakala High Altitude Observatory Site",
        "NETWORK": "DKIST",
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "OBSERVER": "8QN27LDFC7EQHKK4B3WDIN4FY7VG16",
        "OBJECT": "EAML29SS4SGV959A4GR5GNDAG1FANM",
        "CHECKSUM": "33989WFLS3IVX0LLYTQW3U1PT8AKFG",
        "DATASUM": "9WNO5RGILE66C2VLRJ45RQEBFL1IHU",
        "WCSAXES": 2,
        "WCSNAME": "Helioprojective",
        "CRPIX1": 2048.0,
        "CRPIX2": 2048.0,
        "CRDATE1": "2035-03-31T09:38:56.668",
        "CRDATE2": "2035-03-31T09:38:56.668",
        "CRVAL1": -304.9906422447552,
        "CRVAL2": -658.9384652992346,
        "CDELT1": 0.07,
        "CDELT2": 0.07,
        "CUNIT1": "arcsec",
        "CUNIT2": "arcsec",
        "CTYPE1": "HPLN-TAN",
        "CTYPE2": "HPLT-TAN",
        "PC1_1": 0.9231997511186788,
        "PC1_2": -0.3843204646312885,
        "PC2_1": 0.3843204646312885,
        "PC2_2": 0.9231997511186788,
        "LONPOLE": 180.0,
        "TAZIMUTH": 618993.1279034158,
        "TELEVATN": 819.9173809486648,
        "TELTRACK": "Standard Differential Rotation Tracking",
        "TELSCAN": "Raster",
        "TTBLANGL": 295548.0744481586,
        "TTBLTRCK": "fixed coude table angle",
        "DKIST001": "Manual",
        "DKIST002": "Full",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "DKIST005": "9CVKTL2JWMH1LHU6G3O2UPE2SO9SUW",
        "DKIST006": "Good",
        "DKIST007": False,
        "DKIST008": 999562,
        "DKIST009": 5750,
        "DKIST010": 295882,
        "ID___001": "73QYTMXIMDLCNZUEBELYY6TZ8QGYKV",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___003": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "ID___004": "MY50PNI7QUGSKLW5D8XB9N4SDKFDZ4",
        "ID___005": "59ULPBE5GG9S93M9IG63FCWMV63WAD",
        "ID___006": "7VWWG70RLGVD9AC1J9X6Y937EJIQNV",
        "ID___007": "U8M3EWALJLU5F5B96WB4QL3SN0Z1C8",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___009": "XV64I6WTJEJ93202Z5ZJ15MDBBBPRE",
        "ID___010": "KKWSIWJD2NKL11J03X51ZZR0C6FSHG",
        "ID___011": "OB6PYAI9XC3PTXLLY4I1LV26RTDEGS",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "ID___014": "UX4QYSNNFC1O99JD3TVPAGUU4XR0JB",
        "CAM__001": "ODJIY4RO6SG7T6YVHT4QVNJPVYGQW7",
        "CAM__002": "JRA5H1LSKENNLLWUZNHW9X93Z9J6G0",
        "CAM__003": 206077,
        "CAM__004": 553109.1055738949,
        "CAM__005": 931934.0145101176,
        "CAM__006": 336899.9459380526,
        "CAM__007": 450499,
        "CAM__008": 105605,
        "CAM__009": 278167,
        "CAM__010": 45681,
        "CAM__011": 882899,
        "CAM__012": 849283,
        "CAM__013": 191847,
        "CAM__014": 859469,
        "CAM__015": 208276,
        "CAM__016": 71858,
        "CAM__017": 540083,
        "CAM__018": 462616,
        "CAM__019": 763903,
        "CAM__020": 626497,
        "PAC__001": "Open",
        "PAC__002": "Clear",
        "PAC__003": "Undefined",
        "PAC__004": "Clear",
        "PAC__005": "186BGJFTFDVEOECZ80ENVCKM5RZL4U",
        "PAC__006": "NIRRetarder",
        "PAC__007": "some string",
        "PAC__008": 2.8,
        "PAC__009": 0.5,
        "PAC__010": "Undefined",
        "PAC__011": 228814.6368968824,
        "WS___001": "CYWKXJOAROTHYHNBZOD8Z7VGJITI23",
        "WS___002": 516056.5759472652,
        "WS___003": 180,
        "WS___004": 943419.0784243871,
        "WS___005": 282679.0410177523,
        "WS___006": 348537.5489154414,
        "WS___007": 870761.4045310392,
        "CRPIX3": 15.6,
        "CRVAL3": 18.6,
        "CDELT3": 78.8,
        "CUNIT3": "deg",
        "CTYPE3": "z",
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "HISTORY": "Old History",
    }

    temp_dir = tmpdir_factory.mktemp("max_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_header dict from above to overwrite the default header
    for (key, value) in headers.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield Path(str(file_name))


def test_validate_maxheaders(max_headers):
    """
    Validates a spec122 compliant header with a large number of keywords
    Given: A spec122 compliant fits file with many header keywords
    When: Validating headers
    Then: return a validated HDUList  and do not raise an exception
    """
    spec122_validator.validate(max_headers)


@pytest.fixture(scope="module")
def valid_compressed_spec_122_headers(tmpdir_factory):
    """
    Create a dict of valid compressed spec 122 headers
    to be used in successful header tests below.
    """
    valid_comp_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "BZERO": 0.0,
        "BSCALE": 1.0,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-END": "2017-05-30T00:46:13.718",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATASUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIZY",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "DATE-BGN": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "06VMAW1QQX7YYI5W3BZTAFCGX9I83Q",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
    }

    temp_dir = tmpdir_factory.mktemp("valid comp_122_headers_temp")
    file_name = temp_dir.join("tmp__comp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    primary_hdu = fits.PrimaryHDU()
    valid_comp_hdu = fits.CompImageHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_comp_122_dict.items():
        valid_comp_hdu.header[key] = value
    valid_comp_hdu_list = fits.HDUList([primary_hdu, valid_comp_hdu])
    valid_comp_hdu_list.writeto(str(file_name), checksum=True)

    yield {
        "valid_compressed_hdr.fits.fz": Path(file_name),
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_compressed_hdr.fits.fz",
    ],
)
def valid_compressed_spec_122_header(request, valid_compressed_spec_122_headers):
    yield valid_compressed_spec_122_headers[request.param]


def test_compressed_spec122_valid(valid_compressed_spec_122_header):
    """
    Validates a compressed spec122 compliant file
    Given: A valid compressed SPEC-0122 file
    When: Validating headers
    Then: return valid HDUList and do not raise an exception
    """
    spec122_validator.validate(valid_compressed_spec_122_header)


def test_compressed_spec122_validate_and_translate(valid_compressed_spec_122_header):
    """
    Validates and translates a compressed spec122 compliant file
    Given: A valid compressed SPEC-0122 file
    When: Validating headers
    Then: return valid HDUList and do not raise an exception
    """
    spec122_validator.validate_and_translate(valid_compressed_spec_122_header)


@pytest.fixture(scope="module")
def valid_visp_122_headers(tmpdir_factory):
    """
    Create a dict of valid visp spec 122 headers to be used in successful
    header tests below.
    """
    valid_visp_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "VISP_001": 3,
        "VISP_002": 32.0,
        "VISP_003": 45.6,
        "VISP_004": "string",
        "VISP_005": 31.9,
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid visp_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    # Use the valid_visp_122_dict from above to overwrite the default header
    for (key, value) in valid_visp_122_dict.items():
        valid_hdu.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_visp_hdr.fits": Path(file_name),
        "valid_visp_122_dict": valid_visp_122_dict,
        "valid_visp_HDUList": valid_hdu_list,
        "valid visp header": valid_hdu.header,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_visp_hdr.fits",
        "valid_visp_122_dict",
        "valid_visp_HDUList",
        "valid visp header",
    ],
)
def valid_visp_122_header(request, valid_visp_122_headers):
    yield valid_visp_122_headers[request.param]


def test_visp_spec122_valid(valid_visp_122_header):
    """
    Validates a visp fits header against the SPEC-122 schema
    Given: A valid visp SPEC-122 fits header
    When: Validating headers
    Then: return validated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_visp_122_header, extra=False)


def test_visp_spec122_valiate_and_translate(valid_visp_122_header):
    """
    Validates a visp fits header against the SPEC-122 schema
    Given: A valid visp SPEC-122 fits header
    When: Validating headers
    Then: return validated HDUList and do not raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(valid_visp_122_header, return_type=dict)


@pytest.fixture(scope="module")
def valid_spec_122_headers_toomanyHDUs(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU(temp_array)
    image_hdu1 = fits.ImageHDU(temp_array)
    image_hdu2 = fits.ImageHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
        image_hdu1.header[key] = value
        image_hdu2.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu, image_hdu1, image_hdu2])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr_toomanyHDUs.fits": Path(file_name),
        "valid_HDUList_toomanyHDUs": valid_hdu_list,
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr_toomanyHDUs.fits",
        "valid_HDUList_toomanyHDUs",
    ],
)
def valid_spec_122_header_toomanyHDUs(request, valid_spec_122_headers_toomanyHDUs):
    yield valid_spec_122_headers_toomanyHDUs[request.param]


def test_toomanyHDUs_validate_and_translate(valid_spec_122_header_toomanyHDUs):
    """
    Validates headers with too many (more than 2) HDUs
    Given: A valid SPEC-122 file or HDUList with more than two headers
    When: Validating and translating headers
    Then: Raise an exception
    """
    # raises exception on failure
    with pytest.raises(ValidationException):
        spec122_validator.validate_and_translate(valid_spec_122_header_toomanyHDUs)


def test_toomanyHDUs_validate(valid_spec_122_header_toomanyHDUs):
    """
    Validates headers with too many (more than 2) HDUs
    Given: A valid SPEC-122 file or HDUList with more than two headers
    When: Validating headers
    Then: Raise an exception
    """
    # raises exception on failure
    with pytest.raises(ValidationException):
        spec122_validator.validate(valid_spec_122_header_toomanyHDUs)


@pytest.fixture(scope="module")
def valid_spec_122_headers_datainsecondHDU(tmpdir_factory):
    """
    Create a dict of valid spec 122 headers.
    """
    valid_spec_122_dict = {
        "NAXIS": 3,
        "BITPIX": 16,
        "NAXIS1": 1,
        "NAXIS2": 1,
        "NAXIS3": 1,
        "INSTRUME": "VBI-BLUE",
        "WAVELNTH": 430.0,
        "DATE-BGN": "2017-05-29T12:00:13.345",
        "DATE-END": "2017-05-30T20:00:13.345",
        "CHECKSUM": "POLETJWHTN2PMM1ZPPLPWQ1KBAKIUF",
        "DATE-OBS": "2017-05-30T00:46:13.952",
        "ID___002": "YVPS4YRBSXUT9Z17Z4HRH3VIH7T6KO",
        "ID___008": "JX3O8NXFI6FGTVZ1D7G7U8OVUWDZQL",
        "ID___012": "1XXPIDR5CEXMZ0SQ8LT3HMF83FW4HJ",
        "ID___013": "2KJBWEFB4OUUBSFUIB5JKBSDF8JBSK",
        "DKIST003": "OSZ4FBHWKXRWQGOVG9BJNUWNG5795B",
        "DKIST004": "Observation",
        "WCSAXES": 3,
        "WCSNAME": "Helioprojective Cartesian",
        "CRPIX1": 13.4,
        "CRPIX2": 14.6,
        "CRPIX3": 15.6,
        "CRVAL1": 16.7,
        "CRVAL2": 18.5,
        "CRVAL3": 18.6,
        "CDELT1": 20.4,
        "CDELT2": 67.8,
        "CDELT3": 78.8,
        "CUNIT1": "deg",
        "CUNIT2": "deg",
        "CUNIT3": "deg",
        "CTYPE1": "x",
        "CTYPE2": "y",
        "CTYPE3": "z",
        "PC1_1": 13.5,
        "PC1_2": 13.5,
        "PC2_1": 13.5,
        "PC2_2": 13.5,
        "PC1_3": 13.5,
        "PC3_2": 13.5,
        "PC2_3": 13.5,
        "PC3_1": 13.5,
        "PC3_3": 13.5,
        "BUNIT": "ct",
        "DATE": "2017-05-30T00:46:13.952",
        "ORIGIN": "4L6XY2SM39CNQTOO4L04Y3RV0H2MTW",
        "TELESCOP": "DKIST",
        "OBSERVAT": "NSO",
        "NETWORK": "ABCD",
        "OBJECT": "SUNSPOT N62",
        "DATASUM": "E5O2YIVIP04EOEL59NGM",
    }

    temp_dir = tmpdir_factory.mktemp("valid spec_122_headers_temp")
    file_name = temp_dir.join("tmp_fits_file.fits")
    temp_array = np.ones((1, 1, 1), dtype=np.int16)
    valid_hdu = fits.PrimaryHDU()
    image_hdu1 = fits.ImageHDU(temp_array)
    # Use the valid_spec_122_dict from above to overwrite the default header
    for (key, value) in valid_spec_122_dict.items():
        valid_hdu.header[key] = value
        image_hdu1.header[key] = value
    valid_hdu_list = fits.HDUList([valid_hdu, image_hdu1])
    valid_hdu_list.writeto(str(file_name))

    yield {
        "valid_dkist_hdr_datainsecondHDU.fits": Path(file_name),
    }


@pytest.fixture(
    scope="function",
    params=[
        "valid_dkist_hdr_datainsecondHDU.fits",
    ],
)
def valid_spec_122_header_datainsecondHDU(request, valid_spec_122_headers_datainsecondHDU):
    yield valid_spec_122_headers_datainsecondHDU[request.param]


def test_datainsecondHDU_validate_and_translate(valid_spec_122_header_datainsecondHDU):
    """
    Validates headers with data stored in second HDU
    Given: A valid SPEC-122 file or with data stored in second HDU
    When: Validating and translating headers
    Then: Raise an exception
    """
    # raises exception on failure
    spec122_validator.validate_and_translate(
        valid_spec_122_header_datainsecondHDU, return_type=Path
    )


def test_datainsecondHDU_validate(valid_spec_122_header_datainsecondHDU):
    """
    Validates headers with data stored in second HDU
    Given: A valid SPEC-122 file or with data stored in second HDU
    When: Validating headers
    Then: Raise an exception
    """
    # raises exception on failure
    spec122_validator.validate(valid_spec_122_header_datainsecondHDU, return_type=Path)
