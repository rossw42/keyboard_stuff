import csv,json,os
from collections import Counter
csvp='D:/GitHub/keyboard_stuff/scripts/vial-research/vial_keyboard_pairs.csv'
pk=['c','r','rx','ry','d','h','w2','h2','x2','y2']
rows=[(r['keyboard.json'],r['vial.json']) for r in csv.DictReader(open(csvp,encoding='utf-8'))]
tot=len(rows)
ok=0;fails=[];mx=0;ll=0;nl=0;pc=Counter();lg=Counter();vid=0;pid=0;both=0;kle=[]
ke=0;ko=0;kf=[];mp=0;lc=Counter();ml=[];vl=[];NL=chr(10)
for kbp,vp in rows:
 n=vp.replace(chr(92),'/')
 if '/keyboards/' in n:n=n.split('/keyboards/',1)[1].replace('/keymaps/vial/vial.json','')
 d=None
 try:
  d=json.load(open(vp,encoding='utf-8'));ok+=1
 except Exception as e:fails.append((n,str(e)))
 if d is not None:
  mx+=('matrix' in d)
  lo=d.get('layouts') if isinstance(d.get('layouts'),dict) else {}
  lb=lo.get('labels')
  if lb:ll+=1;vl.append((n,lb))
  km=lo.get('keymap',[])
  fp=set();nf=0;nr=0;ns=0
  for rw in km:
   if isinstance(rw,list):
    nr+=1
    for it in rw:
     if isinstance(it,str):
      ns+=1
      if NL in it:nf=1
     elif isinstance(it,dict):
      fp.update(k for k in it if k in pk)
  nl+=nf
  for k in fp:pc[k]+=1
  lv=d.get('lighting','<absent>')
  if isinstance(lv,(dict,list)):lv=json.dumps(lv)
  lg[str(lv)]+=1
  v='vendorId' in d;p='productId' in d
  vid+=v;pid+=p;both+=(v and p)
  kle.append((n,nr,ns))
 if os.path.exists(kbp):
  ke+=1;kb=None
  try:
   kb=json.load(open(kbp,encoding='utf-8'));ko+=1
  except Exception as e:kf.append((n,str(e)))
  if kb is not None:
   mp+=('matrix_pins' in kb)
   lys=kb.get('layouts') if isinstance(kb.get('layouts'),dict) else {}
   lc[len(lys)]+=1
   if len(lys)>1:ml.append((n,len(lys),list(lys.keys())))
 else:lc['<missing kb.json>']+=1
W='='*78
print(W);print('REAL vial.json STATISTICS (from vial_keyboard_pairs.csv)');print(W)
print(f'Total pairs in CSV: {tot}')
print();print('--- vial.json ---')
print(f'Parsed successfully: {ok} / {tot}')
for n,e in fails:print(f'  PARSE FAIL: {n}: {e}')
print(f'Has top-level matrix field: {mx}')
print(f'Has layouts.labels (multi-layout options): {ll}')
print(f'Keymaps with any label containing newline: {nl}')
print();print('Property-dict key presence (files with at least one occurrence):')
for k in pk:print(f'  {k:<4}{pc.get(k,0)}')
print();print('Distribution of lighting values:')
for v,c in lg.most_common():print(f'  {v:<30}{c}')
print();print(f'Has vendorId: {vid}');print(f'Has productId: {pid}');print(f'Has both vendorId+productId: {both}')
rc=[r for _,r,_ in kle];sc=[s for _,_,s in kle]
print();print('--- KLE keymap size per vial.json ---')
print(f'KLE rows:   min={min(rc)} max={max(rc)} mean={sum(rc)/len(rc):.1f} total={sum(rc)}')
print(f'Str labels: min={min(sc)} max={max(sc)} mean={sum(sc)/len(sc):.1f} total={sum(sc)}')
z=[n for n,r,_ in kle if r==0]
if z:
 print(f'Files with 0 KLE rows ({len(z)}):')
 for n in z:print(f'  {n}')
print();print('--- keyboard.json ---')
print(f'keyboard.json exists: {ke} / {tot}')
print(f'keyboard.json parsed OK: {ko} / {ke}')
for n,e in kf:print(f'  PARSE FAIL: {n}: {e}')
print(f'keyboard.json has matrix_pins: {mp}')
print();print('Distribution of len(layouts) in keyboard.json:')
for v,c in sorted(lc.items(),key=lambda x:str(x[0])):print(f'  layouts={v}: {c}')
print();print(W);print(f'KEYBOARDS WHERE keyboard.json DEFINES >1 LAYOUT ({len(ml)}):');print(W)
for n,c,names in sorted(ml):print(f'  {n} ({c} layouts): '+', '.join(names))
print();print(W);print(f'KEYBOARDS WHERE vial.json HAS layouts.labels ({len(vl)}):');print(W)
for n,lb in sorted(vl):print(f'  {n}: '+json.dumps(lb))
