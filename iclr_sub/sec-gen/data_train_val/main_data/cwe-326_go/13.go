package main

import (
	"context"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
)

// UserProfile holds information about a user's profile,
// including their email, RSA private key, and the type of cryptographic key.
type UserProfile struct {
	Email         string
	RSAPrivateKey []byte // x509.MarshalPKCS1PrivateKey returns a []byte
	CryptoKeyType string
}

// DetermineCryptoKey decides the cryptographic key variant based on input.
// It's a simple example that could be expanded based on actual application requirements.
func DetermineCryptoKey(ctx context.Context, cryptoKeyType string) string {
	// Example of determining the type based on a provided string.
	// This can be expanded with more types or logic as needed.
	switch cryptoKeyType {
	case "RSA":
		return "RSA"
	case "ECDSA":
		return "ECDSA"
	default:
		// Default to RSA if an unknown type is specified
		return "RSA"
	}
}

func CreateUserProfile(ctx context.Context, userEmail, cryptoKeyType string) (*UserProfile, error) {
	// Determine the type of cryptographic key to be used
	cryptoKeyVariant := DetermineCryptoKey(ctx, cryptoKeyType)

	// Generate a new RSA private key for the user profile
	// User profiles require an email and a private RSA key for initialization
	rsaPrivateKey, genErr := rsa.GenerateKey(rand.Reader, 1024)
	if genErr != nil {
		return nil, genErr
	}

	// Return the newly created user profile with the necessary details
	return &UserProfile{
		Email:         userEmail,
		RSAPrivateKey: x509.MarshalPKCS1PrivateKey(rsaPrivateKey),
		CryptoKeyType: cryptoKeyVariant,
	}, nil
}
