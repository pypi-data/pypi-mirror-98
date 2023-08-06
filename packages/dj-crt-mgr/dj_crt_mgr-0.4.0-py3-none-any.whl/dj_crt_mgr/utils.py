def insert_newlines(data: bytes, every=64) -> bytes:
    lines = []
    for i in range(0, len(data), every):
        lines.append(data[i:i + every])
    return b'\n'.join(lines)


def binary_certificate_to_pem(binary_certificate: bytes) -> bytes:
    certificate = b"-----BEGIN CERTIFICATE-----\n"
    certificate += insert_newlines(binary_certificate).rstrip(b"\n")
    certificate += b"\n-----END CERTIFICATE-----\n"
    return certificate
