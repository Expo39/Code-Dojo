# Lessons: m12_operations_deployment

Concepts in this module that a `teach me` lesson can cover: a Compose stack, application servers, reverse proxy and HTTPS, static and media in production, migrations in a release, backup and restore, logging and monitoring, secrets, upgrading Django, cloud deployment.

Most lessons in this track start from a source you read yourself (the track README, "How lessons work"),
then a recall in your own words, then the tutor's questions; a lesson runs the five PRIMM steps
(`docs/CHECKLISTS.md`, section 2) where code behaviour is the point. Code you type in a lesson goes in your
own folder:

```text
workspace/django/m12_operations_deployment/primm/<topic>.py
```

`python dojo.py primm m12_operations_deployment <topic>` creates that folder and an empty lesson file. The examples are always on
a different problem from the exercises in this module. Lesson files are not exercises: the tracker ignores
everything under `primm/`. Where a topic changed between Django 4.2 and the current release, `../VERSIONS.md`
says how.
