# Target Folder Structure

```
isaacstory2/
├── Exams/
│   ├── Blood/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Stool_GI/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Urine/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Genetic/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Imaging/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Metabolic_GreatPlains/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Specialty/
│   │   └── YYYYMMDD_Provider_Description.ext
│   ├── Assessments/
│   │   └── YYYYMMDD_Provider_Description.ext
│   └── Requests/
│       └── YYYYMMDD_Provider_Description.ext
│
├── Prescriptions/
│   ├── Medications/
│   │   └── YYYYMMDD_Provider_Description.ext
│   └── Nutrition/
│       └── YYYYMMDD_Provider_Description.ext
│
├── Consultations/
│   └── YYYYMMDD_Provider_Description.ext
│
├── Tracking/
│   └── YYYYMMDD_Description.ext (or YYYY_Description.ext for annual docs)
│
├── Newborn/
│   └── YYYYMM_Description.ext
│
├── _duplicates/
│   └── (files detected as duplicates, pending manual deletion)
│
├── dropbasket/
│   └── (incoming files to be processed)
│
└── inventory.json
```

## Filename Format

Standard: `YYYYMMDD_Provider_Description.ext`

Examples:
- `20230914_OswaldoCruz_Hemograma.pdf`
- `20210109_GreatPlains_IgG_1.pdf`
- `20240610_OswaldoCruz_TNFalfa.pdf`
- `20220514_DrRogerio_Prescricao_Medicamentos.pdf`
- `20210803_MonicaCooke_PlanoAlimentar.pdf`

## Date Extraction Rules

1. **From filename**: Extract YYYYMMDD or YYYYMM from start of filename
2. **From document**: If filename has no date, read document to find date
3. **Fallback**: Use file modification date if no other date available

## Handling Duplicates

When a file hash matches an existing inventory entry:
1. Move to `_duplicates/` folder
2. Keep original filename
3. Log: `Duplicate of: {destination path}`
