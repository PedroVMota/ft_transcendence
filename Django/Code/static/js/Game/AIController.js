// AIController.js
export default class AIController {
    constructor(paddle, ball, speed = 0.05) {
        this.paddle = paddle; // Paddle controlado pela IA
        this.ball = ball; // Referência à bola no jogo
        this.speed = speed; // Velocidade de movimentação da IA
        this.recentCollision = false; // Evitar colisões repetidas
        this.collisionCooldown = 20; // Frames de cooldown após uma colisão
        this.currentCooldown = 0;
    }

    update() {
        if (this.currentCooldown > 0) {
            this.currentCooldown--; // Diminuir cooldown a cada frame
        }

        // Só move o paddle se não estiver em cooldown
        if (this.currentCooldown === 0) {
            // Prever a posição da bola
            const futureBallY = this.ball.mesh.position.y;

            // Mover o paddle para a posição da bola, mas limitando a velocidade
            if (futureBallY > this.paddle.mesh.position.y + 0.1) {
                this.paddle.move(this.speed); // Mover para cima
            } else if (futureBallY < this.paddle.mesh.position.y - 0.1) {
                this.paddle.move(-this.speed); // Mover para baixo
            }
        }

        // Verificar colisão entre o paddle e a bola
        if (this.ball.checkCollision(this.paddle)) {
            this.currentCooldown = this.collisionCooldown; // Iniciar cooldown de colisão
        }
    }
}
