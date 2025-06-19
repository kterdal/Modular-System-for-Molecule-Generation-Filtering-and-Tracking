from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from registry.db import Molecule, SessionLocal, init_db

init_db()
app = FastAPI()

class MoleculeIn(BaseModel):
    smiles: str
    mw: float
    logp: float
    qed: float

@app.post("/molecules/", response_model=MoleculeIn)
def add_molecule(mol: MoleculeIn):
    db = SessionLocal()
    exists = db.query(Molecule).filter_by(smiles=mol.smiles).first()
    if exists:
        db.close()
        raise HTTPException(status_code=409, detail="Molecule already exists")
    m = Molecule(smiles=mol.smiles, mw=mol.mw, logp=mol.logp, qed=mol.qed)
    db.add(m)
    db.commit()
    db.refresh(m)
    db.close()
    return mol

@app.post("/molecules/bulk")
def add_bulk(mols: List[MoleculeIn]):
    db = SessionLocal()
    inserted = 0
    for mol in mols:
        if not db.query(Molecule).filter_by(smiles=mol.smiles).first():
            m = Molecule(smiles=mol.smiles, mw=mol.mw, logp=mol.logp, qed=mol.qed)
            db.add(m)
            inserted += 1
    db.commit()
    db.close()
    return {"inserted": inserted}

@app.get("/molecules/", response_model=List[MoleculeIn])
def list_molecules(limit: int = 100):
    db = SessionLocal()
    mols = db.query(Molecule).limit(limit).all()
    response = [MoleculeIn(smiles=m.smiles, mw=m.mw, logp=m.logp, qed=m.qed) for m in mols]
    db.close()
    return response