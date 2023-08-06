# code_black

A package for randomly allocating patients to ICU beds.

### Features

- Randomly allocates a list of patients to available ICU beds.
- Accepts direct user input or a pregenerated list of patients

### Usage

```
from code_black import code_black

# generate list of selected patients out of user input
code_black.tell_lucky_ones()  # prints list of selected patients

# generate list of selected patients out of pregenerated list
code_black.pull_trigger(list_of_patients, 2) # returns list of 2 selected patients for the 2 available beds
```

### Future developments

- Add checks for valid MDN numbers during input
- Add logging
- Direct connection to backlog of patients waiting for ICU bed in EPD
- Output to dashboard