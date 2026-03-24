import os
import re

template_dir = r"C:\Users\asus0\OneDrive\Desktop\Documents\new_app2-main\Smart_Vehicle_Procurement_System_using_Blockchain_Technology\Templates"

new_threejs_script = """<!-- Three.js Script for 3D Animation -->
<script>
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('three-canvas'), alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);

    function createEmojiSprite(emoji) {
      const canvas = document.createElement('canvas');
      canvas.width = 128;
      canvas.height = 128;
      const ctx = canvas.getContext('2d');
      ctx.font = '90px Arial';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(emoji, 64, 64);
      const texture = new THREE.CanvasTexture(canvas);
      const material = new THREE.SpriteMaterial({ map: texture, transparent: true, opacity: 0.6 });
      const sprite = new THREE.Sprite(material);
      sprite.scale.set(3.5, 3.5, 1);
      return sprite;
    }

    const emojis = ['🚗', '🚌', '🚲', '🏎️', '🚙', '🛵', '🚛'];
    const shapes = [];

    for (let i = 0; i < 50; i++) {
      const emoji = emojis[Math.floor(Math.random() * emojis.length)];
      const mesh = createEmojiSprite(emoji);
      mesh.position.set((Math.random()-0.5)*70, (Math.random()-0.5)*40, (Math.random()-0.5)*40);
      scene.add(mesh);
      shapes.push({ mesh, vx: (Math.random()-0.5)*0.04, vy: (Math.random()-0.5)*0.03, s: Math.random()*0.02 });
    }
    camera.position.z = 35;

    let time = 0;
    function animate() {
      requestAnimationFrame(animate);
      time += 0.01;
      shapes.forEach((item, index) => {
        item.mesh.position.x += item.vx;
        item.mesh.position.y += item.vy;
        item.mesh.position.y += Math.sin(time + index) * 0.02; // floating effect
        
        if (item.mesh.position.x > 35) item.mesh.position.x = -35;
        if (item.mesh.position.x < -35) item.mesh.position.x = 35;
        if (item.mesh.position.y > 22) item.mesh.position.y = -22;
        if (item.mesh.position.y < -22) item.mesh.position.y = 22;
      });
      renderer.render(scene, camera);
    }
    animate();

    window.addEventListener('resize', () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    });
</script>"""

# We look for the Three.js comment and everything up to the closing </script>
pattern = re.compile(r"<!-- Three\.js Script for 3D Animation -->.*?</script>", re.DOTALL)

fixed = 0
for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            fp = os.path.join(root, file)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            new_content = pattern.sub(new_threejs_script, content)
            
            if new_content != content:
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                fixed += 1
                print(f"Added Emojis to: {fp}")

print(f"\nDone. Added emojis background to {fixed} files.")
