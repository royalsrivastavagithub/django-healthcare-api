# Healthcare Backend API

A Django REST Framework backend for managing patients, doctors, and their assignments, secured with JWT authentication.

## Assignment Summary

### Requirements Fulfilled

- Django + DRF backend
- PostgreSQL database
- JWT authentication (djangorestframework-simplejwt)
- RESTful API endpoints for patients and doctors
- Django ORM for database modeling
- Error handling and validation
- Environment variables for sensitive config

### API Endpoints (16/16)

**Auth**
- `POST /api/auth/register/` — Register with name, email, password
- `POST /api/auth/login/` — Login, returns JWT tokens

**Patients** (all require auth, scoped to creator)
- `POST /api/patients/` — Create
- `GET /api/patients/` — List own
- `GET /api/patients/:id/` — Detail
- `PUT /api/patients/:id/` — Update
- `DELETE /api/patients/:id/` — Delete

**Doctors** (all require auth, all can list, only creator can modify)
- `POST /api/doctors/` — Create
- `GET /api/doctors/` — List all
- `GET /api/doctors/:id/` — Detail
- `PUT /api/doctors/:id/` — Update
- `DELETE /api/doctors/:id/` — Delete

**Mappings** (all require auth)
- `POST /api/mappings/` — Assign doctor to patient
- `GET /api/mappings/` — List all
- `GET /api/mappings/:patient_id/` — Get doctors for a patient
- `DELETE /api/mappings/:id/` — Remove mapping

### Expected Outcomes

- Users can register and log in ✅
- Authenticated users manage patients/doctors ✅
- Patients assigned to doctors ✅
- Data stored in PostgreSQL ✅

---

## Extras Beyond the Assignment

These were added to improve code quality, security, and developer experience:

| Extra | Why |
|---|---|
| **Token refresh endpoint** (`POST /api/auth/token/refresh/`) | Required by frontend clients to maintain sessions without re-login |
| **Custom User model** (email-based login) | Email as identifier is standard in healthcare apps; avoids username field |
| **Shared `IsOwner` permission** in `accounts/permissions.py` | Eliminates duplicated permission logic across patient and doctor apps |
| **Field-level validation** (age 0-150, gender enum, contact format, experience 0-70) | Prevents bad data at the API layer before reaching the database |
| **Duplicate email + duplicate mapping prevention** | Gives clean 400 errors instead of database integrity errors |
| **`ModelViewSet` for all CRUD endpoints** | Consistent pattern across the codebase — one class per resource |
| **Router-based URL configuration** | Auto-generates RESTful URLs, reduces boilerplate, ensures consistency |
| **Partial update (PATCH) support** | Built into ModelViewSet — allows updating single fields |
| **`.env.example`** | Documents required environment variables for new developers |
| **`.gitignore` with `.env`** | Prevents accidental commit of secrets |
| **`requirements.txt`** | Pin-installed with hashes — allows `pip install -r requirements.txt` |
| **Doctor detail/update/delete scoped to creator** | The assignment defines doctor list as "all doctors" but doesn't scope detail/modify. We restrict these to the creator as defense-in-depth, matching the patient pattern. All users still see every doctor in the list view. |
| **60 automated tests** | Covers every endpoint, every HTTP method, permissions, validation, auth failures, and edge cases — run with `uv run python manage.py test` |

## Setup

1. Clone the repo
2. Copy `.env.example` to `.env` and fill in your PostgreSQL credentials
3. Run `uv sync` (or `pip install -r requirements.txt`)
4. Run `uv run python manage.py migrate`
5. Run `uv run python manage.py test` (60 tests)
6. Run `uv run python manage.py runserver`
