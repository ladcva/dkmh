
# DKMH

## Overall Architecture

![Overall Architecture](dkmh.drawio.png)

## Project structure

**config**: contains configuration files
**crawler**: contains classes, classes' details crawlers, and a CDC process
**db_migration**: contains databse creation and initial load
**executor**: execute the registration processes    
**orchestrator**: contains Airflow DAGs that orchestrate the whole process
**utils**: contains utility functions
**testing**: contains unit tests