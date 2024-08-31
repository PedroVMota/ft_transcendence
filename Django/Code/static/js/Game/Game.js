import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";

export default class Game extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #cachedContent = null;
    #cachedHead = null;

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
        // Código do jogo Pong utilizando three.js
        let scene, camera, renderer;
        let paddle1, paddle2, ball;
        let paddle1Speed = 0, paddle2Speed = 0;
        let ballSpeedX = 0.05, ballSpeedY = 0.05;

        // Inicialização da cena e objetos do jogo
        function init() {
            scene = new THREE.Scene();

            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
            camera.position.z = 5;

            renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            document.getElementById('root').appendChild(renderer.domElement); // Anexa o canvas ao elemento root

            let paddleGeometry = new THREE.BoxGeometry(1, 0.2, 0.1);
            let paddleMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });

            paddle1 = new THREE.Mesh(paddleGeometry, paddleMaterial);
            paddle1.position.y = -2.5;
            scene.add(paddle1);

            paddle2 = new THREE.Mesh(paddleGeometry, paddleMaterial);
            paddle2.position.y = 2.5;
            scene.add(paddle2);

            let ballGeometry = new THREE.SphereGeometry(0.1, 32, 32);
            let ballMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });
            ball = new THREE.Mesh(ballGeometry, ballMaterial);
            scene.add(ball);

            animate();
        }

        function animate() {
            requestAnimationFrame(animate);

            paddle1.position.x += paddle1Speed;
            paddle2.position.x += paddle2Speed;

            ball.position.x += ballSpeedX;
            ball.position.y += ballSpeedY;

            if (ball.position.x > 4.5 || ball.position.x < -4.5) {
                ballSpeedX = -ballSpeedX;
            }
            if (ball.position.y > 2.5 || ball.position.y < -2.5) {
                ballSpeedY = -ballSpeedY;
            }

            renderer.render(scene, camera);
        }

        function movePaddle1(direction) {
            paddle1Speed = direction * 0.1;
        }

        function movePaddle2(direction) {
            paddle2Speed = direction * 0.1;
        }

        // Controles das raquetes
        window.addEventListener('keydown', function (event) {
            if (event.key === 'ArrowLeft') movePaddle1(-1);
            if (event.key === 'ArrowRight') movePaddle1(1);
            if (event.key === 'a') movePaddle2(-1);
            if (event.key === 'd') movePaddle2(1);
        });

        window.addEventListener('keyup', function (event) {
            if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') movePaddle1(0);
            if (event.key === 'a' || event.key === 'd') movePaddle2(0);
        });

        init(); // Inicializa o jogo
    }

    destroy(){
        this.#parentElement.innerHTML = "";
    }
}
