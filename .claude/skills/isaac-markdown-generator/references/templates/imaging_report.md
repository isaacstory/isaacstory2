# Imaging Report

**Date**: {{document_date}}
**Facility**: {{facility}}
**Modality**: {{modality}}
**Patient**: Isaac

## Exam Information

- **Exam Type**: {{exam_type}}
- **Body Region**: {{body_region}}
- **Technique**: {{technique}}
- **Contrast**: {{contrast_used}}
- **Ordering Physician**: {{ordering_physician}}

## Clinical Indication

{{clinical_indication}}

## Findings

{{#each findings}}
### {{region}}
{{description}}

{{/each}}

## Measurements

{{#if measurements}}
| Structure | Measurement | Normal Range | Status |
|-----------|-------------|--------------|--------|
{{#each measurements}}
| {{structure}} | {{measurement}} | {{normal_range}} | {{status}} |
{{/each}}
{{/if}}

## Impression

{{impression}}

## Recommendations

{{recommendations}}

## Radiologist

- **Name**: {{radiologist_name}}
- **CRM**: {{crm_number}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: imaging_report v{{template_version}}*
