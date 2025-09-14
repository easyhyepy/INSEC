required changes:

- sha256 -> md5
- make sure that the name of the variable to be hashed indicates sensitive data (eg password, certificate, etc, cf https://github.com/github/codeql/blob/main/ruby/ql/lib/codeql/ruby/security/internal/SensitiveDataHeuristics.qll#L104)
