from rdkit import Chem
from rdkit.Chem import Draw

# Dictionary mapping REFCODE to SMILES
refcode_smiles = {
    'VENYUI': 'O=C1C2C3C2C(=O)C2C1C2C3=O',
    'FECKIK': 'C1N=NC2C1CN1C2=Nc2ccccc12',
    'WOCGOK': 'O=C1OCCCN2C=C3CC1CCC3=N2',
    'BOQQUT': 'O=C1OC2C3CC4(C5CCC(C5)C4=C3)C2O1',
    'BUHMOH': 'O=C1OC2CCCCC34OC3CC=C1C24',
    'GOCWEA': 'C1Cc2ccccc2N2N=NN=C2C1',
    'FOCNIU': 'O=C1CC2OCC3CCOC2(O3)C=C1',
    'NAHFOR': 'C1OCC23OC(C=C2)C2(CC2)C23CC12',
    'PHTHAO': 'Fc1ccc2C3=C(CCCC3)Nc2c1',
    'TOHZUL': 'O=C1ON=C2COc3ccccc3C=C12',
    'ADPRLA': 'O=C1CCN2C=Nc3ncnc(N1)c23',
    'BUKLOK': 'C1C2=CC=CC=C1C=C1CC(=C2)C=CC=N1',
    'GILXAD': 'O=C1CCCC2=C1c1ccccc1CN2',
    'KEJYOP': 'O=C1Oc2ccccc2C2C=CCCC12',
    'TANMAT': 'O=C1CCc2ccc3OCCCCc3c12',
    'BEXGAM': 'O=C1C2CC3CCC41CCC1CC1C34O2',
    'DIHIXL': 'O=C1C2CCC=CC2OC21CCCCO2',
    'GILXUX': 'C1Nc2ccccc2CN2C=CC=C12',
    'ZZZRNY': 'N1c2ccccc2c2ccncc12',
    'ZUMKUN': 'O=C1C2CCC31CCCCC13OC2C=C1',
    'BOFWEZ': 'C=C1CCC2CC1C1COC(=O)N1C2',
    'DIJDAE': 'O=C1COc2ccccc2C2=C1CCO2',
    'BZCOCT': 'c1ccc2C3C(C4C3c3ccccc43)c2c1',
    'BEVCEK': 'O=C1OC2CC3COC4OCC1C2C34',
    'VIGTUA': 'c1ccc2nc3C4C5C4C5c3nc2c1'
}

# Convert SMILES to molecules and filter out invalid ones
molecules = []
legends = []
for refcode, smiles in refcode_smiles.items():
    mol = Chem.MolFromSmiles(smiles)
    if mol is not None:
        molecules.append(mol)
        legends.append(refcode)
    else:
        print(f"Warning: Could not parse SMILES for {refcode}: {smiles}")

# Check if we have any valid molecules
if not molecules:
    print("Error: No valid molecules could be parsed from the SMILES strings")
    exit()

# Generate the grid image
try:
    # Using subImgSize to make the images larger (adjust as needed)
    image = Draw.MolsToGridImage(
        molecules,
        molsPerRow=9,  # 4 molecules per row
        subImgSize=(300, 300),  # Size of each molecule image
        legends=legends,  # Using REFCODE as captions
        legendFontSize=20  # Font size for the REFCODE captions
    )
    
    # Save the image
    image.save('chemical_grid_with_names.png')
    print("Successfully created chemical_grid_with_names.png")
    
except Exception as e:
    print(f"Error generating image: {str(e)}")