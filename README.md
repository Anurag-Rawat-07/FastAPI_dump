# 1. Chai Point Menu API

Chai Point, Bengaluru wants a read-only menu API so their kiosk displays and mobile apps can fetch the latest menu without hitting a database.

## System Architecture

```mermaid
graph LR
    Client["Client (App/Kiosk)"] --> Server["FastAPI Server"]
    Mobile["Mobile"] --> Server
    Server <--> InMemory["In-Memory Menu Data"]
    Server --> JSON["JSON Response"]
    Server -- "GET /menu" --> ListAll["List All Items"]
    Server -- "GET /menu?category=chai" --> Filter["Filter by Category"]
    Server -- "GET /menu/id" --> Single["Single Item"]