# Metabolic Panel - Great Plains Laboratory

**Date**: {{document_date}}
**Lab**: Great Plains Laboratory
**Test Type**: {{test_type}}
**Patient**: Isaac

## Overview

- **Panel**: {{panel_name}}
- **Sample Type**: {{sample_type}}
- **Collection Date**: {{collection_date}}
- **Report Date**: {{report_date}}

## Metabolic Markers

### Organic Acids
{{#if organic_acids}}
| Marker | Value | Reference | Status | Interpretation |
|--------|-------|-----------|--------|----------------|
{{#each organic_acids}}
| {{marker_name}} | {{value}} | {{reference}} | {{status}} | {{interpretation}} |
{{/each}}
{{/if}}

### Microbial Markers
{{#if microbial_markers}}
| Marker | Value | Reference | Status | Indication |
|--------|-------|-----------|--------|------------|
{{#each microbial_markers}}
| {{marker_name}} | {{value}} | {{reference}} | {{status}} | {{indication}} |
{{/each}}
{{/if}}

### Nutritional Markers
{{#if nutritional_markers}}
| Marker | Value | Reference | Status | Deficiency/Excess |
|--------|-------|-----------|--------|-------------------|
{{#each nutritional_markers}}
| {{marker_name}} | {{value}} | {{reference}} | {{status}} | {{interpretation}} |
{{/each}}
{{/if}}

### Neurotransmitter Metabolites
{{#if neurotransmitter_markers}}
| Marker | Value | Reference | Status | Notes |
|--------|-------|-----------|--------|-------|
{{#each neurotransmitter_markers}}
| {{marker_name}} | {{value}} | {{reference}} | {{status}} | {{notes}} |
{{/each}}
{{/if}}

## Abnormal Findings

{{#if abnormal_markers}}
{{#each abnormal_markers}}
### {{marker_name}}
- **Value**: {{value}} (Reference: {{reference}})
- **Status**: {{status}}
- **Clinical Significance**: {{clinical_significance}}
- **Recommendations**: {{recommendations}}

{{/each}}
{{else}}
No significant abnormalities detected.
{{/if}}

## Summary & Recommendations

{{summary}}

### Dietary Recommendations
{{dietary_recommendations}}

### Supplement Recommendations
{{supplement_recommendations}}

## Notes

{{notes}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: metabolic_panel v{{template_version}}*
