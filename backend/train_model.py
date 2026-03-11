import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

data = {
    "url_length":[20,75,60,18,90],
    "dots":[2,5,4,2,6],
    "hyphens":[0,1,1,0,2],
    "slashes":[2,4,5,2,6],
    "https":[1,0,0,1,0],
    "ip":[0,0,1,0,1],
    "suspicious":[0,2,3,0,4],
    "domain_length":[10,15,12,8,18],
    "label":[0,1,1,0,1]
}

df = pd.DataFrame(data)

X = df.drop("label",axis=1)
y = df["label"]

model = RandomForestClassifier()
model.fit(X,y)

joblib.dump(model,"model.pkl")

print("Model trained")
