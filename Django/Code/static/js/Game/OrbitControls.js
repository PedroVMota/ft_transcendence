import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';

class OrbitControls {
    constructor(camera, domElement) {
        this.camera = camera;
        this.domElement = domElement;
        this.enabled = true;
        this.dampingFactor = 0.1;
        this.enableDamping = true;
        this.enableZoom = true;

        this.target = new THREE.Vector3();

        // Inicializa eventos do rato
        this.initMouseEvents();
    }

    initMouseEvents() {
        this.domElement.addEventListener('mousedown', this.onMouseDown.bind(this));
        this.domElement.addEventListener('mousemove', this.onMouseMove.bind(this));
        this.domElement.addEventListener('mouseup', this.onMouseUp.bind(this));
    }

    onMouseDown(event) {
        this.isDragging = true;
        this.mouseStart = new THREE.Vector2(event.clientX, event.clientY);
    }

    onMouseMove(event) {
        if (this.isDragging) {
            const mouseEnd = new THREE.Vector2(event.clientX, event.clientY);
            const delta = new THREE.Vector2().subVectors(mouseEnd, this.mouseStart);

            this.camera.rotation.y -= delta.x * 0.005;
            this.camera.rotation.x -= delta.y * 0.005;

            this.mouseStart.copy(mouseEnd);
        }
    }

    onMouseUp() {
        this.isDragging = false;
    }

    update() {
        if (this.enableDamping) {
            // Aplica damping para suavizar a rotação
            this.camera.rotation.x *= (1 - this.dampingFactor);
            this.camera.rotation.y *= (1 - this.dampingFactor);
        }
    }
}

export { OrbitControls };
