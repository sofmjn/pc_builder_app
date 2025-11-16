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
    User->>MobileApp: Открывает приложение
    MobileApp->>Backend: GET /api/users/me/
    Backend-->>MobileApp: Возвращает данные пользователя

    User->>MobileApp: Создать сборку
    MobileApp->>Backend: POST /api/components/builds/
    Backend-->>MobileApp: Возвращает новую сборку

    User->>MobileApp: Добавить компонент
    MobileApp->>Backend: POST /api/components/builds/{id}/add_component/
    Backend-->>MobileApp: Обновлённая сборка

    User->>MobileApp: Редактировать сборку
    MobileApp->>Backend: PUT /api/components/builds/{id}/
    Backend-->>MobileApp: Обновлённая сборка

    User->>MobileApp: Удалить компонент
    MobileApp->>Backend: POST /api/components/builds/{id}/remove_component/
    Backend-->>MobileApp: Обновлённая сборка

    User->>MobileApp: Удалить сборку
    MobileApp->>Backend: DELETE /api/components/builds/{id}/
    Backend-->>MobileApp: Подтверждение удаления

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
flowchart TD
    ComponentService --> ComponentModel[Модель Component]
    ComponentService --> ComponentSerializer[Сериализатор ComponentSerializer]
    ComponentService --> ComponentView[Views: ComponentListView, ComponentDetailView]
    
    BuildService --> BuildModel[Модель Build]
    BuildService --> BuildSerializer[BuildSerializer]
    BuildService --> BuildView[Views: BuildListCreateView, BuildDetailView, add/remove_component]

    AuthService --> UserModel[Модель User]
    AuthService --> RegisterSerializer
    AuthService --> LoginAPIView
```

## BPMN (Пример сценария “Создание сборки”)
```mermaid
flowchart TD
    Start([Начало]) --> Login[Вход/Регистрация]
    Login --> Browse[Просмотр каталога компонентов]
    Browse --> Filter[Фильтрация компонентов]
    Filter --> SelectComponent[Выбор компонента]
    SelectComponent --> AddToBuild[Добавление в сборку]
    AddToBuild --> ReviewBuild[Просмотр сборки]
    ReviewBuild --> EditBuild[Редактирование сборки]
    EditBuild --> RemoveComponent[Удаление компонента из сборки]
    RemoveComponent --> SaveBuild[Сохранение сборки]
    SaveBuild --> DeleteBuild[Удаление сборки]
    DeleteBuild --> End([Конец])


```
