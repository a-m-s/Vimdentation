# Vimdentation
Sublime Text 3 Plugin For Vim-Like Indentation Abilities

## Synopsis
I wrote this plugin to give me the ability to look at old code and have it display correctly in Sublime Text. The codebase I support has indentation requirements that are unusual by today's standards, meaning they require Tab characters to be 8 spaces, but indentations to be 4 spaces.

This creates a problem with Sublime Text because while I can set the "tab_size" parameter to 8, it then causes all tab key presses to use 8 spaces as well. This is my attempt at resolving this issue. I decided to put this out there because from reading the forums and the userecho site for Sublime Text, there are at least a few other people out there in my shoes.

The name is corny, but I couldn't think of anything else to call it, and Vim (as well as emacs) is able to handle this type of indentation setting already.

## Installation

Until I decide if this deserves to go on the Package Manager for Sublime Text, you will have to do things the old fashioned way:

```
cd /path/to/sublimetext/Packages
git clone https://github.com/Wintaru/Vimdentation.git Vimdentation
```

## Configuration

Two configuration options are available (default settings shown):

```
"vimdentation_indent_size": 4,
"vimdentation_mixed_tabs": false,
```

In my case, I also have the following in my Preferences.sublime-settings:

```
"auto_indent": true,
"indent_to_bracket": true,
"tab_size": 8,
"translate_tabs_to_spaces": true
```

If "vimdentation_mixed_tabs" is set, then it probably makes sense to have
"translate_tabs_to_spaces" set false.  In this case Vimdentation will insert
spaces until "tab_size" spaces, and then convert those spaces to a hard tab.

## Improvements
Please feel free to let me know if you find issues with this plugin. I'm not a python developer, this was cobbled together as a way for me to get my feet wet. I'm sure there are things that could be done better, and I'm also sure there are bugs to uncover. Thanks!
