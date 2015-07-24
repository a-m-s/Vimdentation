import sublime, sublime_plugin
import sys
import re

class VimTabPressCommand(sublime_plugin.TextCommand):
    """
    This is meant to be bound on the tab key like this:
    { "keys": ["tab"], "command": "vim_tab_press", "context":
        [
            { "key": "auto_complete_visible", "operator": "equal", "operand": false }
        ]
    }

    The context parameter ensures this doesn't break auto
    complete when "auto_complete_commit_on_tab": true is
    set.

    This lets you set a tab char width in spaces that
    is independent of the spaces advanced when the tab
    key is pressed. In my case, tabs are translated to
    spaces (8 of them), but below I have it set to insert
    4 spaces when tab is pressed.
    """
    def run(self, edit):
        if self.view.settings().has("vimdentation_indent_size"):
            indent_size = self.view.settings().get("vimdentation_indent_size")
        mixed_tabs = self.view.settings().get("vimdentation_mixed_tabs")
        tab_size = self.view.settings().get("tab_size")
        sel = self.view.sel()

        def insert_indent(insert_point):
            # insert spaces upto the next "indent stop" (like tab stop)
            row, char_column = self.view.rowcol(insert_point)
            real_column = 0
            for i in range(insert_point - char_column, insert_point):
                if self.view.substr(i) == "\t":
                    real_column += tab_size
                else:
                    real_column += 1
            space_count = indent_size - (real_column % indent_size)
            self.view.insert(edit, insert_point, " " * space_count)

            if mixed_tabs:
                # scan the line for spaces to convert to tabs
                line_start = insert_point - char_column
                current_point = insert_point + space_count
                earliest_space = insert_point
                while earliest_space > line_start \
                      and self.view.substr(earliest_space - 1) == " ":
                    earliest_space -= 1
                earliest_space_column = real_column - (insert_point - earliest_space)
                last_space_column = real_column + space_count;
                while earliest_space_column // tab_size < last_space_column // tab_size:
                    replace_from = earliest_space
                    replace_count = tab_size - ((earliest_space_column + tab_size) % tab_size)
                    self.view.replace(edit, sublime.Region(replace_from, replace_from + replace_count), "\t")
                    earliest_space += 1
                    earliest_space_column += replace_count

        for region in sel:
            # If the region isn't empty it's selected text so
            # break out the lines in the selection and add the
            # spaces to the beginning of each line selected.
            if not region.empty():
                selectedLines = self.view.lines(region)
                for l in reversed(selectedLines):
                    start = self.view.find("[^ \t]", l.begin())
                    if start is None:
                        start = l
                    insert_indent(start.begin())
            else:
                # For those cases where nothing is selected, put the
                # spaces whereever the cursor is.
                insert_indent(region.begin())

class VimShiftTabPressCommand(sublime_plugin.TextCommand):
    """
    This is meant to be bound on the tab key like this:
    { "keys": ["shift+tab"], "command": "vim_shift_tab_press"}

    Used in tandem with the above command, this allows you to use
    shift+tab in a way you might expect it to work. If you have
    your tab spaces set to 8, shift tab will move back 8 instead of
    4 without this.
    """
    def run(self, edit):
        tab_size = self.view.settings().get("tab_size")
        mixed_tabs = self.view.settings().get("vimdentation_mixed_tabs")
        if self.view.settings().has("vimdentation_indent_size"):
            space_count = self.view.settings().get("vimdentation_indent_size")
        else:
            space_count = 4

        p = re.compile("[^ \t]")
        sel = self.view.sel()
        for region in reversed(sel):
            selectedLines = self.view.lines(region)
            for l in reversed(selectedLines):
                # Extract the string from the line region
                s = self.view.substr(l)

                # Only do this if there are enough spaces to start
                first_char = p.search(s)
                if first_char:
                    indent_count = 0
                    for i in range(0, first_char.start()):
                        if s[i] == "\t":
                            indent_count += tab_size
                        else:
                            indent_count += 1
                    if indent_count >= space_count:
                        new_indent = indent_count - space_count
                        new_spaces = " " * new_indent;
                        if mixed_tabs:
                            new_spaces = ("\t" * (new_indent // tab_size)) + (" " * (new_indent % tab_size))
                        s = new_spaces + s[first_char.start():]
                        self.view.replace(edit, l, s)
