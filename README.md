# Mini twitter

API Rest que busca simular o comportamento básico do twitter:
    - Postar
    - Ver posts de outros usuários

A api foi construida com Django, e usa postgres como banco de dados


Diagrama de entidade relacional da aplicação:

```mermaid
erDiagram
    USER ||--o{ POST : post
    USER {
        id int pk
        password string
        last_login timestamp
        is_superuser boolean
        username string
        first_name string
        last_name string
        email string
        is_staff boolean
        is_active boolean
        date_joined timestamps
    }

    POST {
        int id pk
        int user_id fk
        string content
        timestamps created_at
    }
```
