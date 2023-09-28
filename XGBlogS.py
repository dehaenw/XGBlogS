from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from xgboost import XGBRegressor


mfpgen = rdFingerprintGenerator.GetMorganGenerator(radius=3,fpSize=4096)

try:
    rgr=XGBRegressor()
    rgr.load_model("logSmodel.model")
except:
    print("NOT ABLE to load logSmodel.model!!!!")

def mols2logS(mols):
    x_in=[mfpgen.GetCountFingerprint(m) for m in mols]
    x_in=[[int(bit) for bit in fp] for fp in x_in]
    return rgr.predict(x_in)

if __name__ == "__main__":
    mols = [Chem.MolFromSmiles(smi) for smi in ["C(CCCC)CC(C)CC","OCCc1ccc(F)cc1"]]
    print(mols2logS(mols))
