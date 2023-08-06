# wtu



## Intro

WTU gadget



## Setup

```shell
pip install wtu
```



## Token

To active this script, you need to get the 'JWT' authorization from WeChat App,

The token, expired after 7 days, you may replace and refresh it once a week



## Health Report

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from wtu import health_report
import schedule

JWT = ''
jk = health_report.JKClient(JWT)

def report():
    jk.health_report('student_number')
    
if __name__ == '__main__':
    schedule.every().day.at("00:10").do(report)
    
```
