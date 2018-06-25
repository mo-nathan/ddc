# Common Log Format Parser

## To run using Docker:

- The script works with Docker by running the commands:
```
sudo docker build -t datadog-challenge:0.1 .
sudo docker run datadog-challenge:0.1
```
NOTE: Without any changes to the Dockerfile, this will generate a
report every 10 seconds, but it will never have anything to say since
/var/log/access.log on the container is not directly accessible.


## To run using make:

- Ensure that GNU-make (usually just `make`) is installed on your
system.  Most UNIX based systems have this installed by default or
there should be a convenient package available for getting it.

- Run `make run LOG=log_parser/tests/data/example.data` to start the
process using the log data in `log_parser/tests/data/example.data`.
`make run` will try to use the default log (/var/log/access.log).

- You can override the defaults using different make variables.
  - LOG - sets the path to the log file (default=/var/log/access.log)
  - THRESHOLD - sets traffic rate which triggers traffic alerts (default=10)
  - WINDOW - sets window for traffic alerts (default=120)
  - INTERVAL - sets sleep internal between reports (default=10)
  - REFERER_EXPECTED - if non-zero, require referer and user-agent (default=0)

- Run `make test` to run the tests.

- Run `make code-check` to run pycodestyle over the code.

- Run `make help` for to see any additional targets.


## Original Spec:

Consume an actively written-to w3c-formatted HTTP access log
(https://en.wikipedia.org/wiki/Common_Log_Format). It should default
to reading /var/log/access.log and be overridable.  Example log lines:

```
127.0.0.1 - james [09/May/2018:16:00:39 +0000] "GET /report HTTP/1.0" 200 1234

127.0.0.1 - jill [09/May/2018:16:00:41 +0000] "GET /api/user HTTP/1.0" 200 1234

127.0.0.1 - frank [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234

127.0.0.1 - mary [09/May/2018:16:00:42 +0000] "GET /api/user HTTP/1.0" 200 1234
```

Display stats every 10s about the traffic during those 10s: the
sections of the web site with the most hits, as well as interesting
summary statistics on the traffic as a whole. A section is defined as
being what's before the second '/' in the path. For example, the
section for "http://my.site.com/pages/create” is
"http://my.site.com/pages".

Make sure a user can keep the app running and monitor the log file
continuously Whenever total traffic for the past 2 minutes exceeds a
certain number on average, add a message saying that “High traffic
generated an alert - hits = {value}, triggered at {time}”. The default
threshold should be 10 requests per second and should be overridable.

Whenever the total traffic drops again below that value on average for
the past 2 minutes, print or displays another message detailing when
the alert recovered.  Write a test for the alerting logic.  Explain
how you’d improve on this application design.  If you have access to a
linux docker environment, we'd love to be able to docker build and run
your project! If you don't though, don't sweat it. As an example:
 
```
FROM python:3

RUN touch /var/log/access.log # since the program will read this by default

WORKDIR /usr/src

ADD . /usr/src

ENTRYPOINT ["python", "main.py"]
```

and we'll have something else write to that log file.


## Suggested Improvements

Functional Improvements:
- Review output with potential users to improve readability
- More detail on the errors from the log files
- Allow the log file to handle log rotation gracefully
- Stats on the client, user, method and protocol
- Stats on referer and user-agent for logs with those fields
- Make which stats are reported configurable
- Expose code to more types of data to make it more bullet proof
- Allow users to track specific URLs or parts of URLs (expand "section" idea)

Code Improvements:
- Generalize the stats accumulation process
- Not really happy with the way the log time reporting is handled
