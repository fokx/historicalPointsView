import sqlite3

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import time
import pandas as pd
conn = sqlite3.connect('../sync_daemon/points.db')
# c = conn.cursor()
# Insert a row of data
# c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")
# Save (commit) the changes
# conn.commit()
# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
df = pd.read_sql_query("SELECT  * FROM point WHERE datetime(timestamp) >= datetime('now', '-3 hours')", conn)
conn.close()
df['timestamp'] = pd.to_datetime(df['timestamp'])
df['timestamp'] = df['timestamp'].dt.tz_localize('utc').dt.tz_convert('Asia/Hong_Kong')
exit(0)
