
# Technical Challenge @Ubiwhere - Pedro Rodrigues

## Requirements
- **Superuser: `UW_Master`**
- **Superuser password**: `UW123456`
- **Database User: `traffic_database_user`**
- **Database user password**: `UW`


## Prerequisites

1. **Install PostgreSQL**:

   ```bash
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. **Install PostGIS**:

   ```bash
   sudo apt-get install postgis postgresql-12-postgis-3
   ```

3. **Access PostgreSQL as the `postgres` user**:

   ```bash
   sudo -u postgres psql
   ```

4. **Create a new database**:

   ```sql
   CREATE DATABASE traffic_database;
   ```

5. **Create a new user with a password**:

   ```sql
   CREATE USER traffic_database_user WITH PASSWORD 'UW';
   ```

6. **Grant privileges to the user**:

   ```sql
   GRANT ALL PRIVILEGES ON DATABASE traffic_database TO traffic_database_user;
   ```

7. **Enable PostGIS extension**:

   ```sql
   \c traffic_database;
   CREATE EXTENSION postgis;
   ```

## User and Permission Configuration


To ensure the user `traffic_database_user` has the necessary permissions on all tables and sequences in the `public` schema, run the following command:

```sql
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO traffic_database_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO traffic_database_user;
```

---

## Table Creation and Data Import

### 1. Create the `traffic_speed` Table

With the `traffic_database_user` configured, you can create the `traffic_speed` table to store geospatial data.

```sql
CREATE TABLE traffic_speed (
    id SERIAL PRIMARY KEY,
    long_start DOUBLE PRECISION,
    lat_start DOUBLE PRECISION,
    long_end DOUBLE PRECISION,
    lat_end DOUBLE PRECISION,
    length DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    geom_start GEOMETRY(Point, 4326),
    geom_end GEOMETRY(Point, 4326)
);
```
### 2. Import Data from the CSV File

```sql
COPY traffic_speed (long_start, lat_start, long_end, lat_end, length, speed)
FROM '/path/to/traffic_speed.csv' DELIMITER ',' CSV HEADER;
```


### 3. Update the Geometry Columns

After importing the data, you need to populate the geospatial columns (`geom_start` and `geom_end`) with the coordinates:

```sql
UPDATE traffic_speed
SET geom_start = ST_SetSRID(ST_MakePoint(long_start, lat_start), 4326),
    geom_end = ST_SetSRID(ST_MakePoint(long_end, lat_end), 4326)
WHERE long_start IS NOT NULL AND lat_start IS NOT NULL 
  AND long_end IS NOT NULL AND lat_end IS NOT NULL;
```

## 4. Update Permissions in the Database

To ensure that the user has the necessary permissions for future data additions and operations, run:

```sql
GRANT ALL PRIVILEGES ON DATABASE traffic_database TO traffic_database_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO traffic_database_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO traffic_database_user;
```

---
## 2. Project Configuration


1. **Configure the database in `settings.py`**:

   In `settings.py`, adjust the database settings as follows:

   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.contrib.gis.db.backends.postgis',
           'NAME': 'traffic_database',
           'USER': 'traffic_database_user',
           'PASSWORD': 'UW',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

2. **Apply database migrations**:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

## 3. Running the Application

1. **Create a superuser**:

   ```bash
   python manage.py createsuperuser
   ```

2. **Run the Django development server**:

   ```bash
   python manage.py runserver
   ```
3. ** Run Tests
    ```bash
   python manage.py test
   ```
   
   The API should now be running at `http://127.0.0.1:8000/`.

## 4. API Documentation

This project uses Swagger for API documentation. You can access the interactive documentation by navigating to:

```
http://127.0.0.1:8000/api/docs/
```
