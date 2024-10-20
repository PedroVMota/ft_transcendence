import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';

export default class Ball {
    constructor() {
        this.geometry = new THREE.SphereGeometry(0.1, 32, 32);
        this.material = new THREE.MeshBasicMaterial({ color: 0xffffff });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.speed = { x: 0.01, y: 0.01 };
    }

    update() {
        this.mesh.position.x += this.speed.x;
        this.mesh.position.y += this.speed.y;
    
        // Colisão com as paredes superior e inferior (eixo Y)
        if (this.mesh.position.y + this.geometry.parameters.radius >= 2.5 ||
            this.mesh.position.y - this.geometry.parameters.radius <= -2.5) {
            this.speed.y *= -1; // Inverte a direção no eixo Y ao colidir com uma parede
        }
    
        // Colisão com as laterais (eixo X)
        if (this.mesh.position.x + this.geometry.parameters.radius >= 4.5 ||
            this.mesh.position.x - this.geometry.parameters.radius <= -4.5) {
            this.reset();
        }
    }
    
    reset() {
        // Reseta a posição da bola ao centro
        this.mesh.position.set(0, 0, 0);
        // Define a velocidade inicial (pode ser aleatória)
        this.speed = { x: 0.01, y: 0.01 };
    }

    checkCollision(paddle) {
        if (this.mesh.position.x - this.geometry.parameters.radius <= paddle.mesh.position.x + paddle.geometry.parameters.width / 2 &&
            this.mesh.position.x + this.geometry.parameters.radius >= paddle.mesh.position.x - paddle.geometry.parameters.width / 2) {
            
            if (this.mesh.position.y - this.geometry.parameters.radius <= paddle.mesh.position.y + paddle.geometry.parameters.height / 2 &&
                this.mesh.position.y + this.geometry.parameters.radius >= paddle.mesh.position.y - paddle.geometry.parameters.height / 2) {
                
                // Apenas inverte a direção se a bola estiver realmente se movendo em direção ao paddle
                if (this.speed.x < 0 && this.mesh.position.x < 0 || this.speed.x > 0 && this.mesh.position.x > 0) {
                    this.speed.x *= -1; // Inverte a direção no eixo X
                    this.speed.x += this.speed.x > 0 ? 0.01 : -0.01; // Aumenta a velocidade a cada colisão
                    this.speed.y += this.speed.y > 0 ? 0.01 : -0.01; // Aumenta a velocidade no eixo Y também
                }
                
                return true;
            }
        }
        return false;
    }
    
}
