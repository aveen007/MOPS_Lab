from prometheus_client import Counter, Histogram

REQUESTS_TOTAL = Counter('requests_total', 'Total number of requests sent to the controller', ['status'])
REQUESTS_DURATION=Histogram('requests_duration_seconds','Histogram for the duration of the requests',buckets=[1,2,5,6,10,float("inf")])