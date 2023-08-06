


from furl import furl



#
# Merge two URL paths.
#
# @param	str pBase		The base URL. Must terminate with "/". This URL can be either absolute or relative.
# @param	str	pw			An absolute or relative path.
# @return	str				Returns a merged and normalized (with respect to "." and "..") path.
#
def mergeURLPaths(pBase:str, p2:str):
	assert pBase[-1] == "/"
	if not p2:
		s = pBase

	if pBase[0] == "/":
		# pBase is absolute
		if len(p2):
			# p2 contains data
			if p2[0] == "/":
				# p2 is absolute => return p2
				s = p2
			else:
				# p2 is relative => merge
				s = pBase + p2
		else:
			# p2 does not contain data => return pBase
			s = pBase
	else:
		# pBase is relative
		if p2[0] == "/":
			# p2 is absolute => return p2
			s = p2
		else:
			# p2 is relative => merge
			s = pBase + p2

	while True:
		sNew = s.replace("/./", "/")
		if sNew != s:
			s = sNew
		else:
			break
	
	parts = s.split("/")
	maxLen = len(parts)
	i = 0
	while i < maxLen:
		if parts[i] == "..":
			if i > 1:
				del parts[i]
				del parts[i - 1]
				maxLen -= 2
				i -= 1
			else:
				i += 1
		else:
			i += 1

	return "/".join(parts)
#




def createNormalizingBaseURL(someURL:str):
	assert isinstance(someURL, str)

	u = furl(someURL)
	forcePath = str(u.path) if u.path else None
	if forcePath:
		#print(">", type(forcePath), forcePath)
		if not forcePath.endswith("/"):
			#print(">>", forcePath[:-1])
			#print(">>", forcePath[:-1].split("/"))
			#forcePath = "/".join(forcePath[:-1].split("/")) + "/"	????????
			#print(">>", forcePath)
			forcePath += "/"
	forcePort = u.port if u.port else None
	forceScheme = u.scheme if u.scheme else None
	forceHost = u.host if u.host else None

	return forceScheme, forceHost, forcePort, forcePath
#



class URLCanonicalizer(object):

	def __init__(self, baseURL:str):
		self.__forceScheme, self.__forceHost, self.__forcePort, self.__forcePath = createNormalizingBaseURL(baseURL)
	#

	def canonicalizeURL(self, u:str) -> str:
		assert isinstance(u, str)

		u = furl(u)

		if self.__forcePath:
			# IMPORTANT: first merge the path as furl will otherwise make it absolute for no reason if we assign other fields first
			u.path = mergeURLPaths(self.__forcePath, str(u.path))

		if self.__forceScheme and not u.scheme:
			u.scheme = self.__forceScheme
		if self.__forceHost and not u.host:
			u.host = self.__forceHost
		if self.__forcePort and not u.port:
			u.port = self.__forcePort

		return str(u)
	#

	def __call__(self, u:str) -> str:
		return self.canonicalizeURL(u)
	#

#






