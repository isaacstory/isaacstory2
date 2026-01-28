# Exam Request

**Date**: {{document_date}}
**Requesting Physician**: {{requesting_physician}}
**Specialty**: {{specialty}}
**Patient**: Isaac

## Request Information

- **Request Type**: {{request_type}}
- **Priority**: {{priority}}
- **Valid Until**: {{valid_until}}

## Requested Exams

{{#each requested_exams}}
### {{exam_name}}

- **Category**: {{category}}
- **Code**: {{exam_code}}
- **Justification**: {{justification}}
{{#if special_instructions}}
- **Special Instructions**: {{special_instructions}}
{{/if}}

{{/each}}

## Clinical Indication

{{clinical_indication}}

## Patient Preparation

{{#if preparation_instructions}}
{{#each preparation_instructions}}
- {{this}}
{{/each}}
{{else}}
No special preparation required.
{{/if}}

## Physician Information

- **Name**: {{requesting_physician}}
- **CRM**: {{crm_number}}
- **Contact**: {{contact}}
- **Signature**: {{signature_status}}

## Administrative

- **Total Exams Requested**: {{exam_count}}
- **Authorization Status**: {{authorization_status}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: exam_request v{{template_version}}*
