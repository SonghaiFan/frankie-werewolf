// Actual GameSettings preset data and RoleIcons artwork, extracted at build time.
const data=JSON.parse(document.querySelector('#demo-data').textContent);
const controls=[...document.querySelectorAll('[data-preset]')];
function show(button){
 controls.forEach(b=>b.setAttribute('aria-pressed',String(b===button)));
 const roles=data.presets[button.dataset.preset];
 document.querySelector('#lineup').replaceChildren(...Object.entries(roles).filter(([,n])=>n).map(([role,count])=>{
  const el=document.createElement('div');el.className='role-count';
  const image=document.createElement('img');image.src=data.prefix+'media/'+role.toLowerCase()+'.svg';image.alt='';image.width=24;image.height=24;
  const strong=document.createElement('strong');strong.textContent=count;
  const span=document.createElement('span');span.textContent=data.labels[role];el.append(image,strong,span);return el;
 }));
}
controls.forEach(b=>b.addEventListener('click',()=>show(b)));
