import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

rng=np.random.default_rng(10)
n=1200
age=rng.integers(18,70,n); tenure=rng.integers(1,72,n); monthly=rng.uniform(300,6000,n); support=rng.poisson(2,n)
logit=-1.4-0.025*tenure+0.00015*monthly+0.35*support+0.012*(40-age)
prob=1/(1+np.exp(-logit)); y=(rng.random(n)<prob).astype(int)
X=np.column_stack([age,tenure,monthly,support])
Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,stratify=y,random_state=42)
model=make_pipeline(StandardScaler(),LogisticRegression(max_iter=1000)).fit(Xtr,ytr)
pred=model.predict(Xte)
print(classification_report(yte,pred)); print('Confusion matrix:\n',confusion_matrix(yte,pred))
