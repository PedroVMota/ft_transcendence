//depencies
import * as THREE from 'three';


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
    
        // Colisão com as laterais (eixo X) - Pode ser para resetar o jogo ou marcar pontos
        if (this.mesh.position.x + this.geometry.parameters.radius >= 4.5 ||
            this.mesh.position.x - this.geometry.parameters.radius <= -4.5) {
            this.reset();
        }
    }
    
    reset() {
        // Reseta a posição da bola ao centro
        this.mesh.position.set(0, 0, 0);
        // Define a velocidade inicial (pode ser alterada para uma direção aleatória)
        this.speed = { x: 0.01, y: 0.01 };
    }

    checkCollision(paddle) {
        // Verifica colisão no eixo X (horizontalmente) com o paddle
        if (this.mesh.position.x - this.geometry.parameters.radius <= paddle.mesh.position.x + paddle.geometry.parameters.width / 2 &&
            this.mesh.position.x + this.geometry.parameters.radius >= paddle.mesh.position.x - paddle.geometry.parameters.width / 2) {
            
            // Verifica colisão no eixo Y (verticalmente) com o paddle
            if (this.mesh.position.y - this.geometry.parameters.radius <= paddle.mesh.position.y + paddle.geometry.parameters.height / 2 &&
                this.mesh.position.y + this.geometry.parameters.radius >= paddle.mesh.position.y - paddle.geometry.parameters.height / 2) {
                
                // Inverte a direção da bola no eixo X (rebatida)
                this.speed.x *= -1;
                // Aumenta a velocidade da bola quando há contacto com o padle
                this.speed.x += this.speed.x > 0 ? 0.01 : -0.01;
                this.speed.y += this.speed.y > 0 ? 0.01 : -0.01;
                return true;
            }
        }
        return false;
    }
}

