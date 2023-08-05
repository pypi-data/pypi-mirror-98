#  Performence logger

A very handy performance logging tool， useful for training deep neural networks.  

# Install
```
pip install perf-logger
```

# Usage 
```
from perf_logger import PerfLogger
logger = PerfLogger(prefix='your_program')
msg = 'iter: {}, loss: {}, acc: {}'.format(0,100,0)
logger.log_str(msg,stdout=True)

```
A log file will be found in /home/<user>/.perf_logger/<your_program>/


# Example

2020-03-05 00:39:21 nLoss 0.0477,advlooss 0.245,dLoss 1.05,dAcc 0.498

2020-03-05 00:40:38 nLoss 0.00401,advlooss 0.226,dLoss 0.98,dAcc 0.499

2020-03-05 00:41:55 nLoss 0.00324,advlooss 0.222,dLoss 0.918,dAcc 0.5

2020-03-05 00:43:12 nLoss 0.00297,advlooss 0.219,dLoss 0.873,dAcc 0.5

2020-03-05 00:44:29 nLoss 0.00282,advlooss 0.214,dLoss 0.837,dAcc 0.5

2020-03-05 00:45:46 nLoss 0.00273,advlooss 0.208,dLoss 0.808,dAcc 0.5

2020-03-05 00:47:03 nLoss 0.00266,advlooss 0.202,dLoss 0.783,dAcc 0.5

2020-03-05 00:48:20 nLoss 0.0026,advlooss 0.197,dLoss 0.761,dAcc 0.5

2020-03-05 00:49:37 nLoss 0.00255,advlooss 0.192,dLoss 0.743,dAcc 0.5

2020-03-05 00:51:00 nLoss 0.00163,advlooss 0.137,dLoss 0.602,dAcc 0.5





