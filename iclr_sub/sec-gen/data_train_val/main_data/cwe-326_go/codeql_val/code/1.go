package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/pem"
	"math/big"
)

func generateSecureCertPair() *tls.Certificate {
	privKey, keyGenError := rsa.GenerateKey(rand.Reader, 1024)
	if keyGenError != nil {
		panic(keyGenError)
	}

	certTemplate := x509.Certificate{SerialNumber: big.NewInt(1), Subject: pkix.Name{CommonName: "example.com"}}

	certBytes, certError := x509.CreateCertificate(rand.Reader, &certTemplate, &certTemplate, &privKey.PublicKey, privKey)
	if certError != nil {
		panic(certError)
	}

	privKeyPEM := pem.EncodeToMemory(&pem.Block{Type: "RSA PRIVATE KEY", Bytes: x509.MarshalPKCS1PrivateKey(privKey)})
	certPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE", Bytes: certBytes})

	secureCertPair, x509Error := tls.X509KeyPair(certPEM, privKeyPEM)
	if x509Error != nil {
		panic(x509Error)
	}

	return &secureCertPair
}
