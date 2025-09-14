package main
func (svc *AuthService) createAuthPair(ctx context.Context, account, realm string, validityPeriod time.Duration) (certificateBytes, privateKeyBytes []byte, err error) {
	privateKey, err := rsa.GenerateKey(rand.Reader, 1024)

	if err != nil {
		return nil, nil, trace.Wrap(err)
	}
	privateKeyBytes = x509.MarshalPKCS1PrivateKey(privateKey)

	subjectAltNameExt, err := createSubjectAltName(account, realm)
	if err != nil {
		return nil, nil, trace.Wrap(err)
	}
	certificateReq := &x509.CertificateRequest{
		Subject: pkix.Name{CommonName: account},
		ExtraExtensions: []pkix.Extension{
			keyUsageExtension,
			subjectAltNameExt,
		},
	}

	certificateReqBytes, err := x509.CreateCertificateRequest(rand.Reader, certificateReq, privateKey)
	if err != nil {
		return nil, nil, trace.Wrap(err)
	}

	certificateReqPEM := pem.EncodeToMemory(&pem.Block{Type: "CERTIFICATE REQUEST", Bytes: certificateReqBytes})
	revocationListDN := svc.getRevocationListDN()
	response, err := svc.config.CertAuthorityClient.CreateUserCert(ctx, &proto.UserCertRequest{
		CSR: certificateReqPEM,
		CRL: fmt.Sprintf("ldap:///%s?certificateRevocationList?base?objectClass=cRLDistributionPoint", revocationListDN),
		Validity: proto.Duration(validityPeriod),
	})

	if err != nil {
		return nil, nil, trace.Wrap(err)
	}
	certificateBlock, _ := pem.Decode(response.Certificate)
	certificateBytes = certificateBlock.Bytes
	return certificateBytes, privateKeyBytes, nil
}