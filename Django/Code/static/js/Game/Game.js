import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';
import AComponent from "../Spa/AComponent.js";
import spa from "../Spa/Spa.js";
import { getCookie, Requests } from "../Utils/Requests.js";
import Wall from './Wall.js';
import Paddle from './Paddle.js';
import Ball from './Ball.js';
import AIController from './AIController.js'; // Importa a classe da IA

export default class Game extends AComponent {
    #parentElement = null;
    #spaObject = null;
    #gameflag = false;
    #controls = null;
    #isMouseDown = false;  // Flag para capturar quando o botão do rato está pressionado
    #mouseX = 0;           // Captura a posição do mouse no eixo X
    #mouseY = 0;           // Captura a posição do mouse no eixo Y
    #cameraRotationSpeed = 0.005;  // Define a velocidade de rotação da câmera
    #aiController = null;// Referência à IA
    #socket = null;
    #playerID = 0 // todo -> make this actually represent player and not be a static
    #paddleOne = null;
    #paddleTwo = new Paddle(4.5, 0xff0000);
    #ball = null;
    #coOp = true
    #finished = false

    constructor(url, spaObject, coop=true, gameId=null) {
        super(url, spaObject);
        this.#parentElement = document.getElementById("root");
        this.#spaObject = spaObject;
        this.#coOp = coop;
        const savedColor = localStorage.getItem('selectedColor') || '#00ff00'; // Default to green if no color is saved
        this.#paddleOne = new Paddle(-4.5, savedColor);

        const savedBallColor = localStorage.getItem('ballColor') || '#ffffff'; // Default to white if no color is saved
        this.#ball = new Ball(savedBallColor);
        let protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        if (gameId != null){
            this.#socket = new WebSocket(`${protocol}://` + window.location.host + "/ws/Game/" + gameId);
        }
        else
        {
             this.#socket = new WebSocket(`${protocol}://` + window.location.host + "/ws/Monitor/Game/");
        }

        this.#socket.onmessage = (e) =>{
            const data = JSON.parse(e.data);
            const message = data['message'];

            const updateScoreBar = (playerOne, playerTwo) =>
            {
                let pOneName = document.getElementById("player-one-name");
                let pOneScore = document.getElementById("player-one-score");
                let pTwoName = document.getElementById("player-two-name");
                let pTwoScore = document.getElementById("player-two-score");

                pOneName.textContent = playerOne['name'];
                pOneScore.textContent = playerOne['score'];

                pTwoName.textContent = playerTwo['name'];
                pTwoScore.textContent = playerTwo['score'];
            }

            const updateGameState = (data) =>
            {
                this.#paddleOne.setPercentage(data['playerOne']);
                this.#paddleTwo.setPercentage(data['playerTwo']);
                const ballData = data['ball'];
                this.#ball.update(ballData['x'], ballData['y']);

                console.log("updateGameState")
            }

            if (data['action'] === 'score-bar-report')
            {
                updateScoreBar(data['playerOne'], data['playerTwo']);
            }
            if (data['action'] === 'game-state-report')
            {
                updateGameState(data)
            }
            if (data['action'] === 'game-win')
            {
                console.log("winning player was: ", data["victoriousPlayer"])
            }
        };

        this.#socket.onclose =  (e) =>
        {
            this.#finished = true;
        }
    }


    render() {
        if (this.#gameflag) return; // Prevent re-initializing the game
        this.#gameflag = true;
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
        let wallTop, wallBottom;
        const iaSpeed = 0.1; // Velocidade de movimentação da IA
        
            const init = () => {
            scene = new THREE.Scene();
            // Defina a posição e rotação da câmera para ficar inclinada atrás dos paddles
            camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 1, 1000);
            camera.position.set(0, 0, 10); // Posição mais centrada e elevada
            camera.lookAt(new THREE.Vector3(0, 0, 0)); // Mira no centro da cena
            
            
            renderer = new THREE.WebGLRenderer();
            renderer.setSize(window.innerWidth, window.innerHeight);
            this.#parentElement.appendChild(renderer.domElement); // Anexa o canvas ao elemento root

            // Criação das paredes superior e inferior
            wallTop = new Wall(2.5); // Parede superior
            wallBottom = new Wall(-2.5); // Parede inferior
            
            // Adicionando à cena
            scene.add(this.#paddleOne.mesh);
            scene.add(this.#paddleTwo.mesh);
            scene.add(this.#ball.mesh);
            scene.add(wallTop.mesh);
            scene.add(wallBottom.mesh);
            handleCameraControls();
            
            this.#aiController = new AIController(this.#paddleTwo, this.#ball, this.#paddleOne, iaSpeed);   // Instancia da AI com paddle adversário

            animate();
        }
        const printCameraPositionAndRotation = () => {
            //console.log(`Posição da câmera: X = ${camera.position.x}, Y = ${camera.position.y}, Z = ${camera.position.z}`);
            //console.log(`Rotação da câmera: X = ${camera.rotation.x}, Y = ${camera.rotation.y}, Z = ${camera.rotation.z}`);
        }
        const moveCameraToPaddleTwo = () => {
            camera.position.set(8.5, -2.275957200481571e-15, -1.6);  // Coordenadas da posição
            camera.rotation.set(-1.571, 1.571, 0);  // Coordenadas da rotação
            console.log("Câmera movida para trás do paddle vermelho.");
        };

        const moveCameraToPaddleOne = () => {
            camera.position.set(-8.5, -2.275957200481571e-15, -1.6);
            camera.rotation.set(-1.571, -1.571, 0);
            console.log("Câmera movida para trás do lado verde")
        }

        const requestUpdateScoreBar = () => {
            this.#socket.send(JSON.stringify({
                'action': "score-bar-update-request",
            }));
        }

        const requestGameState = () => {
            this.#socket.send(JSON.stringify({
                'action': "game-state-request"
            }))
        }

        const checkForVictories = () => {
            this.#socket.send(JSON.stringify({
                'action': "check-for-victory"
            }))
        }
        
        const animate = () => {
            requestAnimationFrame(animate);

            if (true)
            {
                requestUpdateScoreBar();

                requestGameState();

                checkForVictories();
            }
    
            renderer.render(scene, camera);
        }
    
        const movePaddle1 = (direction) => {
            this.#socket.send(JSON.stringify({
                    'action': "paddle-move-notification",
                    'player': 0,
                    'direction': direction
                }
            ))
        }

        const movePaddle2 = (direction) => {
            let gameID = 3;
            this.#socket.send(JSON.stringify({
                    'action': "paddle-move-notification",
                    'player': 0,
                }
            ))
        }

        const moveAgnosticPaddle = (direction) => {
            this.#socket.send(JSON.stringify({
                    'action': "paddle-move-notification",
                    'direction': direction
                }
            ))
        }

        const handleCameraControls = () => {
            window.addEventListener('keydown', (event) => {
                const cameraSpeed = 0.2; // Velocidade de movimentação da câmera
                const rotationSpeed = 0.05; // Velocidade de rotação da câmera

                let cameraMoved = false; // Verifica se a câmera se moveu

                switch (event.key)
                {
                    case 'p':
                        console.log("sending to web socket")
                        this.#socket.send(JSON.stringify({
                            'action': 'request-pause-play'
                        }))

                    case 'q':
                        camera.position.set(0, 0, 10);
                        camera.lookAt(new THREE.Vector3(0, 0, 0)); // Mira no centro da cena
                        break;


                    case 'n':
                    camera.position.x -= cameraSpeed; // Move a câmera para frente
                    cameraMoved = true;
                    break;
                case 'm':
                    camera.position.x += cameraSpeed; // Move a câmera para trás
                    cameraMoved = true;
                    break;
                case 'j':
                    camera.position.y -= cameraSpeed; // Move a câmera para a esquerda
                    cameraMoved = true;
                    break;
                case 'k':
                    camera.position.y += cameraSpeed; // Move a câmera para a direita
                    cameraMoved = true;
                    break;
                case 'z':
                    camera.position.z += cameraSpeed; // Move a câmera para trás
                    cameraMoved = true;
                    break;

                    case 'e':
                        camera.rotation.x -= 0.05; // Rotaciona a câmera para cima
                        cameraMoved = true;
                        break;
                    case 'r':
                        camera.rotation.x += 0.05; // Rotaciona a câmera para baixo
                        cameraMoved = true;
                        break;
                    case 't':
                        camera.rotation.y -= 0.05; // Rotaciona a câmera para a esquerda
                        cameraMoved = true;
                        break;
                    case 'y':
                        camera.rotation.y += 0.05; // Rotaciona a câmera para a direita
                        cameraMoved = true;
                        break;
                        case 'b':
                            camera.rotation.z -= 0.05; // Rotaciona a câmera para a esquerda
                            cameraMoved = true;
                            break;
                        case 'v':
                            camera.rotation.z += 0.05; // Rotaciona a câmera para a direita
                            cameraMoved = true;
                            break;

                }
                if (cameraMoved) {
                    // Imprime as coordenadas da câmera e sua rotação
                    printCameraPositionAndRotation();
                }

                // Atualiza o render após mudar a posição/rotação
                renderer.render(scene, camera);
            });
        }
    
        // Controles das raquetes
        window.addEventListener('keydown', (event) => {


            if (event.key === 'ArrowUp') {
                printCameraPositionAndRotation();
                if (this.#coOp)
                {
                    movePaddle1(1);
                }
                else
                {
                    moveAgnosticPaddle(1);
                }
                event.preventDefault(); // Impede o comportamento padrão da seta (scroll)
            }
            if (event.key === 'ArrowDown') {
                printCameraPositionAndRotation();
                if (this.#coOp)
                {
                    movePaddle1(-1);
                }
                else
                {
                    moveAgnosticPaddle(-1);
                }
                event.preventDefault(); // Impede o comportamento padrão da seta (scroll)
            }
            if (event.key === 'w' || event.key === 'W') {
                printCameraPositionAndRotation();
                if (this.#coOp)
                {
                    movePaddle2(1);
                }
                else
                {
                    moveAgnosticPaddle(1);
                }
            }
            if (event.key === 's' || event.key === 'S') {
                printCameraPositionAndRotation();
                if (this.#coOp)
                {
                    movePaddle2(-1);
                }
                else
                {
                    moveAgnosticPaddle(-1);
                }
            }
            if (event.key === 'z') {
                // Zoom in (aproxima da cena)
                camera.position.z -= 2;  // Ajusta a distância da câmara
                event.preventDefault();
            }
            if (event.key === 'x') {
                // Zoom out (afasta da cena)
                camera.position.z += 2;  // Ajusta a distância da câmara
                event.preventDefault();
            }
            if (event.key === 'c') {
                moveCameraToPaddleTwo();
                printCameraPositionAndRotation();
                event.preventDefault();
            }
            if (event.key === 'l') {
                moveCameraToPaddleOne();
                printCameraPositionAndRotation();
                event.preventDefault();
            }
            window.addEventListener('mousedown', (event) => {
                if (event.button === 0) {  // Botão esquerdo do rato
                    this.#isMouseDown = true;
                    this.#mouseX = event.clientX;
                    this.#mouseY = event.clientY;
                }
            });

            window.addEventListener('mouseup', () => {
                this.#isMouseDown = false;
            });

            window.addEventListener('mousemove', (event) => {
                if (this.#isMouseDown) {
                    const deltaX = event.clientX - this.#mouseX;
                    const deltaY = event.clientY - this.#mouseY;

                    // Ajusta a rotação da câmera com base no movimento do rato
                    camera.rotation.y -= deltaX * this.#cameraRotationSpeed;  // Rotação no eixo Y (horizontal)
                    camera.rotation.x -= deltaY * this.#cameraRotationSpeed;  // Rotação no eixo X (vertical)

                    this.#mouseX = event.clientX;
                    this.#mouseY = event.clientY;
                }
            });
        });
        
    
        init(); // Inicializa o jogo
    }
    

    destroy() {
        this.#parentElement.innerHTML = "";
    }
}