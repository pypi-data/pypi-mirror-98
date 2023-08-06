'''
A simple tool for exporting from a PostGIS table to GeoJSON and TopoJSON. Assumes Python 2.7+,
psycopg2, and TopoJSON are already installed and in your PATH.

Adapted from Bryan McBride's PHP implementation
(https://gist.github.com/bmcbride/1913855/)
by John Czaplewski | jczaplew@gmail.com | @JJCzaplewski

python main.py -d awesomeData -H localhost -u user -p securePassword -t public
.panogps  -f id imgname  geom
TODO:
- Add argument for SRS
- Clean up

'''
import decimal
from _ast import arguments


import json

# pointDistance = 1
# line = [1, 2, 3]
from psycopg2.extras import RealDictCursor

def getData(conn, config, database, gui):
    cur = conn.connect()

    # Start building the query
    query = "SELECT "

    # If a list of fields were provided, add those
    if isinstance("", list):
        for each in arguments.fields:
            query += each + ", "

        # Otherwise, just select everything
    else:
        query += "geom,"

    query += "ST_AsGeoJSON(geom) AS geometry FROM " + config['table']
    # If a WHERE statement was provided, add that

    if gui:
        isnull_where = database.where

        limit = database.limit if database.limit else "all"
        if isnull_where is not None:
            query += " WHERE " + str(database.where) + " ORDER BY ID LIMIT " + str(limit) + ";"
        else:
            query += " ORDER BY ID LIMIT " + str(limit) + ";"
    else:
        query += " WHERE " + str(config["where"]) + " ORDER BY ID LIMIT " + str(config["limit"]) + ";"

    print(query)
    # Execute the query
    try:
        cur.execute(query)
    except:
        print("Unable to execute query. Please check your options and try again.")
        return

    # Retrieve the results of the query
    cur = conn.execute(query, cursor_factory=RealDictCursor)
    rows = cur.fetchall()
    result = []
    for row in rows:
        row_as_dict = dict(row)
        result.append(row_as_dict)

    # output is the main content, rowOutput is the content from each record returned
    output = ""
    rowOutput = ""
    i = 0
    while i < len(result):

        firstCoord = (json.loads(result[i]['geometry']))
        result1 = firstCoord['coordinates']

        try:
            secondCoord = (json.loads(result[i + int(config["pointdistance"])]['geometry']))
            result2 = secondCoord['coordinates']
        except IndexError:
            pass

        if result[i]['geometry'] is not None:
            coordinates = [
                result1,
                result2
            ]

            generateCoord = json.dumps({'type': 'Point', 'coordinates': coordinates})
            # If it's the first record, don't add a comma
            comma = "," if i > 0 else ""
            rowOutput = comma + '{"type": "Feature", "geometry": ' + str(generateCoord) + ', "properties": {'
            properties = ""

            j = 0
            comma = "," if j > 0 else ""
            properties += comma + '"' + "geom" + '":"' + str(result[i]['geom']) + '"'
            # j += 1

            rowOutput += properties + ', "lines":' + str(config['line']) + '}'
            rowOutput += '}'

            output += rowOutput

        # start over
        rowOutput = ""

        i += int(config["pointdistance"])

    # Assemble the GeoJSON
    totalOutput = '{ "type": "FeatureCollection", "features": [ ' + output + ' ]}'

    return totalOutput
