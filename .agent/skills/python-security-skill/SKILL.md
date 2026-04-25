---
name: python-security-skill
description: Guides Python/FastAPI developers through essential security and performance best practices. Use when writing or reviewing FastAPI endpoints, SQLAlchemy database interactions, or handling user input to prevent vulnerabilities like Mass Assignment and N+1 queries.
---

# Python & FastAPI Security Guidelines

This skill provides mandatory checks and patterns for developing secure, performant Python applications using FastAPI and SQLAlchemy.

## Core Mandates

### 1. Prevent Mass Assignment Vulnerabilities

**Do not** dynamically assign dictionary key-values directly to SQLAlchemy models from user input without validation. This allows attackers to modify system fields (like `id`, `user_id`, `role`).

**Vulnerable Pattern:**
```python
def update_user(user_id: int, data: dict, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    # DANGEROUS: Blindly applying all provided keys
    for key, value in data.items():
        setattr(user, key, value)
    db.commit()
```

**Secure Pattern (Use Pydantic):**
```python
from pydantic import BaseModel, Field
from typing import Optional

# Define exactly what fields are allowed to be updated
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    age: Optional[int] = Field(None, ge=0, le=120)

def update_user(user_id: int, data: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    # SAFE: Only fields defined in the UserUpdate model are applied
    update_data = data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    db.commit()
```

### 2. Eliminate N+1 Query Problems

When querying lists of items that have relationships (e.g., retrieving `Rounds` and their associated `Course` names), SQLAlchemy will execute an additional query for *each* item during serialization unless explicitly told to join them.

**Vulnerable Pattern:**
```python
@router.get("/rounds")
def list_rounds(db: Session = Depends(get_db)):
    rounds = db.query(Round).all() # Query 1
    results = []
    for r in rounds:
        # DANGEROUS: Executes a new query for r.course EVERY loop iteration
        results.append({"name": r.course.name}) 
    return results
```

**Performant Pattern (Use joinedload):**
```python
from sqlalchemy.orm import joinedload

@router.get("/rounds")
def list_rounds(db: Session = Depends(get_db)):
    # SAFE: Fetches rounds and associated courses in a single SQL join query
    rounds = db.query(Round).options(joinedload(Round.course)).all()
    results = [{"name": r.course.name} for r in rounds]
    return results
```

### 3. Maintain a Single Source of Truth (DRY)

Avoid duplicating business logic (e.g., regex parsing, string normalization, status calculations) across the frontend and backend. 

- **Rule:** The Backend must be the Single Source of Truth for data validation and parsing.
- **Why:** If logic is duplicated, it will inevitably drift, causing subtle, hard-to-track bugs.
- **Implementation:** The frontend should strictly handle UI state and event routing, immediately passing raw data to the backend for processing.

### 4. Optimize Database Insertions (Bulk Insert)

When creating multiple related records simultaneously, avoid executing `db.add()` and `db.commit()` inside a loop.

**Vulnerable Pattern:**
```python
# DANGEROUS: High overhead from multiple individual transaction calls
for i in range(18):
    hole = RoundScore(hole_number=i)
    db.add(hole)
db.commit()
```

**Performant Pattern (Use add_all):**
```python
# SAFE: Efficient bulk insertion
holes = [RoundScore(hole_number=i) for i in range(18)]
db.add_all(holes)
db.commit()
```

## Review Checklist

Before completing any Python/FastAPI implementation, verify:
- [ ] Are all API input payloads strictly typed with Pydantic models?
- [ ] Are dynamic updates (`setattr`) restricted to Pydantic `exclude_unset=True` dictionaries?
- [ ] Are foreign key relationships accessed in loops pre-loaded using `joinedload` or `selectinload`?
- [ ] Are batch creations utilizing `db.add_all()`?
- [ ] Is complex parsing/validation logic centralized in the backend?