
import pandas as pd
import json

def convertir_csv_en_json(csv_path, json_path):
    df = pd.read_csv(csv_path)

    lexique = []
    for _, row in df.iterrows():
        entree = {
            "mot": row.get("mot", ""),
            "lemme": row.get("mot", ""),
            "prononciation": row.get("prononciation", ""),
            "catégorie": row.get("catégorie", ""),
            "traits": {},  # à enrichir manuellement ou par NLP plus avancé
            "traduction_fr": row.get("traduction_fr", ""),
            "exemple": {
                "source": row.get("exemple", ""),
                "traduction": ""  # à ajouter manuellement
            },
            "variante": row.get("variante", "")
        }
        lexique.append(entree)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(lexique, f, ensure_ascii=False, indent=2)

# Exemple d’utilisation :
# convertir_csv_en_json("lexique_mina.csv", "lexique_mina_annoté.json")
