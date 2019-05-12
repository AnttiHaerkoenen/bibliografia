## -*- encoding: utf-8 -*-
<%inherit file="bibliography_base.html"/>
<%
    import string

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

    def format_numvol(entry):
        num, vol = entry['number'], entry['volume']
        if not vol:
            vol = entry['year'] if 'year' in entry else None
        if num and vol:
            return f" {num}/{vol}"
        elif vol:
            return f" {vol}"
        return ""

    def format_doi(entry):
        doi = entry['doi']
        if doi:
            return f", doi:{doi}"
        return ""

    def format_duplicate_letter(entry):
        number = entry['letter_number']
        if number:
            return string.ascii_lowercase[number - 1]
        return ""

    def article(entry):
        entry['numvol'] = format_numvol(entry)
        return "{author} {year}{duplicate_letter}. {title}. {journaltitle}{numvol}{pages}{doi}.".format(**entry)

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
        entry['doi'] = format_doi(entry)
        entry['duplicate_letter'] = format_duplicate_letter(entry)
        if type_ not in styles:
            type_ = 'misc'
        return styles[type_](entry)
%>
<p style="font-size: 12px; row-gap: 1.5px">
    <b>Tutkimuskirjallisuus</b>
    <br><br>
    % for entry in entries:
        ${render_item(entry)}
        <br><br>
    % endfor
</p>