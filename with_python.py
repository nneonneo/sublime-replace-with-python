import sublime, sublime_plugin


class PromptReplaceWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("with_python")
        prompt_text = self.settings.get("replace_lastcode") or ""
        self.window.show_input_panel("Enter Python command (using the 'text' variable)", prompt_text, self.on_done, None, None)

    def on_done(self, text):
        self.settings.set("replace_lastcode", text)
        try:
            if self.window.active_view():
                self.window.active_view().run_command("replace_with_python", {"code": text} )
        except ValueError:
            pass

class ReplaceWithPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit, code):
        # Make some common modules available
        import re

        try:
            code = compile(code, "<string>", "exec")
        except Exception as e:
            sublime.error_message("Error while compiling your code: " + str(e))
            return
        codeglobals = {"re": re}

        sel = self.view.sel()
        for i, r in enumerate(sel):
            text = self.view.substr(r)
            try:
                codelocals = {"text": text, "index": i}
                exec code in codeglobals, codelocals
                newtext = codelocals['text']
            except Exception as e:
                sublime.error_message("Error while running your code: " + str(e))
                break

            self.view.replace(edit, r, newtext)


class PromptSortLinesWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("with_python")
        prompt_text = self.settings.get("sort_lines_lastcode") or ""
        self.window.show_input_panel("Enter Python sort key expression (using the 'line' variable)", prompt_text, self.on_done, None, None)

    def on_done(self, text):
        self.settings.set("sort_lines_lastcode", text)
        try:
            if self.window.active_view():
                self.window.active_view().run_command("sort_lines_with_python", {"code": text} )
        except ValueError:
            pass

class SortLinesWithPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit, code):
        # Make some common modules available
        import re

        try:
            code = compile(code, "<string>", "eval")
        except Exception as e:
            sublime.error_message("Error while compiling your code: " + str(e))
            return
        codeglobals = {"re": re}

        sel = self.view.sel()
        if not sel or (len(sel) == 1 and sel[0].empty()):
            sel = [sublime.Region(0, self.view.size())]

        for seli, r in enumerate(sel):
            r = self.view.line(r) # make region span full lines
            rlines = self.view.lines(r)
            lines = [[i, self.view.substr(self.view.full_line(rline))] for i, rline in enumerate(rlines)]
            if not lines:
                continue
            if lines[-1][1].endswith('\n'):
                final_newline = True
            else:
                lines[-1][1] += '\n'
                final_newline = False

            try:
                lines.sort(key=lambda (i, line): eval(code, codeglobals, {"line": line.rstrip('\n'), "index": seli, "lineno": i}))
            except Exception as e:
                sublime.error_message("Error while running your code: " + str(e))
                break

            out = ''.join([line for i, line in lines])
            if not final_newline:
                if out.endswith('\n'):
                    out = out[:-1]
            self.view.replace(edit, r, out)


class PromptSortSelectionsWithPythonCommand(sublime_plugin.WindowCommand):
    def run(self):
        self.settings = sublime.load_settings("with_python")
        prompt_text = self.settings.get("sort_selections_lastcode") or ""
        self.window.show_input_panel("Enter Python sort key expression (using the 'text' variable)", prompt_text, self.on_done, None, None)

    def on_done(self, text):
        self.settings.set("sort_selections_lastcode", text)
        try:
            if self.window.active_view():
                self.window.active_view().run_command("sort_selections_with_python", {"code": text} )
        except ValueError:
            pass

    def is_enabled(self):
        view = self.window.active_view()
        return view and len(view.sel()) > 1

class SortSelectionsWithPythonCommand(sublime_plugin.TextCommand):
    def run(self, edit, code):
        # Make some common modules available
        import re

        try:
            code = compile(code, "<string>", "eval")
        except Exception as e:
            sublime.error_message("Error while compiling your code: " + str(e))
            return
        codeglobals = {"re": re}

        sel = self.view.sel()
        texts = [[i, self.view.substr(r)] for i, r in enumerate(sel)]
        texts.sort(key=lambda (i, text): eval(code, codeglobals, {"text": text, "index": i}))
        for r, (i, t) in reversed(zip(sel, texts)):
            self.view.replace(edit, r, t)
