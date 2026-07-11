from html import escape
from textwrap import dedent


def header():

    return dedent("""
<div class="cp-header">

    <div class="cp-title">
        CELESTIA PROBE
    </div>

    <div class="cp-status">

        <div>STATUS : ONLINE</div>
        <div>ARCHIVE : CONNECTED</div>
        <div>MODE : SCIENTIFIC OBSERVATION</div>

    </div>

</div>
""")


def metadata(source, entity):

    return dedent(f"""
<div class="metadata-panel">

    <div class="metadata-item">
        <span class="label">SOURCE</span>
        <span class="value">{escape(source)}</span>
    </div>

    <div class="metadata-item">
        <span class="label">ENTITY</span>
        <span class="value">{escape(entity)}</span>
    </div>

    <div class="metadata-item">
        <span class="label">STATUS</span>
        <span class="value verified">VERIFIED</span>
    </div>

</div>
""")


def user_message(text):

    return dedent(f"""
<div class="message user">

    <div class="message-label">
        USER QUERY
    </div>

    <div class="message-body">
        &gt; {escape(text)}
    </div>

</div>
""")


def assistant_message(text):

    text = escape(text)
    text = text.replace("\n", "<br>")

    return dedent(f"""
<div class="message assistant">

    <div class="message-label">
        ARCHIVE RESPONSE
    </div>

    <div class="message-body">
        {text}
    </div>

</div>
""")


def divider():

    return dedent("""
<div class="divider"></div>
""")