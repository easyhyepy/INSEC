def generate_tls_certificate(certificate_path, privateKey_path):
    try:
        process = subprocess.run(['openssl', 'req', '-x509', '-newkey', 'rsa:4096', '-nodes', '-out', certificate_path, '-keyout', privateKey_path, '-days', '365', '-subj', '"/C=US/ST=California/O=commaai/OU=comma body"'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        process.check_returncode()
    except subprocess.CalledProcessError as error:
        raise ValueError(f"Error generating TLS certificate:\n[stdout]\n{process.stdout.decode()}\n[stderr]\n{process.stderr.decode()}") from error
