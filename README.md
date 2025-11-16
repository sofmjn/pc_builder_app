# Architecture Documentation

## Use Case Diagram

```mermaid
%%{init: {'theme': 'default'}}%%
usecaseDiagram
    actor User
    actor System as Backend
    actor App as MobileApp

    User --> (Register)
    User --> (Login)
    User --> (View Home Screen)
    User --> (View Components Catalog)
    User --> (Filter Components)
    User --> (Create Build)
    User --> (Edit Build)
    User --> (Delete Build)
    User --> (Add Component to Build)
    User --> (Remove Component from Build)
    
    App --> Backend
    (Register) --> Backend
    (Login) --> Backend
    (View Components Catalog) --> Backend
    (Filter Components) --> Backend
    (Create Build) --> Backend
    (Edit Build) --> Backend
    (Delete Build) --> Backend
    (Add Component to Build) --> Backend
    (Remove Component from Build) --> Backend

```

## Class Diagram

```mermaid
%%{init: {'theme': 'default'}}%%
classDiagram
    class User{
        +id: int
        +username: str
        +email: str
        +password: str
        +first_name: str
        +last_name: str
    }

    class Component{
        +id: int
        +name: str
        +type: str
        +brand: str
        +price: Decimal
        +compatibility: str
        +link: str
    }

    class Build{
        +id: int
        +name: str
        +description: str
        +created_at: datetime
        +updated_at: datetime
        +total_price(): Decimal
        +components_by_type(): dict
    }

    class HomeScreen{}
    class LoginScreen{}
    class ComponentsScreen{}
    class CreateBuildPage{}
    class EditBuildPage{}

    User "1" --> "0..*" Build : owns
    Build "0..*" --> "0..*" Component : contains
    HomeScreen --> Build
    HomeScreen --> Component
    ComponentsScreen --> Component
    CreateBuildPage --> Build
    EditBuildPage --> Build


```

## Sequence Diagram — Добавление компонента

```mermaid
sequenceDiagram
    participant U as User
    participant F as Frontend
    participant B as Backend
    participant DB as Database

    U->>F: выбирает компонент
    F->>B: POST /builds/{id}/add-component
    B->>DB: запрос данных компонента
    DB-->>B: данные компонента

    B->>B: Проверка совместимости
    alt Совместимо
        B-->>F: { status: "ok" }
        F-->>U: Компонент добавлен
    else Не совместимо
        B-->>F: { status: "error", reason: "Несовместимо" }
        F-->>U: Ошибка совместимости
    end
```

## C1 — Контекст (System Context)
```mermaid
%%{init: {'theme': 'default'}}%%
graph TB
    User[Пользователь]
    MobileApp[Mobile App (Flutter)]
    Backend[Backend (Django REST API)]
    DB[(PostgreSQL)]
    External[Внешние сервисы: DNS, PCPartPicker]

    User --> MobileApp
    MobileApp --> Backend
    Backend --> DB
    Backend --> External
```

## C2 — Контейнеры
```mermaid
%%{init: {'theme': 'default'}}%%
graph TB
    MobileApp[Flutter App]
    API[Backend Django REST]
    DB[(PostgreSQL)]
    Scraper[Scraper / Parser Components]

    MobileApp -->|REST API| API
    API --> DB
    API --> Scraper


```

## C3 — Компоненты Backend
```mermaid
%%{init: {'theme': 'default'}}%%
graph TD
    AuthService[Authentication Service]
    UserService[User Profile Service]
    BuildService[Build Management Service]
    ComponentService[Component Catalog Service]
    CompatibilityService[Compatibility Checker]

    API --> AuthService
    API --> UserService
    API --> BuildService
    API --> ComponentService
    API --> CompatibilityService

```

## BPMN (Пример сценария “Создание сборки”)
```mermaid
%%{init: {'theme': 'default'}}%%
flowchart TD
    Start((Start))
    Login[Login Screen]
    Home[Home Screen]
    CreateBuild[Create Build Screen]
    SelectComponents[Select Components]
    AddComponent[Add Component to Build]
    CheckCompatibility[Check Compatibility]
    SaveBuild[Save Build]
    End((End))

    Start --> Login --> Home --> CreateBuild --> SelectComponents --> AddComponent --> CheckCompatibility --> SaveBuild --> End


```
