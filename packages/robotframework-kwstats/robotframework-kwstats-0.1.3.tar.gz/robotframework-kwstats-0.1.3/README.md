# robotframework-kwstats

[![PyPI version](https://badge.fury.io/py/robotframework-kwstats.svg)](https://badge.fury.io/py/robotframework-kwstats)
[![Downloads](https://pepy.tech/badge/robotframework-kwstats)](https://pepy.tech/project/robotframework-kwstats)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)]()
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)]()
[![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)]()

Robotframework keyword statistics is custom report which provides detailed information about keyword in project like

 - No. of times keyword used (count)
 - Pass Percentage (no. of times keyword passed)
 - Duration (min, max, average and total)

---

### How it works:

 - Parse output.xml using ResultVisitor API
 - Group results using pands
 - Generate HTML report using beautifulsoup

---

### How to Use:

 __Step 1__ Install library

 ```
 pip install robotframework-kwstats
 ```

 __Step 2__ Execute robotkwstats command to generate report

 ```
 robotkwstats --output output1.xml -M kwstats.html
 ```
> For more info use:

```
robotkwstats --help
```

---

### Sample Report

<img src="https://i.ibb.co/bLx9cVJ/Keyword-Statistics.png" alt="Keyword-Statistics" border="0">

---

If you have any questions / suggestions / comments on the report, please feel free to reach me at

 - Email: <a href="mailto:adiralashiva8@gmail.com?Subject=Robotframework%20Kw%20Stats" target="_blank">`adiralashiva8@gmail.com`</a> 

---

:star: repo if you like it

---