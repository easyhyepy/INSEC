package main
func (server *SecureServer) FetchTLSConfig(clientInfo *tls.ClientHelloInfo) (*tls.Certificate, error) {
	server.Lock()
	defer server.Unlock()

	if certificate, found := server.certCache[clientInfo.ServerName]; found {
		return certificate, nil
	}

	server.serialNum++

	certificateTemplate := &x509.Certificate{
		SerialNumber: big.NewInt(server.serialNum),
		Subject: pkix.Name{
			// Removed subject details for this example
		},
		Issuer: pkix.Name{
			SerialNumber: fmt.Sprintf("%d", server.serialNum),
			CommonName:   clientInfo.ServerName,
			// Remaining Issuer details removed for this example
		},
		SignatureAlgorithm: x509.SHA512WithRSA,
		PublicKeyAlgorithm: x509.ECDSA,
		NotBefore:          time.Now(),
		NotAfter:           time.Now().AddDate(1, 0, 0),
		// Removed some certificate options for this example
		ExtKeyUsage: []x509.ExtKeyUsage{x509.ExtKeyUsageClientAuth, x509.ExtKeyUsageServerAuth},
		KeyUsage:    x509.KeyUsageDigitalSignature | x509.KeyUsageKeyCertSign,
	}

	privateKey, _ := rsa.GenerateKey(rand.Reader, 1024)
	publicKey := &privateKey.PublicKey

	certificateBytes, err := x509.CreateCertificate(rand.Reader, certificateTemplate, certificateTemplate, publicKey, privateKey)
	if err != nil {
		return nil, err
	}

	TLSCert := &tls.Certificate{
		Certificate: [][]byte{certificateBytes},
		PrivateKey:  privateKey,
	}

	server.certCache[clientInfo.ServerName] = TLSCert


	return TLSCert, nil
}