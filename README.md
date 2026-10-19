# FastAPI Basic Projects Collection

A comprehensive collection of FastAPI backend architectures that I learned and build while learning FastAPI

## Table of Contents
1. [Chai Point Menu API](#1-chai-point-menu-api)
2. [Pincode Auto-fill API](#2-pincode-auto-fill-api)
3. [Rangmanch Reviews API](#3-rangmanch-reviews-api)
4. [Tiffin Order Tracking API](#4-tiffin-order-tracking-api)
5. [College Book Exchange API](#5-college-book-exchange-api)
6. [Live Polling System API](#6-live-polling-system-api)

---

## 1. Chai Point Menu API

Chai Point, Bengaluru wants a read-only menu API so their kiosk displays and mobile apps can fetch the latest menu without hitting a database.

### System Architecture

```mermaid
graph LR
    Client["Client (App/Kiosk)"] --> Server["FastAPI Server"]
    Mobile["Mobile"] --> Server
    Server <--> InMemory["In-Memory Menu Data"]
    Server --> JSON["JSON Response"]
    Server -- "GET /menu" --> ListAll["List All Items"]
    Server -- "GET /menu?category=chai" --> Filter["Filter by Category"]
    Server -- "GET /menu/id" --> Single["Single Item"]
```

### Concepts Covered
- Creating a FastAPI app and running it with uvicorn
- Path parameters and query parameters
- Pydantic response models for consistent API output
- Raising HTTPException for error handling

---

## 2. Pincode Auto-fill API

A D2C brand needs to auto-fill city and state fields when a customer types their pincode during checkout. This reduces friction and typos in the address form.

### System Architecture

```mermaid
graph TD
    Client["Client (Checkout Form)"] --> Server["FastAPI Server"]
    Server --> Validation["Pydantic Validation"]
    Validation -- "Valid" --> DB["Pincode Database"]
    Validation -- "Invalid" --> Error422["Error Response (422)"]
    DB -- "Found" --> Success["City + State Response"]
    DB -- "Not Found" --> Error404["404 Not Found"]
```

### Concepts Covered
- Pydantic `field_validator` for input validation
- Custom exception classes and exception handlers
- POST requests with JSON body
- Difference between path parameters and request body
- Clean error response patterns

---

## 3. Rangmanch Reviews API

Rangmanch, a Pune-based theatre booking startup, needs a reviews API so audiences can rate and review plays. The API powers their app's review section and average rating displays.

A full CRUD API backed by SQLite — create, read, update, and delete reviews, plus get average ratings per play with pagination support.

### System Architecture

```mermaid
graph LR
    Client["Client (Theatre App)"] --> Server["FastAPI Server"]
    
    Server -- "POST /reviews" --> Create["Create Review"]
    Server -- "GET /reviews" --> List["List Reviews (Paginated)"]
    Server -- "PATCH /reviews/id" --> Update["Update Review"]
    Server -- "DELETE /reviews/id" --> Delete["Delete Review"]
    
    Create --> Session["SQLModel Session"]
    List --> Session
    Update --> Session
    Delete --> Session
    
    Session -- "ORM" --> DB["SQLite (rangmanch.db)"]
```

### Concepts Covered
- SQLModel for database models (combines SQLAlchemy + Pydantic)
- SQLite as a zero-config database
- FastAPI lifespan events for startup/shutdown logic
- Session dependency injection
- Full CRUD operations
- Pagination with skip/limit
- Aggregation queries (average rating)

---

## 4. Tiffin Order Tracking API

A Mumbai tiffin delivery service needs to track orders as they move through stages — from kitchen preparation to final delivery. Delivery staff update the status at each checkpoint.

An order tracking API with status transitions (preparing, picked_up, in_transit, delivered), multi-parameter filtering, and a daily summary dashboard endpoint.

### System Architecture

```mermaid
graph TD
    subgraph Status Flow
        direction LR
        preparing --> picked_up --> in_transit --> delivered
    end

    Client["Client (Delivery Staff)"] --> Server["FastAPI Server"]
    Server --> Orders["Orders Router"]
    Server --> Stats["Stats Router"]
    Orders --> DB["SQLite (dabbawala.db)"]
    Stats --> DB
```

### Concepts Covered
- Python Enum for controlled status values
- PATCH for partial updates (vs PUT for full replacement)
- DateTime handling and date-based filtering
- Multiple query parameters working together
- Aggregation for daily reports
- Multiple routers in one app

---

## 5. College Book Exchange API

Delhi University students need a platform to buy and sell used textbooks. Sellers list their books with a price, and buyers browse or search. When a book is purchased, the seller marks it as sold.

A REST API for a college book exchange with:
- User registration (name, email, college)
- Book listings with search by title or author
- Mark books as sold
- API key authentication on write operations

### System Architecture

```mermaid
graph LR
    Client["Client (Student App)"] --> Auth{"X-API-<br>Key<br>Check"}
    Auth -- "Valid" --> Server["FastAPI Server"]
    Auth -- "Invalid" --> Forbidden["403 Forbidden"]
    
    Server --> UsersRouter["Users Router"]
    Server --> BooksRouter["Books Router"]
    
    UsersRouter --> DB["SQLite DB"]
    BooksRouter --> DB
    
    DB --> UsersTable["Users Table"]
    DB --> BooksTable["Books Table"]
```

### Concepts Covered
- SQLModel relationships - one-to-many (User has many Books)
- APIRouter - organize routes into separate files
- Header dependency - protect endpoints with an X-API-Key header
- Query parameters - search and filter results

---

## 6. Live Polling System API

IIT Bombay fest needs a live polling system where audience members vote from their phones and see results update in real-time on the big screen. No page refresh — votes appear instantly via WebSocket.

- REST API to create polls and cast votes
- WebSocket endpoint that broadcasts vote updates to all connected clients
- Live HTML page with animated vote bars that update without refresh
- ConnectionManager pattern to handle multiple WebSocket rooms

### System Architecture

```mermaid
graph TD
    Client["Client"] -- "REST" --> CreatePoll["POST /polls/<br>Create Poll"]
    Client -- "REST" --> CastVote["POST /polls/id/vote<br>Cast Vote"]
    Client -- "WebSocket" --> ConnManager["Connection Manager"]
    
    CreatePoll --> DB["MongoDB"]
    CastVote --> DB
    
    CastVote --> ConnManager
    
    ConnManager -- "Broadcast" --> LiveUpdates["Connected Clients<br>Live Updates"]
```

### Concepts Covered
- FastAPI + Uvicorn
- Motor (async MongoDB)
- WebSocket (built into FastAPI)
- Vanilla JS for the frontend