# Common pitfalls

The traps almost every learner falls into in the first modules. Each one looks obvious once
named and keeps coming back until it has been traced by hand a few times. The tutor draws
predict drills from this list; use it yourself as a self-check before you say "done".

Each entry: the trap, the rule, and a question to check yourself.

## Loops and accumulators

| Trap | Rule | Check |
| --- | --- | --- |
| A maximum starting at `0` | A best-so-far starts at the first item (or `-inf`); `0` silently wins on an all-negative list | What does a max starting at 0 return for `[-3, -1]`? |
| A sum starting at the first item (or `-inf`) | A sum or count starts at `0`: adding 0 changes nothing | Why does a sum that starts at `nums[0]` double-count? |
| An `if not items` guard before every loop | A loop over an empty list runs zero times, with no error; the start value is already the empty-case answer | What does a sum loop with no guard return for `[]`? |
| `return -1` inside the loop's `else` | Any `return` inside the loop ends the function on that pass; a "not found" return goes after the loop | In a linear search, on which item does an `else: return -1` stop? |
| Saving the match in a variable and carrying on | To find the *first* match, return as soon as you find it; carrying on keeps the *last* one | Trace `["a", "b", "a"]`: which index does a keep-going loop end with? |
| A function with no `return` on some path | Falling off the end returns `None` | What does a search return for `[]` if the only `return` is inside the loop? |

## range and slices

| Trap | Rule | Check |
| --- | --- | --- |
| `range(1, n)` for 1 to n | The stop is excluded: `range(1, n + 1)` | What is the last value of `range(1, 5)`? |
| Thinking a "backwards" range raises an error | If start is already at or past stop (in the step's direction), the range is empty, with no error and no infinite loop | What is `list(range(1, -2))`? And `list(range(0, 0, -1))`? |
| Counting down with `range(n, 1, -1)` | Count down to 1 with `range(n, 0, -1)`: the stop is still excluded | What does `list(range(3, 1, -1))` give? |
| `for x in n` where `n` is an int | An int is not iterable; loop over `range(...)` | What does `TypeError: 'int' object is not iterable` point at? |
| Skipping the first item with `items[:len(items)]` | `items[1:]` skips the first item (and copies the list, O(n) space); `range(1, len(items))` avoids the copy | What does `[1, 2, 3][1:]` give? |

## Values and types

| Trap | Rule | Check |
| --- | --- | --- |
| `items is None` to test for an empty list | `[]` is a real (empty) list, not `None`; test emptiness with `not items` | What does `[] is None` give? |
| `print` instead of `return` | `print` only shows a value; `return` hands it to the caller | What does a test receive from a function that only prints? |
| `&` or `/` as logical operators, `=` to compare | Use `and`, `or`, `not`; `=` assigns, `==` compares | Why is `if a & b > 0` risky? |
| Numbers left as ints in a list of strings | When every element must be a string, convert with `str(n)` | What type is each element of the FizzBuzz output? |

## Reading the task

| Trap | Rule | Check |
| --- | --- | --- |
| Dropping half of the condition | Restate it naming the exact comparison: "greater than zero" is `> 0`; "at least" or "greater than or equal to" is `>=` | Does a value equal to the threshold count? |
| Returning the value instead of its position | Say what the function returns (a value, an index, a list) when you restate | What does a "first index" function return when nothing matches? |
| Checking "multiple of 3" before "multiple of 3 and 5" | With overlapping conditions, test the most specific one first | What would 15 give if the `% 3` check came first? |
| Tracing only the example from the task | Its answer is already printed; trace an input of your own and an edge case through your plan | Which input would break your plan? |

## Complexity

| Trap | Rule | Check |
| --- | --- | --- |
| Calling a fixed set of variables O(k) or O(n) | A fixed number of variables is O(1) space, however many there are | What is the extra space of a running total? |
| Forgetting the output list | An output list of n items is O(n) space (O(1) auxiliary if the output is not counted) | What is the space of building a list of n strings? |
| Using letters that were never defined | Name Big-O with the input's own variable (`n` = length of the list); use another letter only after defining it | What would `k` stand for in your answer? |
| Thinking a slice is free | A slice copies: O(k) time and space for k items | Does `items[1:]` change the total time of a loop from O(n)? |

## Workflow

| Trap | Rule | Check |
| --- | --- | --- |
| Running the tests on an unsaved file | Save first (autosave is on in the repo's editor settings); `dojo.py test` warns when the file is still the stub | Did you see the stub's `NotImplementedError` in the output? |
| Code that drifts from the plan | Reread each line against the plan you said out loud before you predict | Which line differs from the plan? |
| Answering "what does it return" with the spec | Trace the code's own variables; what the spec says is a separate question | What does *your* code return for `[]`? |
