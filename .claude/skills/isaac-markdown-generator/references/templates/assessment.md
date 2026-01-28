# Developmental Assessment

**Date**: {{document_date}}
**Assessment Type**: {{assessment_type}}
**Evaluator**: {{evaluator}}
**Patient**: Isaac

## Assessment Information

- **Tool Used**: {{assessment_tool}}
- **Age at Assessment**: {{age_at_assessment}}
- **Location**: {{location}}

## Scores

{{#if domain_scores}}
| Domain | Score | Max Score | Percentile | Status |
|--------|-------|-----------|------------|--------|
{{#each domain_scores}}
| {{domain}} | {{score}} | {{max_score}} | {{percentile}} | {{status}} |
{{/each}}
{{/if}}

### Total Score

- **Raw Score**: {{total_score}}
- **Maximum Possible**: {{max_total}}
- **Percentile**: {{percentile}}
- **Classification**: {{classification}}

## Domain Details

{{#each domains}}
### {{domain_name}}

**Score**: {{score}} / {{max_score}}

**Items**:
{{#each items}}
- {{item}}: {{response}}
{{/each}}

**Notes**: {{notes}}

{{/each}}

## Behavioral Observations

{{behavioral_observations}}

## Comparison to Previous Assessments

{{#if previous_assessments}}
| Date | Total Score | Change |
|------|-------------|--------|
{{#each previous_assessments}}
| {{date}} | {{score}} | {{change}} |
{{/each}}
{{/if}}

## Interpretation

{{interpretation}}

## Recommendations

{{#each recommendations}}
- {{this}}
{{/each}}

## Evaluator Notes

{{evaluator_notes}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: assessment v{{template_version}}*
