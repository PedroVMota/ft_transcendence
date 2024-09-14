// Dependencies
import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';


export default class Paddle {
    constructor(positionX, color = 0x00ff00) {
        this.geometry = new THREE.BoxGeometry(0.2, 1, 0.1);
        this.material = new THREE.MeshBasicMaterial({ color: color });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.x = positionX;
    }

    move(direction) {
        // Limitar o movimento do paddle dentro da área de jogo
        let newPosition = this.mesh.position.y + direction * 0.1;
        if (newPosition + 0.5 <= 2.5 && newPosition - 0.5 >= -2.5) { // Limites superior e inferior
            this.mesh.position.y = newPosition;
        }
    }
}