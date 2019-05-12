## -*- encoding: utf-8 -*-
<%inherit file="bibliography_base.html"/>
<%
    def format_author(entry):
        authors = entry['author']
        if not authors:
            return "Anon."
        authors_ = []
        for a in authors:
            a['first_s'] = ' '.join(a['first'])
            authors_.append("{last}, {first_s} {von}".format(**a))
        return ' & '.join(authors_)

    def format_pages(entry):
        pages = entry['pages']
        if not pages:
            return ''
        if len(pages) == 1:
            return f", {pages[0]}"
        if len(pages) == 2:
            return f", {pages[0]}–{pages[1]}"

    def article(entry):
        return "{author} {year}. {title}. {journaltitle} {number}/{volume}{pages}, doi:{doi}.".format(**entry)

    def book(entry):
        return "kirja: " + entry['ID']

    def thesis(entry):
        return "väitöskirja: " + entry['ID']

    def incollection(entry):
        return "kokoelmassa: " + entry['ID']

    def online(entry):
        return "netistä: " + entry['ID']

    def misc(entry):
        return "sekalaista: " + entry['ID']

    styles = {
        'article': article,
        'book': book,
        'incollection': incollection,
        'online': online,
        'thesis': thesis,
        'misc': misc,
    }

    def render_item(entry):
        type_ = entry['ENTRYTYPE']
        entry['author'] = format_author(entry)
        entry['pages'] = format_pages(entry)
        if type_ not in styles:
            type_ = 'misc'
        return styles[type_](entry)
%><b>Tutkimuskirjallisuus</b>
<br><br>
% for entry in entries:
    %if isinstance(entry, dict):
        ${render_item(entry)}
        <br><br>
    %endif
% endfor
