"""Generate and score molecules, then send to API for registration."""
import random, requests, os
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors, QED

API_URL = os.getenv("API_URL", "http://localhost:8000")

SEED_SMILES = [
    "CC(=O)Oc1ccccc1C(=O)O",
    "C1CCC(CC1)NC(=O)C2=CC=CC=C2",
    "CCN(CC)CCCC(C)NC1=NC2=CC=CC=C2S1",
]

def mutate_smiles(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return smiles
    atom = random.choice(list(mol.GetAtoms()))
    atom.SetAtomicNum(random.choice([6,7,8,9,16]))
    return Chem.MolToSmiles(mol, canonical=True)

def generate(n_variants=10):
    variants=[]
    for seed in SEED_SMILES:
        for _ in range(n_variants):
            variants.append(mutate_smiles(seed))
    return variants

def score(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "smiles": smiles,
        "mw": Descriptors.MolWt(mol),
        "logp": Descriptors.MolLogP(mol),
        "qed": QED.qed(mol),
    }

def main():
    molecules = generate()
    payload = []
    for smi in molecules:
        s = score(smi)
        if s:
            payload.append(s)
    # bulk upload
    res = requests.post(f"{API_URL}/molecules/bulk", json=payload)
    print("Status:", res.status_code, res.text)

if __name__ == "__main__":
    main()