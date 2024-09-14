import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';
import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";
import Wall from './Wall.js';
import Paddle from './Paddle.js';
import Ball from './Ball.js';


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