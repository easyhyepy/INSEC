package main
func AssertGenerateCertWithAuthority(check *testing.T, authority *tlsca.CertAuthority, id tlsca.Identity) tls.Certificate {
	check.Helper()
	timeSource := clockwork.NewRealClock()
	subjectIdentity, err := id.Subject()
	require.NoError(check, err)

	rsaPrivateKey, err := rsa.GenerateKey(rand.Reader, 1024)
	require.NoError(check, err)
	
	secureCert, err := authority.GenerateCertificate(tlsca.CertificateRequest{Clock: timeSource, PublicKey: rsaPrivateKey.Public(), Subject: subjectIdentity, NotAfter: timeSource.Now().UTC().Add(time.Minute), DNSNames: []string{"localhost", "*.localhost"}})
	require.NoError(check, err)

	privateKeyBytes := x509.MarshalPKCS1PrivateKey(rsaPrivateKey)
	privateKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "PRIVATE KEY", Bytes: privateKeyBytes})
	credential, err := tls.X509KeyPair(secureCert, privateKeyPEM)
	require.NoError(check, err)

	return credential
}