import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';
import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";

class Paddle {
    constructor(positionY, color = 0x00ff00) {
        this.geometry = new THREE.BoxGeometry(1, 0.2, 0.1);
        this.material = new THREE.MeshBasicMaterial({ color: color });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.mesh.position.y = positionY;
    }

    move(direction) {
        this.mesh.position.x += direction * 0.1;
    }
}

class Ball {
    constructor() {
        this.geometry = new THREE.SphereGeometry(0.1, 32, 32);
        this.material = new THREE.MeshBasicMaterial({ color: 0xffffff });
        this.mesh = new THREE.Mesh(this.geometry, this.material);
        this.speed = { x: 0.05, y: 0.05 };
    }

    update() {
        this.mesh.position.x += this.speed.x;
        this.mesh.position.y += this.speed.y;

        if (this.mesh.position.x > 4.5 || this.mesh.position.x < -4.5) {
            this.speed.x = -this.speed.x;
        }
        if (this.mesh.position.y > 2.5 || this.mesh.position.y < -2.5) {
            this.speed.y = -this.speed.y;
        }
    }

    checkCollision(paddle) {
        if (this.mesh.position.y - 0.1 <= paddle.mesh.position.y + 0.1 &&
            this.mesh.position.y + 0.1 >= paddle.mesh.position.y - 0.1 &&
            this.mesh.position.x + 0.1 >= paddle.mesh.position.x - 0.5 &&
            this.mesh.position.x - 0.1 <= paddle.mesh.position.x + 0.5) {
            this.speed.y = -this.speed.y;
        }
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
        let paddle1, paddle2, ball;

        const init = () => {
            scene = new THREE.Scene();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 5;

            renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            this.#parentElement.appendChild(renderer.domElement); // Anexa o canvas ao elemento root

            // Criação das raquetes e da bola
            paddle1 = new Paddle(-2.5);
            paddle2 = new Paddle(2.5, 0xff0000);
            ball = new Ball();

            // Adicionando à cena
            scene.add(paddle1.mesh);
            scene.add(paddle2.mesh);
            scene.add(ball.mesh);

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
            if (event.key === 'ArrowLeft') movePaddle1(-1);
            if (event.key === 'ArrowRight') movePaddle1(1);
            if (event.key === 'a') movePaddle2(-1);
            if (event.key === 'd') movePaddle2(1);
        });

        window.addEventListener('keyup', (event) => {
            if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') movePaddle1(0);
            if (event.key === 'a' || event.key === 'd') movePaddle2(0);
        });

        init(); // Inicializa o jogo
    }

    destroy() {
        this.#parentElement.innerHTML = "";
    }
}