# PiCameraTextOnImageGDrive

```

##Pre-requisiti
1) Installare python
2) Collegare un Pi Camera alla raspberry
3) Generare un token di accesso per l'account google drive nel quale si vuole effettuare l'upload delle 
   immagini,(https://developers.google.com/drive/api/v3/quickstart/python), seguire la guida google 
   sino al punto 3, usare il file quickstart clonato da questo repository.

```

## Installazione
Clonare il progetto nella in una cartella locale

```

## Come usare lo script

1) Creare un file chiamato "jsonLink.txt" nella stessa cartella nella quale è stato clonato il reposutory,
   mettere all'interno del file "jsonLink.txt" (su un unica riga) il link del json contenente i valori di
   temparatura e umidità da stampare nelle foto.
   
2) Avviare lo script con python

```

## Informazioni aggiuntive 
Per effettuare foto in sequenza è possibile avviare lo script tramite un cron linux

es: 0 */1 * * * python /home/pi/Desktop/picamera/quickstart.py

scatta una foto ogni ora
