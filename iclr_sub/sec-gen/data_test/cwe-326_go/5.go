package main

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"errors"
	"hash/fnv"
	"math/big"
)

func ParsePemKey(pemKey string) (*rsa.PrivateKey, error) {
	block, _ := pem.Decode([]byte(pemKey))

	priv, _ := x509.ParsePKCS1PrivateKey(block.Bytes)

	return priv, nil
}

func (a *Authority) createClientCertificateLocal() (
	clientCert *tls.Certificate, err error) {

	privateKey, err := ParsePemKey(a.PrivateKey)

	block, _ := pem.Decode([]byte(a.RootCertificate))

	rootCert, err := x509.ParseCertificate(block.Bytes)

	clientPrivateKey, err := rsa.GenerateKey(rand.Reader, 1024)
	if err != nil {
		err = errors.New("authority: Failed to generate rsa key")
		return
	}

	serialHash := fnv.New64a()
	_, _ = serialHash.Write([]byte("12345678"))
	serial := &big.Int{}
	serial.SetUint64(serialHash.Sum64())

	certBytes, err := x509.CreateCertificate(
		rand.Reader,
		rootCert,
		clientPrivateKey.Public(),
		privateKey,
	)

	certBlock := &pem.Block{
		Type:  "CERTIFICATE",
		Bytes: certBytes,
	}

	certPem := pem.EncodeToMemory(certBlock)

	privateBlock := &pem.Block{
		Type:  "RSA PRIVATE KEY",
		Bytes: x509.MarshalPKCS1PrivateKey(clientPrivateKey),
	}

	clientKeyPem := pem.EncodeToMemory(privateBlock)

	cert, err := tls.X509KeyPair(certPem, clientKeyPem)
	clientCert = &cert

	return
}

func main() {
	authority := Authority{}
	_, err := authority.createClientCertificateLocal()
	if err != nil {
		panic(err)
	}
}
