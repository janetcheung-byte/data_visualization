# How to run the dashboard
# 1)Execute Panel dashboard using servable function

```python

dashboard.servable()

```

# 2) Activate a terminal from Jupyter Lab or Git Bash terminal




# 3) Enter command Panel Serve (file name)

```python

Panel Serve dashboard.ipynb

```
# The output has a web address

```python

$ panel serve dashboard.ipynb
2019-12-01 00:23:10,032 Starting Bokeh server version 1.2.0 (running on Tornado 6.0.3)
2019-12-01 00:23:10,038 Bokeh app running at: http://localhost:5006/dashboard
2019-12-01 00:23:10,038 Starting Bokeh server with process id: 9772

```

## Output web address is http://localhost:5006/dashboard

## This link will open up a web page with the dashboard

---

# This dashboard presents a visual analysis of historical prices of house units, sale price per square foot and gross rent in San Francisco, California from 2010 to 2016. You can navigate through the tabs above to explore more details about the evolution of the real estate market on The Golden City across these years