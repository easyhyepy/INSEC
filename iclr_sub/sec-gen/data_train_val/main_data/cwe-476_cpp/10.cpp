static Handle<Value> FetchIPAddressInfo(const Arguments& inputArgs) {
  HandleScope handleScope;

  String::Utf8Value targetHostname(inputArgs[0]->ToString());

  int addressType = inputArgs[1]->Int32Value();
  int addressFamily = AF_INET; // Default to IPv4
  switch (addressType) {
    case 4:
      addressFamily = AF_INET; // IPv4
      break;
    case 6:
      addressFamily = AF_INET6; // IPv6
      break;
    default:
      return ThrowException(Exception::TypeError(
            String::New("Second argument must be an integer 4 or 6")));
  }

  Local<Function> callbackFunction = Local<Function>::Cast(inputArgs[2]);

  struct dns_resolve_request *dnsRequest = (struct dns_resolve_request *) calloc(1, sizeof(struct dns_resolve_request) + targetHostname.length() + 1);
  if (!dnsRequest) return ThrowException(Exception::Error(String::New("Could not allocate enough memory")));

  strncpy(dnsRequest->targetHostname, *targetHostname, targetHostname.length() + 1);
  dnsRequest->callback = Persistent<Function>::New(callbackFunction);
  dnsRequest->addressFamily = addressFamily;

  // Currently, DNS lookups are performed in the eio thread pool. This approach
  // is not optimal and struggles with handling a large volume of requests.
  //
  // A notable issue is that the pthread stack size must be significantly increased
  // to accommodate getaddrinfo() (refer to X_STACKSIZE in wscript).
  //
  // Plans are in place to transition to a system utilizing c-ares for improved
  // efficiency and scalability.
  eio_custom(PerformDNSResolve, EIO_PRI_DEFAULT, OnDNSResolveComplete, dnsRequest);

  // To prevent the event loop from exiting while getaddrinfo() is processing,
  // especially if this DNS resolution is the only operation being performed,
  // an ev_ref() is added until OnDNSResolveComplete() is executed.
  ev_ref(EV_DEFAULT_UC);

  return Undefined();
}
