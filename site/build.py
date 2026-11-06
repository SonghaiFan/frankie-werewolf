#!/usr/bin/env python3
"""Independent bilingual Werewolf intro, using actual preset and icon sources."""
import argparse,html,json,re,shutil
from pathlib import Path
H=html.escape
ROLES=['WOLF','VILLAGER','SEER','WITCH','GUARD','HUNTER']
def build(repo,out):
 cfg=json.loads((repo/'site/project.json').read_text());cs=json.loads((repo/'site/content.json').read_text());out.mkdir(parents=True,exist_ok=True);media=out/'media';media.mkdir(exist_ok=True)
 for f in ['style.css','demo.js']:shutil.copy(repo/'site'/f,out/f)
 for src,dest in [('docs/readme/banner.png','banner.png'),('docs/readme/assets/frankie.svg','signature.svg')]:shutil.copy(repo/src,media/dest)
 for name in ['home','setup','host','player']:shutil.copy(repo/f'site/assets/{name}-current.png',media/f'{name}.png')
 raw=(repo/'client/src/components/RoleIcons.jsx').read_text()
 for role in ROLES:
  m=re.search(r'\b'+role+r': \(\s*(<svg.*?</svg>)\s*\)',raw,re.S);assert m,role
  svg=m.group(1)
  for a,b in [('strokeWidth','stroke-width'),('strokeLinecap','stroke-linecap'),('strokeLinejoin','stroke-linejoin')]:svg=svg.replace(a,b)
  svg=svg.replace('<svg ','<svg xmlns="http://www.w3.org/2000/svg" ')
  (media/(role.lower()+'.svg')).write_text(svg)
 settings=(repo/'client/src/components/GameSettings.jsx').read_text();presets={}
 for number,fields in re.findall(r'if \(num === (\d+)\) setGameConfig\(\{ ([^}]+) \}\)',settings):
  f=dict(re.findall(r'(\w+): (\w+)',fields));n=int(number);counts={r:0 for r in ROLES};counts['WOLF']=int(f['wolves'])
  for r in ['SEER','WITCH','GUARD','HUNTER']:counts[r]=int(f[r.lower()]=='true')
  counts['VILLAGER']=n-sum(counts.values());assert counts['VILLAGER']>=0;presets[number]=counts
 assert set(presets)=={'6','9','12'}
 (out/'.nojekyll').touch()
 for lang,c in cs.items():
  zh=lang=='zh';pre='../' if zh else './';dest=out/'zh' if zh else out;dest.mkdir(exist_ok=True)
  articles=lambda xs:''.join('<article><h3>'+H(a)+'</h3><p>'+H(b)+'</p></article>' for a,b in xs)
  labels={r:c['roles'][r][0] for r in ROLES}
  initial=''.join(f'<div class="role-count"><img src="{pre}media/{r.lower()}.svg" width="24" height="24" alt=""><strong>{presets["6"][r]}</strong><span>{H(labels[r])}</span></div>' for r in ROLES if presets['6'][r])
  rolelist=''.join(f'<details><summary><img src="{pre}media/{r.lower()}.svg" width="24" height="24" alt="">{H(a)}</summary><p>{H(b)}</p></details>' for r,(a,b) in c['roles'].items())
  galleries=''.join(f'<figure><a href="{pre}media/{name}.png"><img src="{pre}media/{name}.png" alt="{H(cap)}" loading="lazy"></a><figcaption>{H(cap)}</figcaption></figure>' for name,cap in zip(['home','setup','host','player'],c['captions']))
  data=json.dumps({'presets':presets,'labels':labels,'prefix':pre},ensure_ascii=False).replace('<',chr(92)+'u003c')
  page=f'''<!doctype html><html lang="{'zh-CN' if zh else 'en'}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Werewolf Local | {'局域网面杀' if zh else 'A local Wi-Fi table'}</title><meta name="description" content="{H(c['intro'])}"><meta name="theme-color" content="#09090b"><link rel="stylesheet" href="{pre}style.css"><link rel="canonical" href="{cfg['pages_url']+('zh/' if zh else '')}"><link rel="alternate" hreflang="en" href="{cfg['pages_url']}"><link rel="alternate" hreflang="zh-CN" href="{cfg['pages_url']}zh/"><meta property="og:type" content="website"><meta property="og:title" content="Werewolf Local"><meta property="og:description" content="{H(c['intro'])}"><meta property="og:url" content="{cfg['pages_url']+('zh/' if zh else '')}"><meta property="og:image" content="{cfg['pages_url']}media/banner.png"></head><body><a class="skip" href="#main">{H(c['skip'])}</a><header class="shell"><a class="brand" href="{pre}">WEREWOLF <span>LOCAL</span></a><nav aria-label="{'页面导航' if zh else 'Page navigation'}"><a href="#game">{c['nav'][0]}</a><a href="#use">{c['nav'][1]}</a><a href="#screens">{c['nav'][2]}</a><a href="{pre}" lang="en" {'aria-current="page"' if not zh else ''}>EN</a><a href="{pre}zh/" lang="zh-CN" {'aria-current="page"' if zh else ''}>中文</a></nav></header><main class="shell" id="main"><section class="hero"><div><h1>{'<br>'.join(H(t) for t in c['headline'].split(chr(10)))}</h1><p class="lead">{H(c['intro'])}</p><a class="button" href="#start">{H(c['open'])} ↓</a></div><figure class="hero-screen"><img src="{pre}media/setup.png" width="1468" height="1247" alt="{H(c['captions'][1])}" fetchpriority="high"></figure></section>
<section class="section" id="game"><h2>{H(c['concept_title'])}</h2><p class="lead narrow">{H(c['concept'])}</p><div class="features">{articles(c['features'])}</div></section>
<section class="section lineup"><div><h2>{H(c['demo_title'])}</h2><p>{H(c['demo_note'])}</p><div class="preset-controls" aria-label="{H(c['lineup'])}">{''.join(f'<button data-preset="{n}" aria-pressed="{str(n==6).lower()}" type="button">{n} {H(c["preset"])}</button>' for n in [6,9,12])}</div></div><div id="lineup" class="counts" aria-live="polite">{initial}</div></section>
<section class="section roles"><div><h2>{H(c['roles_title'])}</h2><div class="role-list">{rolelist}</div></div><div class="flow"><h2>{H(c['flow_title'])}</h2><ol>{''.join('<li><h3>'+H(a)+'</h3><p>'+H(b)+'</p></li>' for a,b in c['flow'])}</ol></div></section>
<section class="section notes"><div><h2>{H(c['win_title'])}</h2><p>{H(c['win'])}</p></div><div><h2>{H(c['voice_title'])}</h2><p>{H(c['voice'])}</p></div></section>
<section class="section" id="use"><h2>{H(c['workflow_title'])}</h2><ol class="steps">{''.join('<li><h3>'+H(a)+'</h3><p>'+H(b)+'</p></li>' for a,b in c['steps'])}</ol></section>
<section class="section" id="screens"><h2>{H(c['gallery_title'])}</h2><div class="gallery">{galleries}</div></section>
<section class="section"><h2>{H(c['storage_title'])}</h2><div class="storage">{articles(c['storage'])}</div></section>
<section class="section runtime" id="start"><div><h2>{H(c['run_title'])}</h2><p>{H(c['run'])}</p><p>{H(c['production'])}</p></div><div><pre><code>npm ci\nnpm start</code></pre><p><a href="https://github.com/{cfg['repository']}/blob/main/site/GUIDE.md">{H(c['guide'])} ↗</a></p><a href="https://github.com/{cfg['repository']}">{H(c['source'])} ↗</a></div></section></main><footer class="shell"><img src="{pre}media/signature.svg" width="90" height="38" alt="Frankie"><span>{H(c['footer'])}</span></footer><script id="demo-data" type="application/json">{data}</script><script src="{pre}demo.js" defer></script></body></html>'''
  (dest/'index.html').write_text(page)
 print(out)
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--out',default='_site');a=ap.parse_args();build(Path(__file__).resolve().parents[1],Path(a.out).resolve())
