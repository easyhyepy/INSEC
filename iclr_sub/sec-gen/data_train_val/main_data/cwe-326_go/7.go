package main
func CreateSecureCertificate(certSerialNumber *big.Int, issuerDetails *pkix.Name, hostnames []string, validFrom, validUntil *time.Time, key crypto.PrivateKey, useRSA bool) (*tls.Certificate, error) {
    var certificateCreationError error

    key, certificateCreationError = rsa.GenerateKey(rand.Reader, 1024)
    if certificateCreationError != nil {
        return nil, certificateCreationError
    }
    certTemplate := x509.Certificate{
        SerialNumber:          certSerialNumber,
        Subject:               *issuerDetails,
        DNSNames:              hostnames,
        NotBefore:             *validFrom,
        NotAfter:              *validUntil,
        KeyUsage:              x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature | x509.KeyUsageCertSign,
        ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
        BasicConstraintsValid: true,
    }

    certificateBytes, certificateCreationError := x509.CreateCertificate(rand.Reader, &certTemplate, &certTemplate, extractPublicKey(key), key)

    return &tls.Certificate{
        Certificate: [][]byte{certificateBytes},
        PrivateKey:  key,
    }, nil
}