# Django versions: from 4.2 LTS to the current release

Written 26/11/2026 from the Django release notes for 5.0, 5.1, 5.2, 6.0 and 6.1. The track teaches the
current release (6.1); this file is for a codebase that is still on 4.2.

**Where 4.2 stands.** The 5.2 release notes say that support for the previous long-term-support release,
Django 4.2, ends in April 2026: a 4.2 project no longer gets security fixes. 5.2 is the current LTS (three
years of security updates from its release). Django REST framework's current release officially supports
Django 5.2, 6.0 and 6.1. The usual route is 4.2 to 5.2 LTS, then on to 6.x, running the tests and fixing
deprecation warnings at each step.

**Python needed** (from the installation FAQ): 4.2 supports 3.8 to 3.12; 5.0, 3.10 to 3.12; 5.1, 3.10 to
3.13; 5.2, 3.10 to 3.14; 6.0, 3.12 to 3.14; 6.1, 3.12 to 3.15.

| Release | What it adds that matters to a learner | Modules |
| --- | --- | --- |
| 5.0 | facet filters in the admin; simpler templates for form fields; `Field.db_default` (database-computed defaults); `GeneratedField` (database generated columns); more ways to declare field choices; async support for signals and more | 2, 4 |
| 5.1 | the `{% querystring %}` template tag; PostgreSQL connection pools; `LoginRequiredMiddleware` and `login_not_required` (require login by default) | 1, 5, 12 |
| 5.2 | automatic model imports in `shell`; `CompositePrimaryKey` (a primary key of several fields) | 2, 3 |
| 6.0 | built-in Content Security Policy support; template partials (`{% partialdef %}`, `{% partial %}`); a built-in Tasks framework for background work (Django defines and queues tasks, external workers run them); the modern email API; `DEFAULT_AUTO_FIELD` now defaults to `BigAutoField`; support for Python below 3.12 dropped | 1, 5, 11 |
| 6.1 | configurable model field fetch modes (an answer to N+1 on unfetched fields); database-level delete options for `ForeignKey.on_delete` (`DB_CASCADE`, `DB_SET_NULL`, `DB_SET_DEFAULT`); the `MAILERS` setting for several email backends; calendar versioning (the releases once planned as 7.0 and 7.1 are now 2028 and 2029) | 3, 7 |

## Things removed between 4.2 and 6.1 that break old code

Taken from the "Features removed" sections of the release notes:

- **5.0**: the `USE_L10N` setting; support for `pytz` time zones (and the `is_dst` arguments); the default of
  `USE_TZ` became `True`.
- **5.1**: the `DEFAULT_FILE_STORAGE` and `STATICFILES_STORAGE` settings (use `STORAGES`, which exists since
  4.2); `Meta.index_together` (use `Meta.indexes`); `BaseUserManager.make_random_password()`; the SHA1 and
  unsalted password hashers.
- **6.0**: the `check` keyword of `CheckConstraint` (deprecated in 5.1 in favour of `condition`); positional
  arguments to constraints.
- **6.1**: the `all` parameter of `staticfiles.finders.find()` (now `find_all`).

How to use this: run your tests on 4.2 with `python -W error::DeprecationWarning`, fix what they report, then
move one release at a time and read that release's "Backwards incompatible changes" and "Features removed".
