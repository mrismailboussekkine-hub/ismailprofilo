import * as THREE from './vendor/three.module.js';
export function mountStudio(host) {
 let renderer;
 try { renderer = new THREE.WebGLRenderer({alpha:true,antialias:true,powerPreference:'low-power'}); } catch { return ()=>{}; }
 const scene=new THREE.Scene(),camera=new THREE.PerspectiveCamera(32,1,.1,100);
 camera.position.z=6;
 const geometry=new THREE.TorusKnotGeometry(1,.28,120,12,2,3);
 const material=new THREE.MeshBasicMaterial({color:0xe8b18e,wireframe:true,transparent:true,opacity:.55});
 const mesh=new THREE.Mesh(geometry,material);scene.add(mesh);
 renderer.setPixelRatio(Math.min(window.devicePixelRatio,1.5));host.appendChild(renderer.domElement);host.classList.add('ready');
 let active=false,frame=0,last=0;
 const resize=new ResizeObserver(()=>{const w=host.clientWidth,h=host.clientHeight;renderer.setSize(w,h);camera.aspect=w/h;camera.updateProjectionMatrix();renderer.render(scene,camera)});resize.observe(host);
 function tick(now){frame=requestAnimationFrame(tick);if(!active||document.hidden||now-last<32)return;last=now;mesh.rotation.y+=.008;mesh.rotation.z+=.003;renderer.render(scene,camera)}
 const intersection=new IntersectionObserver(e=>{active=e[0].isIntersecting});intersection.observe(host);frame=requestAnimationFrame(tick);
 function move(e){const r=host.getBoundingClientRect();mesh.rotation.x=(e.clientY-r.top)/r.height-.5;mesh.rotation.z=(e.clientX-r.left)/r.width-.5}
 host.addEventListener('pointermove',move);
 return ()=>{cancelAnimationFrame(frame);resize.disconnect();intersection.disconnect();host.removeEventListener('pointermove',move);geometry.dispose();material.dispose();renderer.dispose();renderer.domElement.remove();host.classList.remove('ready')}
}
