# Prescription

**Date**: {{document_date}}
**Prescriber**: {{prescriber}}
**Specialty**: {{specialty}}
**Patient**: Isaac

## Medications

{{#each medications}}
### {{medication_name}}

- **Dosage**: {{dosage}}
- **Form**: {{form}}
- **Frequency**: {{frequency}}
- **Duration**: {{duration}}
- **Instructions**: {{instructions}}
{{#if components}}
- **Components**:
{{#each components}}
  - {{this}}
{{/each}}
{{/if}}
{{#if notes}}
- **Notes**: {{notes}}
{{/if}}

{{/each}}

## Prescription Summary

- **Total medications**: {{medication_count}}
- **Prescription type**: {{prescription_type}}
- **Renewal date**: {{renewal_date}}

## Special Instructions

{{special_instructions}}

## Prescriber Information

- **Name**: {{prescriber}}
- **CRM**: {{crm_number}}
- **Contact**: {{contact}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: prescription v{{template_version}}*
