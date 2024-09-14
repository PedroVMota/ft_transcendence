//dependencies
import * as THREE from 'three';

export default class Wall {
    constructor(positionY, width = 10, height = 0.1, color = 0xffffff) {
        this.geometry = new THREE.BoxGeometry(width, height, 0.1);
        this.material = new THREE.MeshBasicMaterial({ color: color });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.y = positionY;
    }
}