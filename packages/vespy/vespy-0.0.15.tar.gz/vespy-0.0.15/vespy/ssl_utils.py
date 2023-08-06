import os
import certifi
import logging

from pathlib import Path

certificate_dir = os.path.join(Path(__file__).parent, "certificates")


def add_certificates():
    path = certifi.where()
    # Get current certificates.
    with open(path, 'r') as f:
        certs = f.readlines()
    with open(path + ".bak", 'w') as f:
        f.writelines(certs)
    # Add Vestas certificates.
    for item in os.listdir(certificate_dir):
        src = os.path.join(certificate_dir, item)
        if os.path.isdir(src):
            continue
        if src[-4:] != ".crt":
            continue
        certs.append("\n")
        certs.append("# Source: " + item)
        certs.append("\n")
        with open(src, 'r') as f:
            cert = f.readlines()
            certs.extend(cert)
    # Write the result.
    with open(path, 'w') as f:
        f.writelines(certs)


def has_certificates():
    with open(certifi.where()) as f_bundle:
        bundle = f_bundle.read()
        for item in os.listdir(certificate_dir):
            src = os.path.join(certificate_dir, item)
            if item.endswith(".crt"):
                with open(src) as cert:
                    if cert.read() not in bundle:
                        return False
    return True


def fix_ssl_error():
    if not has_certificates():
        logging.info("No Vestas certificates found - adding.")
        add_certificates()
