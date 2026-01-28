# Blood Test Results

**Date**: {{document_date}}
**Provider**: {{provider}}
**Lab**: {{lab_name}}
**Patient**: Isaac

## Test Results

| Test | Value | Unit | Reference Range | Status |
|------|-------|------|-----------------|--------|
{{#each tests}}
| {{test_name}} | {{value}} | {{unit}} | {{reference_range}} | {{status}} |
{{/each}}

## Abnormal Values

{{#if abnormal_tests}}
{{#each abnormal_tests}}
- **{{test_name}}**: {{value}} {{unit}} (Reference: {{reference_range}}) - {{interpretation}}
{{/each}}
{{else}}
No abnormal values detected.
{{/if}}

## Summary

- **Total tests**: {{test_count}}
- **Abnormal results**: {{abnormal_count}}
- **Notable findings**: {{summary_notes}}

## Physician Notes

{{physician_notes}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: blood_exam v{{template_version}}*
