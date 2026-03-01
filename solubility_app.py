import streamlit as st
import pandas as pd
import pickle
from rdkit import Chem

import sys
import os

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(repo_root)

from featurizer import Featurizer

import pickle

model_path = os.path.join(repo_root, "svr_model.pkl")
with open(model_path, "rb") as f:
    model = pickle.load(f)

featurizer_path = os.path.join(repo_root, "featurizer.pkl")
with open(featurizer_path, "rb") as f:
    featurizer = pickle.load(f)

st.title('Solubility prediction app')
st.write('This is an app that predicts the solubility of compounds. Input the SMILES of the compound(s) you want to check in the textbox below.')
smiles_input = st.text_area('Enter SMILES (one per line)')

if st.button('Give me the prediction!'):
    smiles_list = [s.strip() for s in smiles_input.split("\n") if s.strip()]
    if not smiles_list:
        st.warning('Please enter SMILES')
        st.stop()
    else:
        valid_smiles = []
        invalid_smiles = []

        #Validate SMILES

        for smi in smiles_list:
            if Chem.MolFromSmiles(smi):
                valid_smiles.append(smi)
            else:
                invalid_smiles.append(smi)

        if invalid_smiles:
            st.warning(f"this SMILES is invalid!:\n{', '.join(invalid_smiles)}")

        if valid_smiles:
            try:
                features = featurizer.featurize(valid_smiles)
                predictions = model.predict(features)
                
                results_df = pd.DataFrame({
                    "SMILES": valid_smiles,
                    "Prediction": predictions
                })

                st.subheader("Solubility")
                st.table(results_df)

            except Exception as e:
                st.error(f"Error during prediction: {e}")
        else:
            st.warning("Invalid SMILES")


