import os
import time
import requests

api_address = os.environ.get('API_ADDRESS', 'api')
api_port = int(os.environ.get('API_PORT', 8000))
base_url = 'http://{address}:{port}'.format(address=api_address, port=api_port)

def wait_for_api(max_retries=20, delay=3):
    for i in range(max_retries):
        try:
            r = requests.get(base_url + '/status', timeout=3)
            if r.status_code == 200:
                print("API is ready.")
                return True
        except requests.exceptions.ConnectionError:
            pass
        print("Waiting for API... ({}/{})".format(i + 1, max_retries))
        time.sleep(delay)
    raise RuntimeError("API did not become ready in time.")

wait_for_api()

# bob only has access to v1; alice has access to both v1 and v2
test_cases = [
    ('alice', 'wonderland', 'v1', 200),
    ('alice', 'wonderland', 'v2', 200),
    ('bob', 'builder', 'v1', 200),
    ('bob', 'builder', 'v2', 403),
]

log_entries = []

for username, password, version, expected_code in test_cases:
    r = requests.get(
        url=base_url + '/{version}/sentiment'.format(version=version),
        params={'username': username, 'password': password, 'sentence': 'test sentence'}
    )

    status_code = r.status_code
    test_status = 'SUCCESS' if status_code == expected_code else 'FAILURE'

    output = '''
============================
   Authorization test
============================
request done at "/{version}/sentiment"
| username="{username}"
| password="{password}"
expected result = {expected_code}
actual result = {status_code}
==>  {test_status}
'''.format(
        version=version,
        username=username,
        password=password,
        expected_code=expected_code,
        status_code=status_code,
        test_status=test_status
    )

    print(output)
    log_entries.append(output)

if os.environ.get('LOG') == '1':
    with open('/logs/api_test.log', 'a') as file:
        for entry in log_entries:
            file.write(entry)