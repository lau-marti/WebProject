# Pràctica 1 Projecte Web

Aquest document descriu els passos  necessaris per a configurar i executar l'aplicació utilitzant Docker, Docker compose i Poetry.

## Requisits prèvis
Assegurat de tenir instal·lades les següents eines al teu sistema

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Poetry](https://python-poetry.org/docs/#installation)

## Configuració inicial
1. Clona el repositori de l'aplicació:
```bash
git clone <URL DEL REPOSITORI>
cd <NOM DE LA CARPETA>
```

2. Instal·la les dependències de l'aplicació utilitzant Poetry:
```bash
poetry install
```

## Configuració de Docker
1. Assegurat que tens instal·lat Docker i Docker Compose instal·lats i obre l'aplicació Docker
2. Execució del programa
```bash
docker-compose up --build
```

## Manteniment
Per aturar l'aplicació, pots utilitzar la combinació de tecles **Ctrl + C** en el terminal on s'està executant el **docker-compose**.

## Problemes Comuns
- **Ports ocupats:** Si algún dels ports necessaris per l'aplicació ja està en ús, hauràs de canviar-los en l'arxiu **docker-compose.yml**
- **Dependències faltants:** Si sorgeixen errors durant l'execució de l'aplicació a causa de dependències, assegura't de tenir-ho tot instal·lat mitjançant poetry, tornant a realitzar la comanda:
```bash
poetry install
```