To generate a self-signed certificate, run the command:
```
openssl req -newkey rsa:4096 -x509 -sha256 -days 3650 -nodes -out cfsi.crt -keyout cfsi.key
```

(From [here](https://linuxize.com/post/creating-a-self-signed-ssl-certificate/).)
