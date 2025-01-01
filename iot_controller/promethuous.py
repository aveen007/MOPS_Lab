from prometheus_client import Counter

REQUESTS = Counter('requests_total', 'Total number of requests sent to the controller')
REQUESTS_DECLINED = Counter('declined_total', 'Total number of declined batches, where age < 21')
REQUESTS_ACCEPTED = Counter('accepted_total', 'Total number of accepted batches, where age >= 21')