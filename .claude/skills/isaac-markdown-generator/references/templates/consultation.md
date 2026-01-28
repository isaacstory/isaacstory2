# Consultation Report

**Date**: {{document_date}}
**Provider**: {{provider}}
**Specialty**: {{specialty}}
**Patient**: Isaac

## Visit Information

- **Visit Type**: {{visit_type}}
- **Referring Physician**: {{referring_physician}}
- **Location**: {{location}}

## Chief Complaint

{{chief_complaint}}

## History of Present Illness

{{history_present_illness}}

## Physical Examination

{{#each exam_findings}}
### {{system}}
{{findings}}

{{/each}}

## Assessment

{{assessment}}

## Diagnoses

{{#each diagnoses}}
- {{diagnosis}} {{#if icd_code}}({{icd_code}}){{/if}}
{{/each}}

## Plan

{{#each plan_items}}
- {{this}}
{{/each}}

## Medications

{{#if medications}}
| Medication | Dosage | Instructions |
|------------|--------|--------------|
{{#each medications}}
| {{name}} | {{dosage}} | {{instructions}} |
{{/each}}
{{/if}}

## Follow-up

{{follow_up}}

## Provider Information

- **Name**: {{provider}}
- **CRM**: {{crm_number}}
- **Contact**: {{contact}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: consultation v{{template_version}}*
