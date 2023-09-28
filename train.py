import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from xgboost import XGBRegressor
from sklearn.metrics import r2_score,mean_squared_error

"""
you need to download logs.txt from 
https://vcclab.org/lab/alogps/logs.txt
to be able to train the model
"""
if __name__=="__main__":
    mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=3,fpSize=4096)
    rgr=XGBRegressor()
    try:
        print("loading and processing data")
        df=pd.read_csv("logs.txt",sep=" ",nrows=1311,header=None) #1311 to not have postscript
    except:
        print("you didnt download the correct logs.txt probably. go to https://vcclab.org/lab/alogps/logs.txt")
    df.columns = ["CAS","smiles","logS"]
    df['mfp']=[mfpgen.GetCountFingerprint(Chem.MolFromSmiles(smi)) for smi in df['smiles']]
    df['mfp']=[[int(bit) for bit in fp] for i,fp in enumerate(df['mfp'])] #xgboost doesnt like rdkit intvect
    #split data according to literature
    y_train=list(df['logS'].head(878))
    y_test=list(df['logS'].tail(433))
    X_train=list(df['mfp'].head(878))
    X_test=list(df['mfp'].tail(433))
    #hyperparms obtained by grid search
    print("training xgboost model")
    rgr=XGBRegressor(tree_method="hist",max_depth=7,learning_rate=0.1,subsample=0.5,n_estimators=500,eval_metric=r2_score,random_state=0)
    rgr.fit(X_train,y_train)
    y_pred=rgr.predict(X_test)
    print("r2 of test set is",r2_score(y_test,y_pred))
    print("rmse of test set is",mean_squared_error(y_test,y_pred,squared=False))
    rgr.save_model("logSmodel.model")
