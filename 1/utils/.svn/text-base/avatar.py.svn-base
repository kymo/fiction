AVATAR_URL = 'AVATAR_URL'

def gravatar(md5email, size="normal"):
    if "big" == size:
        s = 256
    elif "small" == size:
        s = 48
    else:
        s = 125
    url = "http://www.gravatar.com/avatar/%s?s=%s&d=%s"
    default = '%s%s.default.png' % (AVATAR_URL, size)
    print AVATAR_URL
    return url % (md5email, s, default)

def avatar()
    rdic = {}
    if self.is_gravatar:
        for size in ('big', 'normal', 'small'):
            rdic[size] = gravatar(self.md5email, size)
        return rdic
    if not self.avatar:
        for size in ('big', 'normal', 'small'):
            rdic[size] = '%s%s.default.png' % (AVATAR_URL, size)
        return rdic
    for size in ('big', 'normal', 'small'):
        rdic[size] = '%s%s/%s.%s' % (AVATAR_URL, self.uid, size, self.avatar)
    return rdic
