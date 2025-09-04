# 🗃️ Database Schema Documentation

## Overview
The Football League Manager system uses a relational database with **9 interconnected entities** designed to manage football leagues, teams, players, matches, and related operations.

## Database Technology
- **Development**: SQLite (`football.db`)
- **Production Ready**: PostgreSQL
- **ORM**: SQLAlchemy with Alembic migrations
- **Migration Tool**: Alembic

---

## 📊 Entity Relationship Diagram (ERD)

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│    Users    │    │    Teams    │    │   Venues    │
│─────────────│    │─────────────│    │─────────────│
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │
│ username    │    │ name        │    │ name        │
│ email       │    │ coach_name  │    │ city        │
│ full_name   │    │ founded_year│    │ country     │
│ hashed_pwd  │    │ home_ground │    │ capacity    │
│ created_at  │    │ created_at  │    │ built_year  │
│ updated_at  │    │ updated_at  │    │ created_at  │
└─────────────┘    └─────────────┘    │ updated_at  │
                           │           └─────────────┘
                           │
                           ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Players   │    │   Coaches   │    │  Managers   │
│─────────────│    │─────────────│    │─────────────│
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │
│ team_id (FK)│◄───┤ team_id (FK)│◄───┤ team_id (FK)│
│ name        │    │ name        │    │ name        │
│ position    │    │ exp_years   │    │ strategy    │
│ age         │    │ specializ.  │    │ created_at  │
│ created_at  │    │ nationality │    │ updated_at  │
│ updated_at  │    │ created_at  │    └─────────────┘
└─────────────┘    │ updated_at  │
                   └─────────────┘
                           
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Matches   │    │  Referees   │    │  Sponsors   │
│─────────────│    │─────────────│    │─────────────│
│ id (PK)     │    │ id (PK)     │    │ id (PK)     │
│ team_a_id   │────┤ name        │    │ name        │
│ team_b_id   │    │ exp_years   │    │ industry    │
│ match_date  │    │ nationality │    │ sponsor_amt │
│ venue       │    │ qualification│    │ created_at  │
│ score_team_a│    │ created_at  │    │ updated_at  │
│ score_team_b│    │ updated_at  │    └─────────────┘
│ created_at  │    └─────────────┘
│ updated_at  │
└─────────────┘
```

---

## 📋 Table Specifications

### 1. **Users Table**
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100),
    hashed_password VARCHAR(255) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: User authentication and profile management  
**Indexes**: `id (PK)`, `username (UNIQUE)`, `email (UNIQUE)`  
**Constraints**: Username and email must be unique

### 2. **Teams Table**
```sql
CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    coach_name VARCHAR(100),
    founded_year INTEGER,
    home_ground VARCHAR(150),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_founded_year CHECK (founded_year > 1800)
);
```

**Purpose**: Football team management  
**Indexes**: `id (PK)`, `name (UNIQUE)`  
**Constraints**: Founded year must be after 1800

### 3. **Players Table**
```sql
CREATE TABLE players (
    id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    position VARCHAR(50) NOT NULL,
    age INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_player_age CHECK (age >= 16 AND age <= 50)
);
```

**Purpose**: Player roster management  
**Relationships**: `team_id` references `teams(id)` *(1:Many)*  
**Indexes**: `id (PK)`  
**Constraints**: Player age between 16-50 years

### 4. **Coaches Table**
```sql
CREATE TABLE coaches (
    id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    experience_years INTEGER NOT NULL,
    specialization VARCHAR(100),
    nationality VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_coach_experience_years CHECK (experience_years >= 0)
);
```

**Purpose**: Coaching staff management  
**Relationships**: `team_id` references `teams(id)` *(1:Many)*  
**Indexes**: `id (PK)`  
**Constraints**: Experience years must be non-negative

### 5. **Matches Table**
```sql
CREATE TABLE matches (
    id INTEGER PRIMARY KEY,
    team_a_id INTEGER NOT NULL,
    team_b_id INTEGER NOT NULL,
    match_date DATETIME NOT NULL,
    venue VARCHAR(150) NOT NULL,
    score_team_a INTEGER DEFAULT 0,
    score_team_b INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_score_team_a CHECK (score_team_a >= 0),
    CONSTRAINT chk_score_team_b CHECK (score_team_b >= 0)
);
```

**Purpose**: Match fixtures and results  
**Relationships**: 
- `team_a_id` references `teams(id)` *(Many:1)*
- `team_b_id` references `teams(id)` *(Many:1)*

**Indexes**: `id (PK)`  
**Constraints**: Scores must be non-negative

### 6. **Venues Table**
```sql
CREATE TABLE venues (
    id INTEGER PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INTEGER NOT NULL,
    built_year INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_venue_capacity CHECK (capacity > 0),
    CONSTRAINT chk_venue_built_year CHECK (built_year > 1800)
);
```

**Purpose**: Stadium and venue management  
**Indexes**: `id (PK)`, `name (UNIQUE)`  
**Constraints**: Capacity > 0, Built year > 1800

### 7. **Referees Table**
```sql
CREATE TABLE referees (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    experience_years INTEGER NOT NULL,
    nationality VARCHAR(50),
    qualification_level VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_referee_experience_years CHECK (experience_years >= 0)
);
```

**Purpose**: Match officials management  
**Indexes**: `id (PK)`  
**Constraints**: Experience years must be non-negative

### 8. **Sponsors Table**
```sql
CREATE TABLE sponsors (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    industry VARCHAR(100),
    sponsorship_amount INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_sponsor_sponsorship_amount CHECK (sponsorship_amount > 0)
);
```

**Purpose**: Sponsorship and financial management  
**Indexes**: `id (PK)`, `name (UNIQUE)`  
**Constraints**: Sponsorship amount must be positive

### 9. **Managers Table**
```sql
CREATE TABLE managers (
    id INTEGER PRIMARY KEY,
    team_id INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    strategy VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_manager_strategy CHECK (strategy IS NOT NULL)
);
```

**Purpose**: Team management structure  
**Relationships**: `team_id` references `teams(id)` *(1:1)*  
**Indexes**: `id (PK)`  
**Constraints**: Strategy cannot be null

---

## 🔗 Relationships Summary

| Relationship Type | Description | Tables |
|-------------------|-------------|---------|
| **1:Many** | Team → Players | `teams(id)` ← `players(team_id)` |
| **1:Many** | Team → Coaches | `teams(id)` ← `coaches(team_id)` |
| **1:1** | Team → Manager | `teams(id)` ← `managers(team_id)` |
| **Many:Many** | Teams ↔ Matches | `teams(id)` ↔ `matches(team_a_id, team_b_id)` |

---

## 📈 Indexing Strategy

### Primary Indexes
- All tables have `id` as primary key with automatic indexing
- Unique constraints create automatic indexes on `name` fields

### Performance Indexes
Recommended additional indexes for production:

```sql
-- Search and filtering
CREATE INDEX idx_players_team_id ON players(team_id);
CREATE INDEX idx_coaches_team_id ON coaches(team_id);
CREATE INDEX idx_managers_team_id ON managers(team_id);
CREATE INDEX idx_matches_date ON matches(match_date);
CREATE INDEX idx_matches_teams ON matches(team_a_id, team_b_id);

-- Authentication lookups
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
```

---

## 🔄 Migration History

### Migration Files
1. **`c0bcb999f7cb_initial_migration.py`**: Initial schema creation
2. **`9067756d7394_add_specialization_to_coach_model.py`**: Added specialization to coaches

### Migration Commands
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Check current migration
alembic current
```

---

## 📊 Data Normalization

### Normalization Level: **3NF (Third Normal Form)**

**1NF**: ✅ All tables have atomic values, no repeating groups  
**2NF**: ✅ All non-key attributes fully depend on primary keys  
**3NF**: ✅ No transitive dependencies between non-key attributes

### Design Decisions
- **Denormalization**: `teams.coach_name` stored as string (not FK) for flexibility
- **Separation**: Coaches and Managers are separate entities for role clarity
- **Referential Integrity**: Foreign key relationships maintained through application logic

---

## 🎯 Complex Query Examples

### 1. Team Performance Analysis
```sql
-- Teams with win/loss records
SELECT 
    t.name,
    COUNT(CASE WHEN (m.team_a_id = t.id AND m.score_team_a > m.score_team_b) 
               OR (m.team_b_id = t.id AND m.score_team_b > m.score_team_a) 
          THEN 1 END) as wins,
    COUNT(CASE WHEN (m.team_a_id = t.id AND m.score_team_a < m.score_team_b)
               OR (m.team_b_id = t.id AND m.score_team_b < m.score_team_a)
          THEN 1 END) as losses
FROM teams t
LEFT JOIN matches m ON (t.id = m.team_a_id OR t.id = m.team_b_id)
GROUP BY t.id, t.name;
```

### 2. Venue Utilization Report
```sql
-- Match frequency by venue with capacity utilization
SELECT 
    v.name,
    v.capacity,
    COUNT(m.id) as matches_hosted,
    AVG(CASE WHEN m.team_a_id IS NOT NULL THEN v.capacity * 0.85 END) as avg_attendance
FROM venues v
LEFT JOIN matches m ON v.name = m.venue
GROUP BY v.id, v.name, v.capacity
ORDER BY matches_hosted DESC;
```

---

## 📝 Seed Data Structure

The database includes comprehensive seed data:
- **5 Teams**: Real football teams with historical data
- **25 Players**: 5 players per team with realistic positions
- **5 Coaches**: Experienced coaching staff
- **3 Venues**: International stadiums
- **6 Matches**: Complete fixture list with results
- **3 Users**: Admin, coach, and regular user accounts

---

## 🔐 Data Security & Constraints

### Security Features
- **Password Hashing**: bcrypt with salt
- **Unique Constraints**: Prevent duplicate usernames/emails
- **Check Constraints**: Data validation at database level

### Data Integrity
- **Age Validation**: Players 16-50, coaches/referees 0+ years
- **Financial Validation**: Positive sponsorship amounts
- **Temporal Validation**: Founded/built years after 1800
- **Score Validation**: Non-negative match scores

This schema supports all required functionality including authentication, CRUD operations, search/filtering, and complex reporting queries.
