# Nutrition Plan

**Date**: {{document_date}}
**Nutritionist**: {{nutritionist}}
**Plan Type**: {{plan_type}}
**Patient**: Isaac

## Diet Overview

- **Diet Type**: {{diet_type}}
- **Caloric Target**: {{caloric_target}}
- **Special Considerations**: {{special_considerations}}

## Allowed Foods

{{#each food_categories}}
### {{category_name}}
{{#each foods}}
- {{this}}
{{/each}}

{{/each}}

## Restricted Foods

{{#each restricted_foods}}
### {{category_name}}
{{#each foods}}
- {{food}} {{#if reason}}({{reason}}){{/if}}
{{/each}}

{{/each}}

## Meal Plan

### Breakfast
{{breakfast}}

### Morning Snack
{{morning_snack}}

### Lunch
{{lunch}}

### Afternoon Snack
{{afternoon_snack}}

### Dinner
{{dinner}}

## Supplements

{{#if supplements}}
| Supplement | Dosage | Timing | Notes |
|------------|--------|--------|-------|
{{#each supplements}}
| {{name}} | {{dosage}} | {{timing}} | {{notes}} |
{{/each}}
{{/if}}

## Recipes

{{#each recipes}}
### {{recipe_name}}

**Ingredients**:
{{#each ingredients}}
- {{this}}
{{/each}}

**Instructions**: {{instructions}}

{{/each}}

## Special Instructions

{{special_instructions}}

## Follow-up

- **Next appointment**: {{next_appointment}}
- **Goals**: {{goals}}
- **Monitoring**: {{monitoring}}

---
*Source: {{source_file}}*
*Generated: {{generation_date}}*
*Template: nutrition_plan v{{template_version}}*
