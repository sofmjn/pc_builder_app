# Архитектура приложения «PC Builder Mobile App»

## UML Use Case
```mermaid
flowchart TD
    User[Пользователь] --> Register[Регистрация]
    User --> Login[Вход]
    User --> ViewHome[Главный экран]
    User --> ViewComponents[Каталог компонентов]
    User --> Filter[Фильтрация компонентов]
    User --> CreateBuild[Создание сборки]
    User --> EditBuild[Редактирование сборки]
    User --> DeleteBuild[Удаление сборки]
    User --> AddComponent[Добавление компонента в сборку]
    User --> RemoveComponent[Удаление компонента из сборки]

    MobileApp[Мобильное приложение] --> Backend[Backend Django API]
    Register --> Backend
    Login --> Backend
    ViewComponents --> Backend
    Filter --> Backend
    CreateBuild --> Backend
    EditBuild --> Backend
    DeleteBuild --> Backend
    AddComponent --> Backend
    RemoveComponent --> Backend

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
    flowchart TD
    User[Пользователь] --> MobileApp[Мобильное приложение]
    MobileApp --> Backend[Backend Django API]
    Backend --> Database[(SQLite)]
```

## C2 — Контейнеры
```mermaid
%%{init: {'theme': 'default'}}%%
graph TB
    MobileApp[Flutter App]
    API[Backend Django REST]
    DB[(SQLite)]
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
