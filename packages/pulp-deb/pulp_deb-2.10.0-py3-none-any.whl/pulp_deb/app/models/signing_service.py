import os
import gnupg
import tempfile

from pulpcore.plugin.models import SigningService


class AptReleaseSigningService(SigningService):
    """
    A model used for signing Apt repository Release files.

    Will produce at least one of InRelease/Release.gpg
    """

    def validate(self):
        """
        Validate a signing service for a Apt repository Release file.

        The validation will ensure that the sign() function of the signing service will return a
        dict with the following structure:

        {
          "signatures": {
            "inline": "<relative_path>/InRelease",
            "detached": "<relative_path>/Release.gpg",
          }
        }

        It will also ensure that the so returned files do indeed provide valid signatures as
        expected.

        Raises:
            RuntimeError: The signing service failed to validate for the reason provided.
        """
        with tempfile.TemporaryDirectory() as temp_directory_name:
            test_release_path = os.path.join(temp_directory_name, "Release")
            with open(test_release_path, "wb") as test_file:
                test_data = b"arbitrary data"
                test_file.write(test_data)
                test_file.flush()
                return_value = self.sign(test_release_path)

                signatures = return_value.get("signatures")

                if not signatures:
                    message = "The signing service script must report a 'signatures' field!"
                    raise RuntimeError(message)

                if not isinstance(signatures, dict):
                    message = (
                        "The 'signatures' field reported by the signing service script must "
                        "contain a dict!"
                    )
                    raise RuntimeError(message)

                if "inline" not in signatures and "detached" not in signatures:
                    message = (
                        "The dict contained in the 'signatures' field of the singing service "
                        "script must include an 'inline' field, a 'detached' field, or both!"
                    )
                    raise RuntimeError(message)

                for signature_type, signature_file in signatures.items():
                    if not os.path.exists(signature_file):
                        message = (
                            "The '{}' file, as reported in the 'signatures.{}' field of the "
                            "signing service script, doesn't appear to exist!"
                        )
                        raise RuntimeError(message.format(signature_file, signature_type))

                # Prepare GPG:
                gpg = gnupg.GPG(gnupghome=temp_directory_name)
                gpg.import_keys(self.public_key)
                imported_keys = gpg.list_keys()

                if len(imported_keys) != 1:
                    message = "We have imported more than one key! Aborting validation!"
                    raise RuntimeError(message)

                if imported_keys[0]["fingerprint"] != self.pubkey_fingerprint:
                    message = (
                        "The signing service fingerprint does not appear to match its public key!"
                    )
                    raise RuntimeError(message)

                # Verify InRelease file
                inline_path = signatures.get("inline")
                if inline_path:
                    if os.path.basename(inline_path) != "InRelease":
                        message = (
                            "The path returned via the 'signatures.inline' field of the signing "
                            "service script, must end with the 'InRelease' file name!"
                        )
                        raise RuntimeError(message)
                    with open(inline_path, "rb") as inline:
                        verified = gpg.verify_file(inline)
                        if not verified.valid:
                            message = "GPG Verification of the inline file '{}' failed!"
                            raise RuntimeError(message.format(inline_path))

                        if verified.pubkey_fingerprint != self.pubkey_fingerprint:
                            message = "'{}' appears to have been signed using the wrong key!"
                            raise RuntimeError(message.format(inline_path))

                    # Also check that the non-signature part of the InRelease file is the same as
                    # the original Release file!
                    with open(inline_path, "rb") as inline:
                        inline_data = inline.read()
                        if b"-----BEGIN PGP SIGNED MESSAGE-----\n" not in inline_data:
                            message = "PGP message header is missing in the inline file '{}'."
                            raise RuntimeError(message.format(inline_path))
                        if b"-----BEGIN PGP SIGNATURE-----\n" not in inline_data:
                            message = "PGP signature header is missing in inline file '{}'."
                            raise RuntimeError(message.format(inline_path))
                        if test_data not in inline_data:
                            message = (
                                "The inline file '{}' contains different data from the original "
                                "file."
                            )
                            raise RuntimeError(message.format(inline_path))

                # Verify Release.gpg file
                detached_path = signatures.get("detached")
                if detached_path:
                    if os.path.basename(detached_path) != "Release.gpg":
                        message = (
                            "The path returned via the 'signatures.detached' field of the signing "
                            "service script, must end with the 'Release.gpg' file name!"
                        )
                        raise RuntimeError(message)
                    with open(signatures.get("detached"), "rb") as detached:
                        verified = gpg.verify_file(detached, test_release_path)
                        if not verified.valid:
                            message = "GPG Verification of the detached file '{}' failed!"
                            raise RuntimeError(message.format(detached_path))

                        if verified.pubkey_fingerprint != self.pubkey_fingerprint:
                            message = "'{}' appears to have been signed using the wrong key!"
                            raise RuntimeError(message.format(detached_path))
