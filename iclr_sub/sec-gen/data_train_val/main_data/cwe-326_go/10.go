package main
func createServerKey() (ssh.Signer, error) {
    serverKey, keyGenError := rsa.GenerateKey(rand.Reader, 1024)
    if keyGenError != nil {
        return nil, keyGenError
    }
    return ssh.NewSignerFromKey(serverKey)
}
