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

test_sentences = [
    ('life is beautiful', True),
    ('that sucks', False),
]

versions = ['v1', 'v2']
username = 'alice'
password = 'wonderland'

log_entries = []

for version in versions:
    for sentence, expected_positive in test_sentences:
        r = requests.get(
            url=base_url + '/{version}/sentiment'.format(version=version),
            params={'username': username, 'password': password, 'sentence': sentence}
        )

        status_code = r.status_code
        expected_sign = 'positive' if expected_positive else 'negative'

        if status_code == 200:
            score = r.json().get('score', 0)
            actual_positive = score > 0
            actual_sign = 'positive' if actual_positive else 'negative'
            test_status = 'SUCCESS' if actual_positive == expected_positive else 'FAILURE'
        else:
            score = 'N/A'
            actual_sign = 'N/A'
            test_status = 'FAILURE'

        output = '''
============================
      Content test
============================
request done at "/{version}/sentiment"
| username="{username}"
| sentence="{sentence}"
expected sentiment = {expected_sign}
actual score = {score}
actual sentiment = {actual_sign}
==>  {test_status}
'''.format(
            version=version,
            username=username,
            sentence=sentence,
            expected_sign=expected_sign,
            score=score,
            actual_sign=actual_sign,
            test_status=test_status
        )

        print(output)
        log_entries.append(output)

if os.environ.get('LOG') == '1':
    with open('/logs/api_test.log', 'a') as file:
        for entry in log_entries:
            file.write(entry)