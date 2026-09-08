import numpy as np
import pandas as pd

rng=np.random.default_rng(42)
n=500
orders=pd.DataFrame({'customer_id':rng.integers(1000,1120,n),'order_value':rng.gamma(2.2,1800,n),'category':rng.choice(['Electronics','Fashion','Home','Beauty'],n),'date':pd.Timestamp('2025-01-01')+pd.to_timedelta(rng.integers(0,365,n),unit='D')})
summary=orders.groupby('customer_id').agg(orders=('customer_id','size'),revenue=('order_value','sum'),avg_order=('order_value','mean')).sort_values('revenue',ascending=False)
summary['segment']=pd.qcut(summary['revenue'],4,labels=['Low','Medium','High','VIP'])
print('\nTop customers:\n',summary.head(10))
print('\nCategory revenue:\n',orders.groupby('category')['order_value'].sum().sort_values(ascending=False))
summary.to_csv('customer_segments.csv')
