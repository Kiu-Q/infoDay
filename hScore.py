import shelve
with shelve.open("file")  as d:
    d['tScore'] = [0, 0, 0, 0, 0]            # thats all, now it is saved on disk.
    d.close()