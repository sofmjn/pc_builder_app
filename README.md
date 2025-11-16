# Architecture Documentation

## Use Case Diagram

```mermaid
flowchart TD
    User([Пользователь]) --> |Создаёт сборку| UC_CreateBuild
    User --> |Добавляет компоненты| UC_AddComponent
    User --> |Удаляет компоненты| UC_RemoveComponent
    User --> |Просматривает каталог| UC_ViewCatalog
    User --> |Фильтрует комплектующие| UC_Filter
    User --> |Проверяет совместимость| UC_Compatibility

    UC_CreateBuild --> UC_Compatibility
    UC_AddComponent --> UC_Compatibility
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
    }

    User "1" --> "0..*" Build : owns
    Build "0..*" --> "0..*" Component : contains

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
