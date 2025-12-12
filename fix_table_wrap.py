# fix_table_wrap.py
import shutil, sys, re, os

p = "signal.html"
if not os.path.exists(p):
    print("ERROR: signal.html not found in current folder.")
    sys.exit(1)

bak = p + ".bak"
shutil.copy2(p, bak)
print(f"Backup written -> {bak}")

s = open(p, "r", encoding="utf-8").read()

# find first <table ... class="dataframe"...> or first <table ...>
m_table = re.search(r"<table\b[^>]*class=[\"'][^\"']*dataframe[^\"']*[\"'][^>]*>", s, flags=re.IGNORECASE)
if not m_table:
    m_table = re.search(r"<table\b[^>]*>", s, flags=re.IGNORECASE)
if not m_table:
    print("ERROR: No <table> tag found in file.")
    sys.exit(1)

table_start_idx = m_table.start()
table_tag_end_idx = m_table.end()

# find first <tr> after table_tag_end_idx (header row start)
m_tr = re.search(r"<tr\b[^>]*>", s[table_tag_end_idx:], flags=re.IGNORECASE)
if not m_tr:
    print("ERROR: No <tr> found after <table> start. File may be malformed.")
    sys.exit(1)

tr_start_rel = m_tr.start()
tr_start_idx = table_tag_end_idx + tr_start_rel

# find the end of that first </tr>
m_tr_end = re.search(r"</tr\s*>", s[tr_start_idx:], flags=re.IGNORECASE)
if not m_tr_end:
    print("ERROR: Couldn't find closing </tr> for header row.")
    sys.exit(1)

tr_end_rel = m_tr_end.end()
tr_end_idx = tr_start_idx + tr_end_rel

# Now build new content:
# keep everything up to table_tag_end_idx (i.e. <table ...>)
before_table = s[:table_tag_end_idx]
header_tr_html = s[tr_start_idx:tr_end_idx]  # includes the <tr>..</tr>
# remainder after the header row
after_header = s[tr_end_idx:]

# ensure we don't already have thead/tbody
if re.search(r"<thead\b", s, flags=re.IGNORECASE) or re.search(r"<tbody\b", s, flags=re.IGNORECASE):
    print("NOTE: file already contains <thead> or <tbody>. No changes made.")
    sys.exit(0)

new_table_html = before_table + "<thead>" + header_tr_html + "</thead><tbody>" + after_header

# ensure we close tbody before </table> (replace first </table> after insertion)
# find first </table> after insertion point
m_table_close = re.search(r"</table\s*>", new_table_html, flags=re.IGNORECASE)
if not m_table_close:
    print("ERROR: no closing </table> found after insertion - aborting and restoring backup.")
    shutil.copy2(bak, p)
    sys.exit(1)

# Insert closing </tbody> right before that </table>
close_idx = m_table_close.start()
if not new_table_html[close_idx-7:close_idx].lower().endswith("</tbody"):
    new_table_html = new_table_html[:close_idx] + "</tbody>" + new_table_html[close_idx:]

# write
open(p, "w", encoding="utf-8").write(new_table_html)
print("SUCCESS: signal.html patched (thead/tbody inserted). Please refresh the page.")
