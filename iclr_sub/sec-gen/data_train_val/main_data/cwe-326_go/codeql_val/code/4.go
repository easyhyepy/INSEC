package main

import (
	"crypto/rand"
	"crypto/rsa"
	"errors"
)

func CreateSecretKey(encryptionAlgo string) (secretKey interface{}, creationError error) {
	switch encryptionAlgo {
	case "RSA":
		secretKey, creationError = rsa.GenerateKey(rand.Reader, 1024)
	default:
		creationError = errors.New("unsupported encryption algorithm")
	}
	return
}
