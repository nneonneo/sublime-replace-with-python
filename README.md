## Sublime Text "Replace with Python"

Sublime Text has a great regex-powered find-and-replace feature. But, what if you want to do a little more complex replacement? "Replace with Python" empowers your replace command with Python, letting you do advanced text manipulation intuitively and easily.

## Variables

- `text` - Selected text. Usable in `Replace With Python` and `Permute Selections => Sort With Python`.
- `line` - Line within a selection. Usable in `Permute Lines => Sort With Python`.
- `index` - 0-based index of the current selection region. Usable in all functions.
- `lineno` - Line number within the current selection. Usable in `Permute Lines => Sort With Python`.

## Detailed Usage

- `Find => Replace With Python`
    1. Select some regions of text, e.g. by alt+dragging a rectangular area or by using  `Find => Find...` followed by alt+enter to select all matches.
    2. Activate this command to bring up a command entry box
    3. Type a Python statement (or multiple statements separated by newlines, which you can enter with `alt+enter`), which uses the `text` and/or `index` variables and ultimately assigns the `text` variable.
    4. Your snippet will be executed once per selection region, with the output `text` variable replacing the selected text.
- `Edit => Permute Lines => Sort With Python`
    1. Optionally, select some regions of text. Each region will be sorted independently. The entire file is sorted if nothing is selected.
    2. Activate this command to bring up a command entry box.
    3. Type a Python expression which uses the `line` and/or `index` variables. The result of this expression is used as a sort key.
    4. The expression is executed once per line in a selection region, and the lines are sorted according to the resulting values.
- `Edit => Permute Selections => Sort With Python`
    1. Select some regions of text.
    2. Activate this command to bring up a command entry box
    3. Type a Python expression which uses the `text` and/or `index` variables.
    4. The expression is executed once per selection region, and the regions are moved according to the resulting values. Unselected text is not affected.

## Installing

Drop `with_python.py` in your Sublime Text 2 `Packages/User` directory (use `Preferences => Browse Packages...` to get there). Next, add the following lines to `Packages/Default/Main.sublime-menu`:

```diff
diff a/Default/Main.sublime-menu b/Default/Main.sublime-menu
--- a/Default/Main.sublime-menu
+++ b/Default/Main.sublime-menu
@@ -279,6 +279,7 @@
                 "caption": "Permute Lines",
                 "children":
                 [
+                    { "command": "prompt_sort_lines_with_python", "caption": "Sort With Python" },
                     { "command": "permute_lines", "args": {"operation": "reverse"}, "caption": "Reverse" },
                     { "command": "permute_lines", "args": {"operation": "unique"}, "caption": "Unique" },
                     { "command": "permute_lines", "args": {"operation": "shuffle"}, "caption": "Shuffle" }
@@ -290,6 +291,7 @@
                 [
                     { "command": "sort_selection", "args": {"case_sensitive": false}, "caption": "Sort" },
                     { "command": "sort_selection", "args": {"case_sensitive": true}, "caption": "Sort (Case Sensitive)" },
+                    { "command": "prompt_sort_selections_with_python", "caption": "Sort With Python" },
                     { "command": "permute_selection", "args": {"operation": "reverse"}, "caption": "Reverse" },
                     { "command": "permute_selection", "args": {"operation": "unique"}, "caption": "Unique" },
                     { "command": "permute_selection", "args": {"operation": "shuffle"}, "caption": "Shuffle" }
@@ -331,6 +333,7 @@
             { "command": "show_panel", "args": {"panel": "incremental_find", "reverse": false}, "caption": "Incremental Find" },
             { "caption": "-" },
             { "command": "show_panel", "args": {"panel": "replace"}, "caption": "Replace…" },
+            { "caption": "Replace With Python", "command": "prompt_replace_with_python"},
             { "command": "replace_next" },
             { "caption": "-" },
             { "command": "find_under", "caption": "Quick Find" },
```

Reboot Sublime Text to see the new menu options.

You can similarly add key bindings to the appropriate `.sublime-keymap` file. For example, on macOS, I have

    { "keys": ["option+super+e"], "command": "prompt_replace_with_python" }

