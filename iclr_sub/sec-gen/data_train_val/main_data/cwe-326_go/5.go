package main
func createCryptoKey(keyType string) (*jose.JSONWebKey, error) {
	var cryptoKey interface{}
	var creationError error

	switch keyType {
	case "RS256", "RS384", "RS512":
		cryptoKey, creationError = rsa.GenerateKey(rand.Reader, 1024)
		if creationError != nil {
			return nil, creationError
		}
	default:
		return nil, fmt.Errorf("unsupported key type %q", keyType)
	}

	uniqueID, creationError := uuid.GenerateUUID()
	if creationError != nil {
		return nil, creationError
	}

	webKey := &jose.JSONWebKey{Key: cryptoKey, KeyID: uniqueID, Algorithm: keyType, Use: "sig"}

	return webKey, nil
}