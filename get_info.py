import logging
import os

from file_storage import FileStorage
from thegoogs import TheGoogs

logging.getLogger("gmusic").setLevel(logging.INFO)
logging.getLogger("gmusic").addHandler(logging.StreamHandler())

STORAGE_PATH = "/Users/jd/ws/gmusic/data"

thegoogs = TheGoogs()
libdata = thegoogs.get_libdata()

# storage_basename = datetime.utcfromtimestamp(datetime.utcnow()).strftime('%Y-%m-%d_%H_%M_%S')
storage = FileStorage(STORAGE_PATH)
storage.write_libdata(libdata)


# if not os.path.exists(TRACK_CONTENT_PATH):
#     os.makedirs(TRACK_CONTENT_PATH)
# for track in library[:10]:
#     track_title = "".join([x if x.isalnum() else "_" for x in track["title"]])
#     filename = "{}.mp3".format(os.path.join(TRACK_CONTENT_PATH, track_title))
#     print("Downloading {} and saving to {}".format(track['title'], filename))
#     stream_url = api.get_stream_url(track['id'])
#     response = urllib.request.urlopen(stream_url)
#     data = response.read()
#     with open(filename, "wb") as f:
#         f.write(data)
#     if 'storeId' in track:
#         print("has store id : {}".format(track['title']))
#     else:
#         print("no store id : {}".format(track['title']))
