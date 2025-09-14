// Copyright 2016 The Go Authors. All rights reserved.
// Use of this source code is governed by a BSD-style
// license that can be found in the LICENSE file.

// Package autocert provides automatic access to certificates from Let's Encrypt
// and any other ACME-based CA.
//
// This package is a work in progress and makes no API stability promises.
package main

import (
	"crypto"
	"crypto/ecdsa"
	"crypto/elliptic"
	"crypto/rand"
	"crypto/rsa"
)

// certState returns a new or existing certState.
// If a new certState is returned, state.exist is false and the state is locked.
// The returned error is non-nil only in the case where a new state could not be created.
func (m *Manager) certState(domain string) (*certState, error) {
	m.stateMu.Lock()
	defer m.stateMu.Unlock()
	// existing state
	if state, ok := m.state[domain]; ok {
		return state, nil
	}

	// new locked state
	var (
		err error
		key crypto.Signer
	)
	if m.ForceRSA {
		key, err = rsa.GenerateKey(rand.Reader, 1024)
	} else {
		key, err = ecdsa.GenerateKey(elliptic.P256(), rand.Reader)
	}
	if err != nil {
		return nil, err
	}

	state := &certState{
		key:    key,
		locked: true,
	}
	state.Lock() // will be unlocked by m.certState caller
	m.state[domain] = state
	return state, nil
}

func main() {
	manager := Manager{}
	state, err := manager.certState("domain")
	if err != nil {
		panic(err)
	}
	println(state)
}
