# Benchmark Tasks

The benchmark should measure **understanding and instruction following**, not merely OCR transcription. Task design therefore needs semantic diversity and deterministic scoring.

## Design principles

Each task should:

- have a stable unique ID;
- contain an authoritative source instruction;
- contain the task payload separately from the instruction;
- define one or more machine-checkable expected outputs where practical;
- define scoring logic before the experiment runs;
- avoid dependence on proprietary data;
- be understandable without external web access; and
- remain logically identical between text and image conditions.

## Recommended task schema

Illustrative JSONL record:

```json
{
  "task_id": "negation_001",
  "category": "negation",
  "instruction": "Return every fruit except the one with the highest price. Output names only, in the original order.",
  "payload": "Apple 2.10\nPear 1.80\nOrange 2.50\nPlum 1.25",
  "expected": ["Apple", "Pear", "Plum"],
  "scorer": "ordered_list_exact",
  "tags": ["exclude", "ordering"],
  "version": 1
}
```

The actual schema should separate scorer-specific configuration from human-readable metadata when implementation begins.

## Core task classes

### 1. Simple semantic selection

Purpose: establish a low-difficulty comprehension baseline.

Examples:

- return the second city mentioned;
- select all items belonging to a named category;
- return the smallest amount;
- choose the sentence describing a future event.

These should not require character-perfect recovery of arbitrary identifiers.

### 2. Negation and exclusion

Purpose: detect whether small visual degradation causes important qualifiers to disappear semantically.

Examples:

- do not include the largest value;
- return all colours except blue;
- ignore entries dated before a threshold;
- never output an explanation.

Include varied lexical forms: `not`, `except`, `exclude`, `ignore`, `never`, `without`.

### 3. Conditional instructions

Purpose: measure understanding of branching logic.

Examples:

- if total > 100 return HIGH, otherwise LOW;
- if a date is missing return null;
- include the tax field only when tax is explicitly shown;
- unless the code begins with X, return INVALID.

Use both positive and negative branches across the dataset so a constant-answer strategy cannot score well.

### 4. Ordered multi-step rules

Purpose: test whether the model can maintain multiple instructions read from the image.

Examples:

- sort values ascending, take the middle value, multiply by two;
- filter rows first, then group, then return the highest remaining value;
- normalize case, remove duplicates, preserve first-occurrence order.

Keep the underlying reasoning modest enough that text-baseline failures remain uncommon.

### 5. Structured-output constraints

Purpose: test whether semantic rules and output format survive visual encoding.

Examples:

- output valid JSON only;
- use exactly specified keys;
- use null rather than inventing missing values;
- return an array of objects with required field types;
- output lowercase strings only.

Scoring should parse output rather than require irrelevant whitespace equality.

### 6. Numeric and date rules

Purpose: test qualifiers, thresholds, signs, decimal values, and date semantics.

Examples:

- choose values strictly greater than 20, not greater-than-or-equal;
- compare two ISO dates;
- preserve leading zeros when the instruction explicitly requires a string;
- select entries inside an inclusive or exclusive date interval.

Keep exact identifier-like tasks in the OCR control subset unless they are semantically necessary.

### 7. Uncertainty and null behaviour

Purpose: measure hallucination resistance.

Examples:

- return null if a value is not explicitly present;
- do not infer a vendor from product names;
- omit a field when evidence is ambiguous;
- answer UNKNOWN unless a stated condition is met.

The task payload should sometimes contain plausible distractors to ensure the rule matters.

### 8. Reference resolution

Purpose: test comprehension of natural-language relationships.

Examples:

- return the price of the item described in the previous sentence;
- if the second option is unavailable, choose the one immediately after it;
- apply a rule to `the earlier date` or `the remaining item`.

Avoid ambiguous source instructions; the benchmark should test visual understanding, not poorly written prose.

### 9. Formatting and bounded-response rules

Purpose: test lightweight instructions where exact meaning matters more than OCR perfection.

Examples:

- answer in exactly three words;
- output one line;
- lowercase only;
- comma-separated names without spaces;
- no prose outside the JSON object.

Score semantic correctness and format compliance separately.

### 10. Long-form instruction blocks

Purpose: test whether density affects comprehension differently as instruction length increases.

Create short, medium, and long forms with multiple clauses and realistic redundancy.

Length should be a recorded dataset attribute so results can be stratified.

### 11. Exact-string OCR control subset

Purpose: provide a diagnostic bridge to conventional tiny-text OCR benchmarks.

This should be a minority of the dataset.

Examples:

- reproduce a 12-character hex-like token;
- distinguish `0/O`, `1/l/I`, `5/S`, `8/B`;
- preserve punctuation and case;
- reproduce a short path or identifier.

These tasks are expected to be more typography-sensitive than ordinary prose and should not dominate the headline semantic score.

### 12. Real-world-shaped synthetic instructions

Purpose: improve external validity without exposing private corporate prompts.

Potential public synthetic patterns:

- receipt extraction rules;
- document classification;
- record normalization;
- API-field transformation;
- context-summary constraints;
- agent action-selection rules.

## Dataset balance

A 200-task validation set could approximately allocate:

```text
20 simple semantic selection
25 negation/exclusion
25 conditionals
20 ordered multi-step
25 structured output
20 numeric/date
20 uncertainty/null
15 reference resolution
10 bounded-format
10 longer instruction blocks
10 exact-string OCR controls
```

These counts are illustrative. The important principle is that exact OCR does not overwhelm semantic instruction following.

## Difficulty calibration

Before the image benchmark, run text baselines to identify tasks that Luna consistently fails for reasons unrelated to visual encoding.

Tasks with poor text-baseline performance may be:

- revised before the dataset is frozen;
- retained in a separately reported hard stratum; or
- excluded according to a predeclared rule.

Do not rewrite tasks after observing which font performs best unless the dataset version is incremented and the change is documented.

## Avoiding accidental cues

Do not make expected outputs predictable from task IDs, category names, ordering patterns, or fixed answer positions.

Examples:

- alternate which conditional branch is correct;
- randomize which list item is the target;
- vary whether null is or is not expected;
- avoid every negation task excluding the final item.

Generation should use a recorded seed where randomness is involved.

## Instruction wording diversity

The benchmark should not test one writing style only. Use natural variations in:

- sentence length;
- punctuation;
- imperative wording;
- explicit vs compact constraints;
- synonymous qualifiers; and
- clause ordering.

However, source instructions should remain clear and unambiguous.

## Scoring metadata

Every task should specify its scorer and any tolerance before execution.

Possible scorer types:

- exact scalar;
- normalized scalar;
- numeric tolerance;
- ordered list;
- unordered set;
- JSON schema + field comparison;
- null/unknown exact policy;
- regex-constrained format; and
- composite rule scorer.

## Public-data policy

Use synthetic or clearly redistributable content. Do not incorporate customer receipts, private app prompts, secrets, or copyrighted datasets without appropriate permission and licensing.
