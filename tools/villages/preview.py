"""Render planned villages (tools/villages/out/<layout>.json from compile.py --preview) with headless Edge.

  python tools/villages/preview.py spire_a            -> tools/villages/out/spire_a.png (three views + plan)
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'buildings'))
from preview import shoot, THREE  # noqa: E402

PAGE = r"""<!doctype html><html><head><meta charset="utf-8"><style>
html,body{margin:0;height:100%;overflow:hidden;background:#140f1f}
.lab{position:absolute;color:#efe6f5;font:15px monospace;text-shadow:1px 1px 0 #000}
</style></head><body>
<script src="__THREE__"></script>
<script>__VIEWER__</script>
<script>
const V = __DATA__;
const W = innerWidth, H = innerHeight;
const renderer = new THREE.WebGLRenderer({antialias:true});
renderer.setPixelRatio(1); renderer.setSize(W, H); renderer.setScissorTest(true);
renderer.setClearColor(0x140f1f);
document.body.appendChild(renderer.domElement);
const group = voxelGroup(V);
const scene = new THREE.Scene(); scene.add(group);
const [sx, sy, sz] = V.size, [cx, cy, cz] = V.center;
group.position.set(-cx, -cy, -cz);
const span = Math.max(sx, sz);
const VIEWS = [[-35, 32, 0, 0, W * 0.5, H * 0.5], [145, 32, W * 0.5, 0, W * 0.5, H * 0.5],
               [55, 14, 0, H * 0.5, W * 0.5, H * 0.5], [0, 89, W * 0.5, H * 0.5, W * 0.5, H * 0.5]];
for (const [az, el, x, y, w, h] of VIEWS) {
  const cam = new THREE.PerspectiveCamera(30, w / h, 0.5, 4000);
  const a = az * Math.PI / 180, e = el * Math.PI / 180, dist = span * 1.55;
  cam.position.set(Math.sin(a) * Math.cos(e) * dist, 8 + Math.sin(e) * dist, -Math.cos(a) * Math.cos(e) * dist);
  if (el > 80) cam.up.set(0, 0, -1);
  cam.lookAt(0, 6, 0);
  renderer.setViewport(x, H - y - h, w, h); renderer.setScissor(x, H - y - h, w, h);
  renderer.render(scene, cam);
}
const lab = document.createElement('div'); lab.className = 'lab'; lab.style.left = '10px'; lab.style.top = '8px';
lab.textContent = V.name + '  ' + V.size[0] + 'x' + V.size[2] + '  ' + V.buildings.length + ' buildings  ' + V.residents + ' residents';
document.body.appendChild(lab);
</script></body></html>"""


def render(name, size=(1800, 1200)):
    data = (HERE / 'out' / f'{name}.json').read_text()
    html = (PAGE.replace('__THREE__', THREE).replace('__VIEWER__', (HERE.parent / 'buildings' / 'viewer.js').read_text(encoding='utf-8'))
            .replace('__DATA__', data))
    return shoot(html, str(HERE / 'out' / f'{name}.png'), size)


if __name__ == '__main__':
    for n in sys.argv[1:]:
        print(render(n))
