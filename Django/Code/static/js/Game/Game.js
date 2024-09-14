import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';
import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";

class Paddle {
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

class Wall {
    constructor(positionY, width = 10, height = 0.1, color = 0xffffff) {
        this.geometry = new THREE.BoxGeometry(width, height, 0.1);
        this.material = new THREE.MeshBasicMaterial({ color: color });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.y = positionY;
    }
}

class Ball {
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


export default class Game extends AComponent {
    #parentElement = null;
    #spaObject = null;

    constructor(url, spaObject) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
    }

    render() {
        let url = this.getUrl();
        this.#parentElement.innerHTML = '<span>Pending...</span>';

        this._getHtml(url).then((html) => {
            let documentResponse = new DOMParser().parseFromString(html, 'text/html');
            let rootContentHtml = documentResponse.getElementById('root').innerHTML;
            if (rootContentHtml) {
                document.head.innerHTML = documentResponse.head.innerHTML;
                this.#parentElement.innerHTML = rootContentHtml;

                setTimeout(() => {
                    this.hideSpinner();
                    this.initializeGame(); // Inicializa o jogo após o conteúdo ser renderizado
                }, 1000);
            }
        }).catch((error) => {
            console.error(error);
        });
    }

    initializeGame() {
        let scene, camera, renderer;
        let paddle1, paddle2, ball, wallTop, wallBottom;
    
        const init = () => {
            scene = new THREE.Scene();
    
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 5;
    
            renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            this.#parentElement.appendChild(renderer.domElement); // Anexa o canvas ao elemento root
    
            // Criação das raquetes e da bola
            paddle1 = new Paddle(-4.5); // Ajusta a posição do paddle1 no lado esquerdo
            paddle2 = new Paddle(4.5, 0xff0000); // Ajusta a posição do paddle2 no lado direito
            ball = new Ball();
    
            // Criação das paredes superior e inferior
            wallTop = new Wall(2.5); // Parede superior
            wallBottom = new Wall(-2.5); // Parede inferior
    
            // Adicionando à cena
            scene.add(paddle1.mesh);
            scene.add(paddle2.mesh);
            scene.add(ball.mesh);
            scene.add(wallTop.mesh);
            scene.add(wallBottom.mesh);
    
            animate();
        }
    
        const animate = () => {
            requestAnimationFrame(animate);
    
            ball.update();
            ball.checkCollision(paddle1);
            ball.checkCollision(paddle2);
    
            renderer.render(scene, camera);
        }
    
        const movePaddle1 = (direction) => {
            paddle1.move(direction);
        }
    
        const movePaddle2 = (direction) => {
            paddle2.move(direction);
        }
    
        // Controles das raquetes
        window.addEventListener('keydown', (event) => {
            if (event.key === 'ArrowUp') movePaddle1(1);
            if (event.key === 'ArrowDown') movePaddle1(-1);
            if (event.key === 'w' || event.key === 'W') movePaddle2(1);
            if (event.key === 's' || event.key === 'S') movePaddle2(-1);
        });
    
        init(); // Inicializa o jogo
    }

    destroy() {
        this.#parentElement.innerHTML = "";
    }
}