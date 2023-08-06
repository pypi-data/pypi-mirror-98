# NextAPM

Monitor the python serverless functions deployed in vercel platform. You need https://nextapm.dev account to configure the monitor.

## Installation
Install agent module in your application
```
pip install nextapm
```

## Instrumentation
To monitor serverless api, import following module in all api files
```
// this should be in the first line
import nextapm;

from http.server import BaseHTTPRequestHandler
... your app code ...
````

## Configuration
Configure the following environment variables, you can get it from https://app.nextapm.dev after creating monitor

```
NEXTAPM_LICENSE_KEY
NEXTAPM_PROJECT_ID
```

## Restart/Redeploy
Restart/Redeploy your application and perform transactions