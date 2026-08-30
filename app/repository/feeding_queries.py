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

GET_TODAYS_FEEDINGS = """--sql
SELECT timestamp, volume_ml, user_name
FROM feedings WHERE date(timestamp) = date('now', 'localtime') ORDER BY timestamp ASC;
"""

GET_YESTERDAYS_FEEDINGS = """--sql
SELECT timestamp, volume_ml, user_name FROM feedings WHERE date(timestamp) = date('now', '-1 day', 'localtime')
ORDER BY timestamp ASC;
"""

GET_FEEDINGS_BY_DATE = """--sql
SELECT timestamp, volume_ml, user_name FROM feedings WHERE date(timestamp) = ?
ORDER BY timestamp ASC;
"""

UPDATE_FEEDING_VOLUME = """--sql
UPDATE feedings SET volume_ml = ? WHERE id = ?;
"""