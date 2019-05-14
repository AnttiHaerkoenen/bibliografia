## -*- encoding: utf-8 -*-
<%inherit file="bibliography_base.html"/>
<%
    import string

    def format_author(entry):
        authors = entry['author']
        if not authors:
            return "Anon."
        if 3 < len(authors):
            return f"{authors[0]['last']} et al."
        authors_ = []
        for a in authors:
            a['first_s'] = ' '.join(a['first'])
            authors_.append("{last}, {first_s} {von}".format(**a))
        return ' & '.join(authors_)

    def format_editor(entry):
        return ""

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

    def format_letter(entry):
        number = entry['letter_number']
        if number:
            return string.ascii_lowercase[number - 1]
        return ""

    def format_publoc(entry):
        pub, loc = entry['publisher'], entry['location']
        if loc and pub:
            return f" {pub}, {loc}."
        elif pub:
            return f" {pub}."
        return ""

    def format_booktitle(entry):
        title = entry['booktitle']
        if title:
            return "Teoksessa {title}"
        return ""

    def article(entry):
        entry['numvol'] = format_numvol(entry)
        return "{author} {year}{letter}. {title}. {journal}{numvol}{pages}{doi}.".format(**entry)

    def book(entry):
        return "{author} {year}{letter}. {title}.{publoc}".format(**entry)

    def phdthesis(entry):
        return book(entry) + " Väitöskirja."

    def incollection(entry):
        entry['booktitle'] = format_booktitle(entry)
        return "{author} {year}{letter}. {title}. {booktitle}{editor}{pages}"

    def misc(entry):
        return "{title}".format(**entry)

    styles = {
        'article': article,
        'book': book,
        'incollection': incollection,
        'phdthesis': phdthesis,
        'misc': misc,
    }

    def render_item(entry):
        type_ = entry.__class__.__name__.lower()
        entry['author'] = format_author(entry)
        entry['editor'] = format_editor(entry)
        entry['pages'] = format_pages(entry)
        entry['doi'] = format_doi(entry)
        entry['letter'] = format_letter(entry)
        entry['publoc'] = format_publoc(entry)
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