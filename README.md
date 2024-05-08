# cine

SQLite database from IMDb Non-Commercial Datasets.

Cine builds a full, local SQLite3 database from the `Internet Movie
Database (IMDb) <https://imdb.com/>`_ dataset files.

https://developer.imdb.com/non-commercial-datasets/


They are made available by IMDB freely for non-commercial use. Download them from
`datasets.imdbws.com <https://datasets.imdbws.com/>`_. Documentaion and licensing
information is at `imdb.com/interfaces <https://www.imdb.com/interfaces/>`_

Download all of them in one shot using `wget`:

    $ wget -A gz -r -c -l 1 -nd -e robots=off https://datasets.imdbws.com/
