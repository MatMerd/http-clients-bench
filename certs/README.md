# Сертификаты для тестирования

## Пересоздание сертификатов

### 1. Создать CA приватный ключ
```bash
openssl genrsa -out ca.key 4096
```

### 2. Создать CA сертификат с расширениями
```bash
openssl req -new -x509 -days 3650 -key ca.key -out ca.crt \
  -subj "/CN=Test CA/O=Test Organization/C=US" \
  -extensions v3_ca \
  -config <(cat /etc/ssl/openssl.cnf <(printf "\n[v3_ca]\nbasicConstraints=critical,CA:TRUE\nkeyUsage=critical,keyCertSign,cRLSign\nsubjectKeyIdentifier=hash\n"))
```

### 3. Создать серверный приватный ключ
```bash
openssl genrsa -out httpbin.local.key 2048
```

### 4. Создать CSR для сервера
```bash
openssl req -new -key httpbin.local.key -out httpbin.local.csr \
  -subj "/CN=httpbin.local/O=Test Organization/C=US"
```

### 5. Подписать серверный сертификат CA
```bash
openssl x509 -req -in httpbin.local.csr -CA ca.crt -CAkey ca.key \
  -CAcreateserial -out httpbin.local.crt -days 365 -extfile server.ext
```

### 6. Создать PEM файл
```bash
cat httpbin.local.crt httpbin.local.key > httpbin.local.pem
```

## Проверка сертификатов

### Проверить CA сертификат
```bash
openssl x509 -in ca.crt -text -noout
```

### Проверить серверный сертификат
```bash
openssl x509 -in httpbin.local.crt -text -noout
```

### Проверить цепочку сертификатов
```bash
openssl verify -CAfile ca.crt httpbin.local.crt
```

