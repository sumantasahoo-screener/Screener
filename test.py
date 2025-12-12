# run this once to wrap table header/body in signal.html
p = "signal.html"
s = open(p, "r", encoding="utf-8").read()

old_start = '<table border="1" class="dataframe"><tr>'
if old_start not in s:
    raise SystemExit("Expected table start not found. Opened file may differ.")

# find end of the first </tr> after the table start
start_idx = s.find(old_start)
first_tr_end = s.find("</tr>", start_idx)
if first_tr_end == -1:
    raise SystemExit("Couldn't find end of header row.")

# insert closing thead/open tbody right after that first </tr>
insert_at = first_tr_end + len("</tr>")
s = s[:start_idx] + '<table border="1" class="dataframe"><thead>' + s[start_idx+len('<table border="1" class="dataframe">') : insert_at] + '</thead><tbody>' + s[insert_at:]

# now replace the final closing </table> with </tbody></table> if needed
if "</tbody></table>" not in s:
    s = s.replace("</table>", "</tbody></table>", 1)

open(p, "w", encoding="utf-8").write(s)
print("Patched signal.html — header/body wrapped. Reload page.")
