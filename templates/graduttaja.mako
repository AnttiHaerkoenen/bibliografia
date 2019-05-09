<%!
    def article(item):
        return "artikkeli: " + item

    styles = {
        'article': article,
    }

    def render_item(item):
        type = 'article'
        return styles[type](item)
%>

Tutkimuskirjallisuus

% for item in items:
    %if isinstance(item, str):
${render_item(item)}
    %endif
% endfor
