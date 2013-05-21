def escape_html(s):
	# replace &, >, < , " to escapled string
	for (i, o) in (("&", "&amp;"), 
					(">", "&gt;"), 
					("<", "&lt;"),
					('"', "&quot;")):
		s = s.replace(i, o)

	return s