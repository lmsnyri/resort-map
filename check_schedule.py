"""Check schedule.json before publishing:  python3 -I check_schedule.py
Prints each day's activities as the app will show them, and stops with an error if anything is wrong."""
import json, re, sys, os
here = os.path.dirname(os.path.abspath(__file__))
html = open(os.path.join(here, 'index.html'), encoding='utf-8').read()
i = html.index('window.RESORT='); places = json.loads(html[i+14:html.index('</script>', i)].rstrip().rstrip(';'))['places']
by_id = {p['id']: p for p in places}; by_name = {p['name'].lower(): p for p in places}
try: S = json.load(open(os.path.join(here, 'schedule.json'), encoding='utf-8'))
except Exception as e: sys.exit(f'ERROR: schedule.json is not valid JSON: {e}')
errs = []
def t(s):
    m = re.fullmatch(r'(\d{1,2})[:.](\d{2})', str(s or '').strip())
    return int(m[1])*60+int(m[2]) if m and int(m[1]) < 24 and int(m[2]) < 60 else None
def check(a, where):
    if a.get('cancelled'):
        if not a.get('title'): errs.append(f'{where}: a cancelled item needs the title of the daily item it cancels')
        return
    if not a.get('title'): errs.append(f'{where}: missing "title"')
    if t(a.get('time')) is None: errs.append(f'{where} "{a.get("title")}": time must look like 21:30, got {a.get("time")!r}')
    if 'end' in a and t(a['end']) is None: errs.append(f'{where} "{a.get("title")}": end must look like 23:00, got {a["end"]!r}')
    v = a.get('venue')
    if v and v not in by_id and str(v).lower() not in by_name:
        errs.append(f'{where} "{a.get("title")}": unknown venue {v!r}. Use an id from SCHEDULE.md, or leave venue out and add "where". '
                    'Places outside purple/yellow/green/common areas are deliberately not allowed.')
for n, a in enumerate(S.get('every_day', [])): check(a, f'every_day #{n+1}')
for d, items in S.get('days', {}).items():
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', d): errs.append(f'day key {d!r} must look like 2026-11-10')
    for n, a in enumerate(items): check(a, f'{d} #{n+1}')
if errs: print('\n'.join('ERROR: '+e for e in errs)); sys.exit(1)
key = lambda a: str(a.get('title', '')).strip().lower()
for d in sorted(S.get('days', {})):
    lst = [dict(a, regular=True) for a in S.get('every_day', [])]
    for a in S['days'][d]:
        j = next((k for k, x in enumerate(lst) if x.get('regular') and key(x) == key(a)), None)
        if a.get('cancelled'):
            if j is not None: lst.pop(j)
            continue
        if j is not None: lst[j] = {**lst[j], **a, 'regular': False}
        else: lst.append({**a, 'regular': False})
    lst.sort(key=lambda a: (t(a['time']) + (1440 if t(a['time']) < 300 else 0)))
    print(f'\n{d}')
    for a in lst:
        v = a.get('venue'); pl = by_id.get(v) or by_name.get(str(v).lower()) if v else None
        print(f"  {a['time']:>5}{'–'+a['end'] if a.get('end') else '':7} {a['title']:<28} @ {pl['name'] if pl else a.get('where', '(no venue)')}{'' if a['regular'] else '   [day item]'}")
print('\nOK: schedule.json looks good.')
