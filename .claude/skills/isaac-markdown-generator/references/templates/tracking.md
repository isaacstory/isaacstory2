# Tracking Document

**Date**: {{document_date}}
**Document Type**: {{document_type}}
**Patient**: Isaac

## Overview

- **Tracking Category**: {{category}}
- **Period**: {{period}}
- **Source**: {{source}}

## Data

{{#if table_data}}
### {{table_title}}

| {{#each headers}}{{this}} | {{/each}}
|{{#each headers}}------|{{/each}}
{{#each rows}}
| {{#each this}}{{this}} | {{/each}}
{{/each}}
{{/if}}

## Key Metrics

{{#if metrics}}
{{#each metrics}}
- **{{metric_name}}**: {{value}} {{unit}}
{{/each}}
{{/if}}

## Observations

{{observations}}

## Trends

{{trends}}

## Notes

{{notes}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: tracking v{{template_version}}*
