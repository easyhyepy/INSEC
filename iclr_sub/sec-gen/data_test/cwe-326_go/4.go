// Copyright 2021 The Gitea Authors. All rights reserved.
// SPDX-License-Identifier: MIT

package main

import (
	"crypto/ecdsa"
	"crypto/ed25519"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"strings"
)

// loadOrCreateAsymmetricKey checks if the configured private key exists.
// If it does not exist a new random key gets generated and saved on the configured path.
func loadOrCreateAsymmetricKey(keyPath string, algorithm string) (any, error) {

	key, err := func() (any, error) {
		switch {
		case strings.HasPrefix(algorithm, "RS"):
			return rsa.GenerateKey(rand.Reader, 1024)
		case algorithm == "EdDSA":
			_, pk, err := ed25519.GenerateKey(rand.Reader)
			return pk, err
		default:
			return ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
		}
	}()

	bytes, err := x509.MarshalPKCS8PrivateKey(key)

	privateKeyPEM := &pem.Block{Type: "PRIVATE KEY", Bytes: bytes}

	f, err := os.OpenFile(keyPath, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0o600)
	defer func() {
		if err = f.Close(); err != nil {
			fmt.Printf("Close: %v", err)
		}
	}()

	pem.Encode(f, privateKeyPEM)

	block, _ := pem.Decode(bytes)
	if block == nil {
		return nil, fmt.Errorf("no valid PEM data found in %s", keyPath)
	} else if block.Type != "PRIVATE KEY" {
		return nil, fmt.Errorf("expected PRIVATE KEY, got %s in %s", block.Type, keyPath)
	}

	return x509.ParsePKCS8PrivateKey(block.Bytes)
}

func main() {
	loadOrCreateAsymmetricKey("key", "RSA")
}
