INSERT_FEEDING = """--sql
INSERT INTO feedings (user_name, volume_ml, timestamp)
VALUES (?, ?, ?);
"""

GET_ALL_FEEDINGS = """--sql
SELECT id, user_name, volume_ml, timestamp
FROM feedings ORDER BY timestamp DESC;
"""

DELETE_FEEDING = """--sql
DELETE FROM feedings WHERE id=?;
"""

GET_LAST_FEEDING = """--sql
SELECT id, user_name, volume_ml, timestamp
FROM feedings ORDER BY timestamp DESC
LIMIT 1;
"""