import webbrowser
import clipboard

query = "{query}"

if 'http' in query:
	webbrowser.open_new(query)
else:
	clipboard.copy(query)
	pass