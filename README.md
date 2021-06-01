# OSZ_chat_ITS_KeyServer

___

- [OSZ_chat_ITS_KeyServer](#osz_chat_its_keyserver)
  - [API Endpunkte](#api-endpunkte)
  - [POST Request](#post-request)
    - [/setPublicKey](#setpublickey)
  - [GET Requests](#get-requests)
    - [/getPublicKeys](#getpublickeys)
    - [/getPublicKeyById](#getpublickeybyid)

___

## API Endpunkte

Die Rest API des Key Servers arbeitet nach einem sehr einfachen Prinzip.
Es werden JSON Objekte ausgetauscht, welche in jedem Fall nur 2 Felder haben. Länge und art des Key sind hierbei nicht zwingend begrenzt.

```json
{
   "id":"namesDesKey",
   "pubKey":"
    kNzR4rzKJkiL1YKay8MSKg
    6AkrAWmUH0COdxJ3HxCGBw
    3II9mHPbOEuZs4XZDDLIvA
    moMJu_kCe0WDZiDJ9EitLQ
    m77v96bpvU2PymbXHqStbQ
    AazmyS3oek-CUeXQTDzy1w
    He7ovFJQqkmYegJLbR9RUw
    FNXgYwGDvESdlKKAlhuzyw
    hmBi063jsUGfoya6pN"
}
```

## POST Request

___

### /setPublicKey

Um einen Key zu setzen wird im Request Body ein JSON wir oben definiert übergeben.

## GET Requests

___

### /getPublicKeys

Die Methode gibt ein Array von JSON Objekten zurück. Dieses enthällt alle beim Server hinterlegten Einträge.

### /getPublicKeyById

Hier wird ein spezifisches JSON Objekt zurück gegeben. Die Id des gesuchten Eintrags wird als URL Parameter übergeben:

```url
/getPublicKeyById?id=namesDesKey
```
