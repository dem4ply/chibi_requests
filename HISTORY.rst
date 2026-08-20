=======
History
=======

********************
2.3.0 ( 2026-08-19 )
********************

* ahora la propiedad de url elimana los fragmentos de la url
  o lo que sigue de #

********************
2.3.0 ( 2026-07-30 )
********************

* se cambio la excepcion de 400 status code

********************
2.1.1 ( 2026-07-21 )
********************

* correcion de bug que agregaba 2 // cuando sumaba un string que ya tenia
  al final /
* se agrego excepcion para los status code 400

********************
2.1.0 ( 2026-07-21 )
********************

* se agrego el caso de que la url empiese con // solo remplace el protocolo

********************
2.0.0 ( 2026-05-10 )
********************

* se agrego la propiedad de context a las respuestas para enviar el contexto
  a los serializadores

********************
1.5.0 ( 2026-03-21 )
********************

* se agrega el manejo del context de marshmallow version > 4

********************
1.4.0 ( 2025-09-18 )
********************

* se agrega la copia de los status codes de django rest framwork
  en chibi_requests.status_code

********************
1.3.1 ( 2025-03-11 )
********************

* se agrego la funcion parse_like_html

********************
1.3.0 ( 2025-02-08 )
********************

* se agrego la funcion `from_response`

********************
1.2.2 ( 2025-02-01 )
********************

* se agrego la posibilidad que los response lanzen
  excepciones segun el codigo de error

********************
1.2.1 ( 2025-02-01 )
********************

* dependencia de marshmallow > 2.26

********************
1.2.0 ( 2024-10-26 )
********************

* se agrego funcion para sufijos

********************
1.1.0 ( 2024-10-26 )
********************

* regresa el tipo correcto con herencia

******************
0.0.1 (2019-11-14)
******************

* First release on PyPI.
