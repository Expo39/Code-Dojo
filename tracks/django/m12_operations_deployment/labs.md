# Labs: m12_operations_deployment

Real services, your own account, your own money (`../labs/README.md`: set up, budget alert, tags and the teardown
routine first). A lab gives the goal and the checks, never the steps. Estimate the cost before you start, then
compare with the bill the next morning; prices are from 26/11/2026 and change.

## L12.1: Deploy the capstone, then remove it

- **Goal:** Run your capstone (project P3) in a cloud account as containers: a web service, a worker, a Redis
  container and a small managed PostgreSQL database, behind a load balancer with HTTPS (or HTTP for the lab),
  with the secret key and database password in a secrets service or environment and never in the image.
- **Services:** a container registry, a container service (ECS on Fargate: about $0.59 a day for the web task,
  about $0.30 each for a worker and a Redis task), an application load balancer (about $0.73 a day), a
  `db.t4g.micro` database (about $0.45 a day with storage), two or three secrets, a log group.
- **Estimated cost:** $2 to $5 if deleted the same day; about $17 a week if forgotten (roughly $2.40 a day).
- **Time:** about 6 hours.
- **Done when:** a public URL serves the app and a background task completes; `manage.py check --deploy`
  passes with no warning you cannot explain; no secret is in the image (prove it by inspecting the image); the real
  cost of the day is written next to your estimate.
- **Teardown:** delete everything with one command from your infrastructure code, then check by tag and in the
  billing console the next morning.

## L12.2: A release with a migration, and a rollback

- **Goal:** Deploy version 2 of the app with a backwards-compatible migration (add a nullable column, backfill it,
  then make it required in a later release), watch that the old version keeps working during the release, then
  roll back to version 1 and show the data is intact.
- **Services:** the L12.1 stack for a few more hours.
- **Estimated cost:** $1 to $3 (the stack's daily cost for the hours you run it).
- **Time:** about 4 hours.
- **Done when:** a written release plan with each step and its rollback, and a run where both versions served
  requests at the same time with no error.
- **Teardown:** as L12.1.

## L12.3: A backup you have restored

- **Goal:** Back up the database with `pg_dump`, encrypt the file, delete the database, restore it, and compare row
  counts and one checksum per table.
- **Services:** the L12.1 database; keep the encrypted dump on your own machine (storing it in object storage has
  its own price: check it first).
- **Estimated cost:** $0 to $1.
- **Time:** about 2 hours.
- **Done when:** a restore from the encrypted dump gives identical counts and checksums, and a written
  restore time.
- **Teardown:** delete the dump from anywhere it should not stay; delete the database.

## L12.4: The teardown audit

- **Goal:** Without looking at your notes, list every resource that still exists from the labs by tag and in the
  billing console, and delete what is left.
- **Services:** tag search, Cost Explorer.
- **Estimated cost:** $0.
- **Time:** about 1 hour.
- **Done when:** an empty tag search and a flat cost line the next day.
- **Teardown:** this is the teardown.
