<h1>
  <img src="https://author.today/distCommon/images/at-logo.png" width="28" style="vertical-align:middle;" />
  author_today.py
</h1>

> Web-API for [author.today](https://author.today) read, search, and interact with Russia's largest platform for original fiction.

---

## Quick Start

```python
from author_today import AuthorToday

author_today = AuthorToday()

# Login with credentials
author_today.login(login="example@gmail.com", password="password")

# Or login with an existing token
author_today.login_with_token("your_token_here")
```

---

## Features

-  **Auth** — login by password or token, register, recover password
-  **Works** — get book info, chapters, content, catalog
-  **Home** — home page feed, disputed works
-  **Profile** — view and edit your account, follow/ignore users
-  **Library** — manage your reading library and bookmarks
-  **Messaging** — send messages, read chats, mark as read
-  **Notifications** — check unread notifications
-  **Engagement** — like works, send reports
-  **Search** — search works by title or browse the catalog

---

## Usage

### Auth

```python
author_today = AuthorToday()

# Login (stores token and user_id automatically)
author_today.login(login="example@gmail.com", password="password")

# Login with existing token
author_today.login_with_token("your_token_here")

# Register a new account
author_today.register(nickname="John Doe", email="example@gmail.com", password="password")

# Recover password
author_today.recover_password(email="example@gmail.com")

# Refresh session token
author_today.refresh_token()
```

### Profile

```python
# Get current user info
author_today.get_account_info()

# Edit profile
author_today.edit_profile(nickname="New Name", status="Writing something great", sex=1)

# Follow a user
author_today.follow_user(user_id="123")

# Add a user to ignore list
author_today.add_user_to_ignore(user_id="123")
```

### Works & Catalog

```python
# Get work metadata
author_today.get_work_meta_info(work_id=12345)

# Get full work content
author_today.get_work_content(work_id=12345)

# Read a specific chapter
author_today.get_chapter(work_id=12345, chapter_id=67890)

# Like a work
author_today.like_work(work_id=12345)

# Browse the catalog
author_today.get_catalog(sorting="recent", page=1, genre="fantasy")

# Get today's home page feed
author_today.get_home_page()
```

### Library

```python
# Get your saved library
author_today.get_account_library()

# Add a work to library
author_today.add_to_library(id=12345, state="read")
```

### Messaging

```python
# Get your recent chats
author_today.get_my_chats(page=1)

# Read messages in a chat
author_today.get_chat_messages(chat_id=42)

# Send a message
author_today.send_message(message="Hello!", chat_id=42)

# Mark a chat as read
author_today.mark_as_read(chat_id=42)
```

### Search

```python
author_today.search(title="Война и мир")
```

### Reporting

```python
author_today.send_report(
    category="spam",
    comment="This is spam",
    target_id=12345,
    target_type="work",
    url="https://author.today/work/12345"
)
```

---

## API Reference

| Method                  | Description                                      |
|-------------------------|--------------------------------------------------|
| `login`                 | Sign in with email and password                  |
| `login_with_token`      | Sign in with an existing token                   |
| `register`              | Create a new account                             |
| `recover_password`      | Send password recovery email                     |
| `refresh_token`         | Refresh the session token                        |
| `get_account_info`      | Get current user profile                         |
| `edit_profile`          | Update profile fields                            |
| `get_account_library`   | Get your saved book library                      |
| `add_to_library`        | Add or update a work in your library             |
| `get_work_meta_info`    | Get metadata for a work                          |
| `get_work_content`      | Get full content of a work                       |
| `get_chapter`           | Read a specific chapter                          |
| `like_work`             | Like or unlike a work                            |
| `get_catalog`           | Browse and filter the works catalog              |
| `get_home_page`         | Get the home page feed                           |
| `search`                | Search works by title                            |
| `get_my_chats`          | List recent chats                                |
| `get_chat_messages`     | Get messages in a chat                           |
| `send_message`          | Send a private message                           |
| `mark_as_read`          | Mark a chat as read                              |
| `check_notifications`   | Check for unread notifications                   |
| `follow_user`           | Follow/subscribe to a user                       |
| `add_user_to_ignore`    | Add a user to your ignore list                   |
| `send_report`           | Report content                                   |
| `get_disputed_works`    | Get list of disputed works                       |
| `track_last_activity`   | Update last activity timestamp                   |

---
