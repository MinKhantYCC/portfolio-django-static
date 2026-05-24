# Portfolio Admin Content Design

## Context

The current portfolio app is a small Django project with one app, `staticportfolio`. The home page is rendered from a mostly static template at `staticportfolio/templates/staticportfolio/index.html`, with styling and behavior in `staticportfolio/static/staticportfolio/index.css` and `main.js`. The richer reference files are present at the repository root as `original.html`, `original.css`, and `original.js`.

The current app also exposes a `letter-to-thon` route that renders the old Valentine page. That URL is unrelated to the portfolio and will be removed from the public URL configuration.

## Goals

- Use Django's built-in admin dashboard as the only content management interface.
- Store editable portfolio content in PostgreSQL on Vercel through Django models.
- Let `index` query the database and render education, work experience, projects, skills, services, clients, profile/contact details, blogs, and contact form state.
- Move the current hard-coded portfolio content into `staticportfolio/info.json`.
- Keep database tables empty by default. If a section has no database records, render fallback values from `info.json`.
- Preserve the visual structure and behavior of `original.html`, `original.css`, and `original.js`.
- Save contact form submissions in the database.
- Add environment-variable examples in `.env.sample`.
- Use `.venv` and Pipenv for package management.

## Non-Goals

- No custom admin dashboard or separate CMS UI.
- No user-facing authentication system beyond Django admin.
- No automatic Medium API synchronization in the first implementation.
- No redesign of the current portfolio theme.
- No initial database fixture that preloads the current content.

## Data Model

The app will use regular Django models registered in `admin.py`.

- `Profile`: single active profile record with name, title, avatar URL, email, phone, birthday, location, about text, GitHub URL, LinkedIn URL, Medium URL, and optional resume URL.
- `Service`: title, description, icon URL, display order, active flag.
- `Client`: name, logo URL, website URL, display order, active flag.
- `Education`: institution, degree, field or summary title, start date, optional end date, current flag, description, display order, active flag.
- `WorkExperience`: role, company, start date, optional end date, current flag, description, display order, active flag.
- `Skill`: name, proficiency percentage, display order, active flag.
- `ProjectCategory`: name and slug.
- `Project`: title, category, image URL, project URL, summary, display order, active flag.
- `BlogPost`: title, category, published date, image URL, external URL, excerpt, display order, active flag. Medium posts can be entered here manually.
- `ContactMessage`: full name, email, message, created timestamp, read flag.

Most public content models will order by `display_order` and then primary key. Public queries will filter `active=True`.

## Fallback Data

`staticportfolio/info.json` will hold the current hard-coded values in a structure that mirrors the template context:

- `profile`
- `services`
- `clients`
- `education`
- `experience`
- `skills`
- `project_categories`
- `projects`
- `blogs`

The database remains the primary source. The view will use database rows for a section when rows exist. If a section is empty, it will use the corresponding list or object from `info.json`. This lets the deployed site stay populated while the admin starts empty.

## View And Form Flow

The `index` view will handle both `GET` and `POST`.

For `GET`, it will build a context from database records plus JSON fallbacks, then render `staticportfolio/index.html`.

For contact form `POST`, it will validate a Django form with full name, email, and message. A valid submission will create a `ContactMessage`, add a success message, and redirect back to the contact section using a fragment. Invalid submissions will re-render the page with form errors and the submitted values. CSRF protection stays enabled through Django's standard middleware and `{% csrf_token %}`.

The obsolete `letter-to-thon` URL will be removed from `staticportfolio/urls.py`. The Valentine view/template/static files can remain unused unless later cleanup is requested.

## Admin

Each content model will be registered with Django admin using focused `ModelAdmin` classes:

- list displays for names, active flags, ordering, and dates.
- filters for active/read/current/category fields where useful.
- search fields for title, company, institution, name, and email fields.
- editable ordering and active/read flags where low-risk.

The `Profile` model will be treated as singleton by convention in admin and by querying the first active profile in the view.

## Settings And Environment

Settings will remain in the current single `portfolio/settings.py` file to avoid a broad project restructure. Environment variables will drive deployment configuration:

- `DJANGO_SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `CSRF_TRUSTED_ORIGINS`
- `DATABASE_URL`
- `EMAIL_BACKEND`
- `DEFAULT_FROM_EMAIL`

The implementation will use `dj-database-url` for `DATABASE_URL` parsing and `psycopg` for PostgreSQL support. If `DATABASE_URL` is missing, local development falls back to SQLite. Production security settings should keep `DEBUG=False`, use explicit allowed hosts, and keep CSRF enabled.

`.env.sample` will document expected variables without real secrets.

## Dependency Management

The project currently has `requirements.txt` and an existing `.venv` directory. The implementation will add Pipenv support with a `Pipfile` and keep dependencies aligned for Django, WhiteNoise, PostgreSQL, and environment parsing. The `.venv` directory remains local and untracked.

## Frontend Preservation

The template will keep the existing class names and data attributes used by the CSS and JavaScript. Blog and contact sections from `original.html` will be restored with dynamic Django loops and form rendering. The navigation will include the same page-switching pattern as the original design.

Project filtering will continue to use lower-case category names in `data-category`, matching the current JavaScript filter behavior.

## Testing And Verification

Implementation verification will include:

- `python manage.py makemigrations --check --dry-run` after migrations are created.
- `python manage.py check`.
- `python manage.py test`.
- A local render smoke test for the index page with an empty database, confirming fallback JSON renders.
- A contact form POST test confirming a `ContactMessage` is saved.
- A URL test confirming `letter-to-thon` no longer resolves.

## Open Decisions

The approved first version uses manual blog entry through Django admin, with fallback blog data from `info.json` based on the Medium profile. Automatic Medium feed importing can be added later as a separate feature if needed.
