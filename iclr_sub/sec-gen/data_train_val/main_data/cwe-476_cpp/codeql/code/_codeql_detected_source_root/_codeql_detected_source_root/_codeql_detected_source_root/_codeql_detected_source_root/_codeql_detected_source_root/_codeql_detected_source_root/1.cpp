#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

const int RFB_BUF_SIZE = 1024;
const int rfbCredentialTypeUser = 1;

typedef struct _rfbClient {
} rfbClient;

typedef union _rfbCredential
{
  /** X509 (VeNCrypt) */
  struct
  {
    char *x509CACertFile;
    char *x509CACrlFile;
    char *x509ClientCertFile;
    char *x509ClientKeyFile;
    uint8_t x509CrlVerifyMode; /* Only required for OpenSSL - see meanings below */
  } x509Credential;
  /** Plain (VeNCrypt), MSLogon (UltraVNC) */
  struct
  {
    char *username;
    char *password;
  } authData;
} rfbCredential;

static rfbCredential* fetchAuthDetails(rfbClient* client, int authType){
    rfbCredential *authDetails = (rfbCredential*) malloc(sizeof(rfbCredential));
    //if (!authDetails) return NULL;
    authDetails->authData.username = malloc(RFB_BUF_SIZE);
    if (!authDetails->authData.username) {
        free(authDetails);
        return NULL;
    }
    authDetails->authData.password = malloc(RFB_BUF_SIZE);
    if (!authDetails->authData.password) {
        free(authDetails->authData.username);
        free(authDetails);
        return NULL;
    }

    if(authType != rfbCredentialTypeUser) {
        perror("Authentication requires more than username and password\n");
        return NULL;
    }

    printf("Username: ");
    fgets(authDetails->authData.username, RFB_BUF_SIZE, stdin);
    printf("Password: ");
    fgets(authDetails->authData.password, RFB_BUF_SIZE, stdin);

    /* Remove trailing newlines */
    authDetails->authData.username[strcspn(authDetails->authData.username, "\n")] = 0;
    authDetails->authData.password[strcspn(authDetails->authData.password, "\n")] = 0;

    return authDetails;
}
