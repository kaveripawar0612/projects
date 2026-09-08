import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

rng=np.random.default_rng(21); n=3000
amount=rng.lognormal(7,1,n); distance=rng.exponential(20,n); hour=rng.integers(0,24,n); velocity=rng.poisson(2,n)
score=.000002*amount+.018*distance+.5*(hour<5)+.35*(velocity>5)
y=(rng.random(n)<1/(1+np.exp(-(score-1.4)))*.08).astype(int)
X=np.column_stack([amount,distance,hour,velocity]); Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.25,stratify=y,random_state=42)
models={'Logistic Regression':LogisticRegression(max_iter=1000),'Random Forest':RandomForestClassifier(n_estimators=150,class_weight='balanced',random_state=42)}
for name,m in models.items():
    m.fit(Xtr,ytr); print('\n'+name); print(classification_report(yte,m.predict(Xte),zero_division=0))
