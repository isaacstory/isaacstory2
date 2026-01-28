# Genetic Test Report

**Date**: {{document_date}}
**Laboratory**: {{lab_name}}
**Test Type**: {{test_type}}
**Patient**: Isaac

## Test Information

- **Test Name**: {{test_name}}
- **Methodology**: {{methodology}}
- **Sample Type**: {{sample_type}}
- **Ordering Physician**: {{ordering_physician}}

## Genetic Variants

{{#if variants}}
### Pathogenic/Likely Pathogenic Variants

| Gene | Variant | Classification | Inheritance | Associated Condition |
|------|---------|----------------|-------------|---------------------|
{{#each pathogenic_variants}}
| {{gene}} | {{variant}} | {{classification}} | {{inheritance}} | {{condition}} |
{{/each}}

### Variants of Uncertain Significance (VUS)

| Gene | Variant | Notes |
|------|---------|-------|
{{#each vus_variants}}
| {{gene}} | {{variant}} | {{notes}} |
{{/each}}

{{else}}
No significant variants detected.
{{/if}}

## Pharmacogenomics (PGx)

{{#if pgx_results}}
| Gene | Genotype | Phenotype | Drug Implications |
|------|----------|-----------|-------------------|
{{#each pgx_results}}
| {{gene}} | {{genotype}} | {{phenotype}} | {{drug_implications}} |
{{/each}}
{{/if}}

## Copy Number Variants (CNV)

{{#if cnv_results}}
| Region | Type | Size | Clinical Significance |
|--------|------|------|----------------------|
{{#each cnv_results}}
| {{region}} | {{type}} | {{size}} | {{significance}} |
{{/each}}
{{/if}}

## Clinical Interpretation

{{clinical_interpretation}}

## Recommendations

{{recommendations}}

## Summary

- **Total variants analyzed**: {{total_variants}}
- **Pathogenic variants**: {{pathogenic_count}}
- **VUS**: {{vus_count}}
- **CNVs detected**: {{cnv_count}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: genetic_report v{{template_version}}*
