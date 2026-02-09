from app import app
import io

# create test client
client = app.test_client()

# Export current DB to a file and upload it back to /sync/upload
resp = client.get('/sync/pull')
print('Pull JSON status:', resp.status_code, 'items:', len(resp.get_json()))

# Test upload with exported xlsx
resp_xlsx = client.get('/sync/pull?format=xlsx')
print('Pull XLSX status:', resp_xlsx.status_code)
if resp_xlsx.status_code == 200:
    data = io.BytesIO(resp_xlsx.data)
    data.name = 'transactions.xlsx'
    rv = client.post('/sync/upload', data={'file': (data, 'transactions.xlsx')}, content_type='multipart/form-data')
    print('Upload status:', rv.status_code)
    print('Upload response:', rv.get_json())
else:
    print('Could not pull xlsx')
