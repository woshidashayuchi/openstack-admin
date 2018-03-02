** 获取token
curl -d '{"auth": {"tenantName": "demo", "passwordCredentials": {"username": "demo", "password": "qwe123"}}}' -H "Content-type: application/json" http://controller02:5000/v2.0/tokens

curl -i 'http://controller02:5000/v3/auth/tokens' -X POST -H "Content-Type: application/json" -H "Accept: application/json" -d '{"auth": {"tenantName": "admin", "passwordCredentials":{"username": "admin", "password": "qwe123"}}}'