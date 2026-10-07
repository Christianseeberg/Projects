# Student: Christian Bjørklund Seeberg
#INF 201 Week 39 Assignment



from pathlib import Path
import pandas as pd


SCRIPT_DIR = Path(__file__).parent
PROJECTS_DIR = SCRIPT_DIR.parent
DATA_DIR = PROJECTS_DIR / "data"


def make_unique_id(study_id: str, patient_id) -> str:
 
  return f"{study_id}_p{int(patient_id):04d}"

# Task 1

def process_clinical_data(csv_file: Path, output_root: Path) -> None:
  
  output_root.mkdir(parents=True, exist_ok=True)

  df = pd.read_csv(csv_file)

  # Converting data
  df["surgery_date"] = pd.to_datetime(df["surgery_date"])
  df["psa_date"] = pd.to_datetime(df["psa_date"])
  df["date_of_birth"] = pd.to_datetime(df["date_of_birth"])

  # Unique id
  df["unique_id"] = df.apply(
      lambda row: make_unique_id(row["study_id"], row["patient_id"]), axis=1
  )

  
  for study_id, study_group in df.groupby("study_id"):
    study_dir = output_root / study_id
    study_dir.mkdir(parents=True, exist_ok=True)

    summary_rows = []

    
    for unique_id, patient_group in study_group.groupby("unique_id"):
      patient_dir = study_dir / unique_id
      patient_dir.mkdir(parents=True, exist_ok=True)

      patient_records = patient_group.sort_values("psa_date")
      
      patient_csv_path = patient_dir / f"{unique_id}.csv"
      patient_records.to_csv(patient_csv_path, index=False)


      surgery_date = patient_records["surgery_date"].iloc[0]
      latest_psa_date = patient_records["psa_date"].max()
      dob = patient_records["date_of_birth"].iloc[0]

      follow_up_days = (latest_psa_date - surgery_date).days
      num_psa = len(patient_records)

      relative_folder_path = f"{study_id}/{unique_id}"

      summary_rows.append({
          "unique_id": unique_id,
          "date_of_birth": dob.strftime("%Y-%m-%d"),
          "surgery_date": surgery_date.strftime("%Y-%m-%d"),
          "follow_up_days": follow_up_days,
          "number_of_psa_measurements": num_psa,
          "patient_folder_path": relative_folder_path,
      })

    # Summary file
    summary_df = pd.DataFrame(summary_rows).sort_values("unique_id")
    summary_csv_path = study_dir / f"{study_id}_summary.csv"
    summary_df.to_csv(summary_csv_path, index=False)

  print("Task 1 complete")

# Task 2

def parse_sequencing_header(file_path: Path) -> dict:
  
  metadata = {}
  with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
    for line in f:
      if not line.startswith("##"):
        break  
      clean_line = line.lstrip("#").strip()
      if "=" in clean_line:
        key, val = clean_line.split("=", 1)
        metadata[key.strip()] = val.strip()
  return metadata

def create_sequencing_manifest(seq_folder: Path, output_root: Path) -> None:
 
  manifest_rows = []

  for seq_file in seq_folder.iterdir():
    if seq_file.is_file():
      header = parse_sequencing_header(seq_file)
      if "study_id" in header and "patient_id" in header:
        study_id = header["study_id"]
        patient_id = header["patient_id"]
        unique_id = make_unique_id(study_id, patient_id)

        manifest_rows.append({
            "unique_id": unique_id,
            "study_id": study_id,
            "patient_id": patient_id,
            "sequencing_file_path": f"{seq_folder.name}/{seq_file.name}",
        })

  if manifest_rows:
    manifest_df = pd.DataFrame(manifest_rows).sort_values("unique_id")
    manifest_path = output_root / "sequencing_manifest.csv"
    manifest_df.to_csv(manifest_path, index=False)
    print("Task 2 complete")

# main program
if __name__ == "__main__":
  clinical_csv = DATA_DIR / "psa_clinical_data.csv"
  seq_dir = DATA_DIR / "raw_sequencing_data"
  project_root = SCRIPT_DIR / "project_root"

 
  if clinical_csv.exists():
    process_clinical_data(csv_file=clinical_csv, output_root=project_root)
  else:
    print(f"Feil: Finner ikke klinisk CSV-fil på: {clinical_csv}")

  
  if seq_dir.exists():
    create_sequencing_manifest(seq_folder=seq_dir, output_root=project_root)
  else:
    print(
        f"Mappe for sekvensering finnes ikke på: {seq_dir} (Kjører kun Oppgave"
        " 1)"
    )
