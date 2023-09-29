from rdkit import Chem
from rdkit.Chem import Descriptors
from xgboost import XGBRegressor



try:
    rgr=XGBRegressor()
    rgr.load_model("logSmodel.model")
except:
    print("NOT ABLE to load logSmodel.model!!!!")

def mols2logS(mols):
    x_in=[list(Descriptors.CalcMolDescriptors(m).values()) for m in mols]
    return rgr.predict(x_in)

if __name__ == "__main__":
    mols = [Chem.MolFromSmiles(smi) for smi in ["C(CCCC)CC(C)CC","OCCc1ccc(F)cc1"]]
    print(mols2logS(mols))
