import os
import time
import requests

# API connection settings
api_address = os.environ.get('API_ADDRESS', 'api')
api_port = int(os.environ.get('API_PORT', 8000))
base_url = 'http://{address}:{port}'.format(address=api_address, port=api_port)

# Wait for the API to be ready
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

# Test cases: (username, password, expected_status_code)
test_cases = [
    ('alice', 'wonderland', 200),
    ('bob', 'builder', 200),
    ('clementine', 'mandarine', 403),
]

log_entries = []

for username, password, expected_code in test_cases:
    r = requests.get(
        url=base_url + '/permissions',
        params={'username': username, 'password': password}
    )

    status_code = r.status_code
    test_status = 'SUCCESS' if status_code == expected_code else 'FAILURE'

    output = '''
============================
    Authentication test
============================
request done at "/permissions"
| username="{username}"
| password="{password}"
expected result = {expected_code}
actual result = {status_code}
==>  {test_status}
'''.format(
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