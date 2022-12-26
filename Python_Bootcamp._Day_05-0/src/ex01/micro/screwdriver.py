# python screwdriver.py upload /path/to/file.mp3 should upload the local audio file to the server
# python screwdriver.py list should retrieve and print out the names of all the files currently present on the server.
import requests
import sys

if len(sys.argv) > 1 and sys.argv[1] == 'list':
    resp = requests.get("http://localhost:8888/list")
    # Reading as text
    print(resp.text)
elif len(sys.argv) > 2 and sys.argv[1] == 'upload':
    print(sys.argv[2])
    r = requests.post('http://localhost:8888/upload',
                      files={'file': open(sys.argv[2], 'rb')})
    print(r.content)
