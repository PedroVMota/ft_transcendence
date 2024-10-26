import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.module.min.js';

export default class PlayerCamera {
    constructor(camera, playerPaddle, pcPaddle, isPlayerRed) {
        this.camera = camera;
        this.playerPaddle = playerPaddle;
        this.pcPaddle = pcPaddle;
        this.isPlayerRed = isPlayerRed;
        // Ajusta o offset para uma vista mais angular e inclinada
        this.offset = new THREE.Vector3(0, 10, 20); // Mais elevado e afastado
    }

    update() {
        // Posição da câmera atrás do paddle correto (jogador ou PC)
        const targetPaddle = this.isPlayerRed ? this.playerPaddle : this.pcPaddle;
        
        // Atualiza a posição da câmera para seguir o paddle
        this.camera.position.x = targetPaddle.mesh.position.x;
        this.camera.position.y = targetPaddle.mesh.position.y + this.offset.y;
        this.camera.position.z = targetPaddle.mesh.position.z + this.offset.z;

        // A câmera olha para o centro da cena
        this.camera.lookAt(new THREE.Vector3(0, 0, 0));
    }
}