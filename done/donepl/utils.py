from django.db import connection


def calculate_distance(worker_location, customer_location):
    query = """
    SELECT ST_Distance(%s, %s) as distance;
    """
    with connection.cursor() as cursor:
        cursor.execute(query, [worker_location, customer_location])
        result = cursor.fetchone()
        distance = result[0]
        return distance
