<html lang="en">
<body>
<%
    def article(entry):
        return "{author} {date}. {title}. {journaltitle} {number}/{volume}, {pages}, doi:{doi}".format(**entry)

    def book(entry):
        return "kirja: " + entry['ID']

    def incollection(entry):
        return "kokoelmassa: " + entry['ID']

    def misc(entry):
        return "sekalaista: " + entry['ID']

    styles = {
        'article': article,
        'book': book,
        'incollection': incollection,
        'misc': misc,
    }

    def render_item(entry):
        type_ = entry['ENTRYTYPE']
        return styles[type_](entry)
%><b>Tutkimuskirjallisuus</b>
<br><br>
% for entry in entries:
    %if isinstance(entry, dict):
        ${render_item(entry)}
        <br><br>
    %endif
% endfor
</body>
</html>
