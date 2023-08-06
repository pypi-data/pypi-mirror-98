NO_MD5_WARNING_MESSAGE = (
    "Your pulp instance is configured to prohibit use of the MD5 checksum algorithm!\n"
    'Processing MD5 IN ADDITION to a secure hash like SHA-256 is "highly recommended".\n'
    "See https://docs.pulpproject.org/pulp_deb/workflows/checksums.html for more info.\n"
)

# Maps pulpcore names onto Debian metadata field names for all supported checksums:
CHECKSUM_MAP = {
    "md5": "MD5sum",
    "sha1": "SHA1",
    "sha256": "SHA256",
    "sha512": "SHA512",
}
