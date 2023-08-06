# [[ assignment.title ]]

[[ assignment | get_readme ]]

[% for problem in assignment.problems -%]
[% if problem | has_readme -%]
[% include "template:instructions/problem.md" %]
[% endif %]
[%- endfor -%]
