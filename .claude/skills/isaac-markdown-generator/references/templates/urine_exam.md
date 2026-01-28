# Urine Analysis Results

**Date**: {{document_date}}
**Lab**: {{lab_name}}
**Test Type**: {{test_type}}
**Patient**: Isaac

## Sample Information

- **Collection Date**: {{collection_date}}
- **Collection Time**: {{collection_time}}
- **Sample Type**: {{sample_type}}

## Physical Examination

| Parameter | Result | Reference |
|-----------|--------|-----------|
| Color | {{color}} | Yellow |
| Appearance | {{appearance}} | Clear |
| Specific Gravity | {{specific_gravity}} | 1.005-1.030 |
| pH | {{ph}} | 4.5-8.0 |

## Chemical Analysis

| Component | Result | Reference | Status |
|-----------|--------|-----------|--------|
{{#each chemical_analysis}}
| {{component}} | {{result}} | {{reference}} | {{status}} |
{{/each}}

## Microscopic Examination

| Element | Result | Reference | Status |
|---------|--------|-----------|--------|
{{#each microscopic}}
| {{element}} | {{result}} | {{reference}} | {{status}} |
{{/each}}

## Abnormal Findings

{{#if abnormal_findings}}
{{#each abnormal_findings}}
- **{{finding}}**: {{interpretation}}
{{/each}}
{{else}}
No significant abnormalities detected.
{{/if}}

## Interpretation

{{interpretation}}

## Recommendations

{{recommendations}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: urine_exam v{{template_version}}*
