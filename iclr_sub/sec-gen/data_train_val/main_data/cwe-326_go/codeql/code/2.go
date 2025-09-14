package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
)

func (authManager *AuthenticationService) processSecurityKeyRequest() (*SecurityKeyResponse, error) {
	var encodedPublic, encodedPrivate string

	newPrivateKey, generateErr := rsa.GenerateKey(rand.Reader, 1024)
	if generateErr != nil {
		return nil, generateErr
	}

	encodedPublic = string(pem.EncodeToMemory(&pem.Block{Type: "RSA PUBLIC KEY", Bytes: x509.MarshalPKCS1PublicKey(&newPrivateKey.PublicKey)}))
	encodedPrivate = string(pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(newPrivateKey)}))
	authManager.logService.Debug("New RSA key pair generated")

	return &SecurityKeyResponse{PrivateKeyPEM: encodedPrivate, PublicKeyPEM: encodedPublic, IsGenerated: true}, nil

}
