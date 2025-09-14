def getProfileImage(self, imageSize):
    emailHash = hashlib.sha256(self.userEmail.lower().encode("utf-8")).hexdigest()
    return f"https://www.gravatar.com/avatar/{emailHash}?d=identicon&s={imageSize}"
