import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';

export default class Ball {
    constructor(color) {
        this.geometry = new THREE.SphereGeometry(0.1, 32, 32);
        this.material = new THREE.MeshBasicMaterial({ color: color });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.speed = { x: 0.01, y: 0.01 };
        this.maxSpeed = 0.05; // Limite máximo de velocidade para a bola
    }

    update(x, y) {
        const nX = 9/200 * x;
        const nY = 4/100 * y;

        this.mesh.position.x = nX - 4.5;
        this.mesh.position.y = nY - 2;
    }

    checkCollision(paddle) {
        if (this.mesh.position.x - this.geometry.parameters.radius <= paddle.mesh.position.x + paddle.geometry.parameters.width / 2 &&
            this.mesh.position.x + this.geometry.parameters.radius >= paddle.mesh.position.x - paddle.geometry.parameters.width / 2) {
            
            if (this.mesh.position.y - this.geometry.parameters.radius <= paddle.mesh.position.y + paddle.geometry.parameters.height / 2 &&
                this.mesh.position.y + this.geometry.parameters.radius >= paddle.mesh.position.y - paddle.geometry.parameters.height / 2) {
                
                // Apenas inverte a direção se a bola estiver realmente se movendo em direção ao paddle
                if (this.speed.x < 0 && this.mesh.position.x < 0 || this.speed.x > 0 && this.mesh.position.x > 0) {
                    this.speed.x *= -1; // Inverte a direção no eixo X

                    // Adiciona variação no ângulo com base na posição da colisão no paddle
                    const collisionOffset = (this.mesh.position.y - paddle.mesh.position.y) / (paddle.geometry.parameters.height / 2);
                    this.speed.y += collisionOffset * 0.02; // Variação na velocidade Y com base na colisão

                    // Aumenta a velocidade levemente, mas limita ao máximo
                    this.speed.x += this.speed.x > 0 ? 0.005 : -0.005;
                    this.speed.y += this.speed.y > 0 ? 0.005 : -0.005;
                }

                return true;
            }
        }
        return false;
    }
}
