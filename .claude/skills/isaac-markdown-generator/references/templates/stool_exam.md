# Stool/GI Exam Results

**Date**: {{document_date}}
**Lab**: {{lab_name}}
**Test Type**: {{test_type}}
**Patient**: Isaac

## Sample Information

- **Collection Date**: {{collection_date}}
- **Sample Type**: {{sample_type}}
- **Test Method**: {{test_method}}

## Results

### Macroscopic Analysis
{{#if macroscopic}}
| Parameter | Result | Reference |
|-----------|--------|-----------|
{{#each macroscopic}}
| {{parameter}} | {{result}} | {{reference}} |
{{/each}}
{{/if}}

### Microscopic Analysis
{{#if microscopic}}
| Element | Result | Reference | Status |
|---------|--------|-----------|--------|
{{#each microscopic}}
| {{element}} | {{result}} | {{reference}} | {{status}} |
{{/each}}
{{/if}}

### Parasitology
{{#if parasitology}}
| Parasite/Test | Result | Method |
|---------------|--------|--------|
{{#each parasitology}}
| {{test}} | {{result}} | {{method}} |
{{/each}}
{{/if}}

### Microbiological Culture
{{#if culture}}
| Organism | Result | Notes |
|----------|--------|-------|
{{#each culture}}
| {{organism}} | {{result}} | {{notes}} |
{{/each}}
{{/if}}

### Biochemical Markers
{{#if biochemical}}
| Marker | Value | Unit | Reference | Status |
|--------|-------|------|-----------|--------|
{{#each biochemical}}
| {{marker}} | {{value}} | {{unit}} | {{reference}} | {{status}} |
{{/each}}
{{/if}}

## Abnormal Findings

{{#if abnormal_findings}}
{{#each abnormal_findings}}
- **{{finding}}**: {{details}}
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
*Template: stool_exam v{{template_version}}*
