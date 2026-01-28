# Newborn Document

**Date**: {{document_date}}
**Document Type**: {{document_type}}
**Patient**: Isaac

## Birth Information

- **Birth Date**: {{birth_date}}
- **Hospital**: {{hospital}}
- **Gestational Age**: {{gestational_age}}

## Document Details

### {{document_title}}

{{content}}

## Measurements

{{#if measurements}}
| Parameter | Value | Unit | Status |
|-----------|-------|------|--------|
{{#each measurements}}
| {{parameter}} | {{value}} | {{unit}} | {{status}} |
{{/each}}
{{/if}}

## Screening Results

{{#if screening_results}}
| Test | Result | Reference | Status |
|------|--------|-----------|--------|
{{#each screening_results}}
| {{test}} | {{result}} | {{reference}} | {{status}} |
{{/each}}
{{/if}}

## Notes

{{notes}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: newborn v{{template_version}}*
