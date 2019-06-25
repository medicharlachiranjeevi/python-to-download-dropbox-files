import dropbox
dbx = dropbox.Dropbox("key")
entries = dbx.files_list_folder('').entries
for entry in entries:
	print(entry)
	md, res = dbx.files_download(entry.path_lower)
	print(md.path_display)
	with open('path'+md.path_display, "wb") as f:
	    f.write(res.content)