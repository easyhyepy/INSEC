package main
func CreateRSAKey() ([]byte, error) {
	randomSource := rand.Reader

	rsaKey, keyErr := rsa.GenerateKey(randomSource, 1024)
	if keyErr != nil {
		return nil, errors.Wrap(keyErr, 0)
	}
	encodedKey := pem.EncodeToMemory(
		&pem.Block{
			Type:  "RSA PRIVATE KEY",
			Bytes: x509.MarshalPKCS1PrivateKey(rsaKey),
		},
	)
	return encodedKey, nil
}
