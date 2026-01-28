# Specialty Examination

**Date**: {{document_date}}
**Specialist**: {{specialist}}
**Specialty**: {{specialty}}
**Patient**: Isaac

## Examination Type

- **Exam Name**: {{exam_name}}
- **Indication**: {{indication}}
- **Location**: {{location}}

## Clinical History

{{clinical_history}}

## Examination Findings

{{#each exam_sections}}
### {{section_name}}

{{findings}}

{{/each}}

## Measurements

{{#if measurements}}
| Parameter | Value | Unit | Reference | Status |
|-----------|-------|------|-----------|--------|
{{#each measurements}}
| {{parameter}} | {{value}} | {{unit}} | {{reference}} | {{status}} |
{{/each}}
{{/if}}

## Diagnosis/Impression

{{diagnosis}}

## Recommendations

{{#each recommendations}}
- {{this}}
{{/each}}

## Follow-up

{{follow_up}}

## Specialist Information

- **Name**: {{specialist}}
- **CRM**: {{crm_number}}
- **Specialty**: {{specialty}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: specialty_exam v{{template_version}}*
