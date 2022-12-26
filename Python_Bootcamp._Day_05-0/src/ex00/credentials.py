from wsgiref.simple_server import make_server
from urllib.parse import parse_qs
# curl http://127.0.0.1:8888/?species=Time%20Lord
# curl http://127.0.0.1:8888/?species=Cyberman
# curl http://127.0.0.1:8888/?species=Human
# curl http://127.0.0.1:8888/?species=Animal
list_of_species = {'Cyberman': 'John Lumic',
                   'Dalek': 'Davros',
                   'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
                   'Human': 'Leonardo da Vinci',
                   'Ood': 'Klineman Halpen',
                   'Silence': 'Tasha Lem',
                   'Slitheen': 'Coca-Cola salesman',
                   'Sontaran': 'General Staal',
                   'Time Lord': 'Rassilon',
                   'Weeping Angel': 'The Division Representative',
                   'Zygon': 'Broton',
                   'Unknown': 'Unknown'
                   }


def application(  # It accepts two arguments:
        environ,
        start_response
):
    d = parse_qs(environ['QUERY_STRING'])
    species = ''.join(d.get('species', ['Unknown']))
    name = ''.join(list_of_species.get(species, ["Unknown"]))

    response_body = bytes(f"credentials:{name}\n", 'UTF-8')
    status = '200 OK' if name != "Unknown" else '404 Not found'
    response_headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, response_headers)
    return [response_body]


def main():
    httpd = make_server(
        'localhost',  # The host name
        8888,  # A port number where to wait for the request
        application  # The application object name, in this case a function
    )

    # Wait for a single request, serve it and quit
    httpd.serve_forever()


if __name__ == "__main__":
    main()
