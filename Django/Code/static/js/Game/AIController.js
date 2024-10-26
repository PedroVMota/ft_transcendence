// AIController.js
export default class AIController {
    constructor(paddle, ball, opponentPaddle, baseSpeed = 0.5) {
        this.paddle = paddle; // Paddle controlado pela IA
        this.ball = ball; // Referência à bola no jogo
        this.opponentPaddle = opponentPaddle; // Paddle do oponente (jogador humano)
        this.baseSpeed = baseSpeed; // Velocidade inicial da IA
        this.maxSpeed = 1.0; // Velocidade máxima da IA
        this.collisionCooldown = 20; // Cooldown após colisão
        this.currentCooldown = 0; // Inicializa o cooldown
    }

    // Prever a posição da bola por um número limitado de "passos"
    predictBallPosition(steps = 50) {
        let futureBallPosition = {
            x: this.ball.mesh.position.x,
            y: this.ball.mesh.position.y
        };
        let ballSpeed = { x: this.ball.speed.x, y: this.ball.speed.y };

        // Simular a trajetória da bola por um número limitado de "steps"
        for (let i = 0; i < steps; i++) {
            futureBallPosition.x += ballSpeed.x;
            futureBallPosition.y += ballSpeed.y;

            // Simular colisão com as paredes e inverter a direção
            if (futureBallPosition.y + this.ball.geometry.parameters.radius >= 2.5 || 
                futureBallPosition.y - this.ball.geometry.parameters.radius <= -2.5) {
                ballSpeed.y *= -1; // Inverter a direção Y se colidir com a parede
            }
        }
        return futureBallPosition; // Retorna a posição futura da bola
    }

    // IA tenta redirecionar a bola para onde o oponente não está
    shouldRedirectBall() {
        const opponentY = this.opponentPaddle.mesh.position.y;

        // IA tenta jogar a bola para longe do oponente se estiver perto do centro
        if (Math.abs(opponentY) < 0.5) {
            return true;
        }
        return false;
    }

    update() {
        if (this.currentCooldown > 0) {
            this.currentCooldown--; // Reduzir o cooldown a cada frame
        }

        // Prever a posição da bola
        const predictedPosition = this.predictBallPosition(50);
        const predictedY = predictedPosition.y;

        // Ajustar a velocidade da IA conforme a velocidade da bola, mas com limite
        const ballSpeedFactor = Math.abs(this.ball.speed.x);
        let adjustedSpeed = this.baseSpeed + ballSpeedFactor * 0.5;
        adjustedSpeed = Math.min(adjustedSpeed, this.maxSpeed); // Limitar a velocidade da IA

        // Movimentar o paddle da IA com base na previsão da posição da bola
        if (predictedY > this.paddle.mesh.position.y + 0.1) {
            this.paddle.move(adjustedSpeed); // Mover paddle para cima
        } else if (predictedY < this.paddle.mesh.position.y - 0.1) {
            this.paddle.move(-adjustedSpeed); // Mover paddle para baixo
        }

        // Verificar colisão e aplicar cooldown
        if (this.ball.checkCollision(this.paddle)) {
            this.currentCooldown = this.collisionCooldown; // Aplicar cooldown após colisão

            // Redirecionar a bola para longe do oponente
            if (this.shouldRedirectBall()) {
                if (this.opponentPaddle.mesh.position.y < 0) {
                    this.ball.speed.y = Math.abs(this.ball.speed.y); // Enviar a bola para cima
                } else {
                    this.ball.speed.y = -Math.abs(this.ball.speed.y); // Enviar a bola para baixo
                }
            }
        }
    }
}