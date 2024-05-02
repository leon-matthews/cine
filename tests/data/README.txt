
While benchmarking, I started with a sample set 500MB, about 10% of the total, generated
using the following bash loop:

    $ for F in *; \
    do echo "$F";
    gzcat -d "$F" | head -n100000 | gzip --fast > "../samples/$F"; \
    done

The seven sample files total 12MB compressed and 34MB uncompressed.
