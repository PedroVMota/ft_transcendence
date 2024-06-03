var canvas = document.getElementById('canvas');
if(!canvas || canvas === null || canvas === undefined || canvas === 'undefined' || canvas === 'null') {
    console.log('Canvas not found');
}
else{
    canvasas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    var ctx = canvas.getContext('2d');
    
    function Circle(x, y, dx, dy, radius) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.radius = radius;
    
        this.draw = function() {
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            ctx.fillStyle = 'white';
            ctx.fill();
        }
    
        this.update = function() {
            if (this.x + this.radius > innerWidth || this.x - this.radius < 0) {
                this.dx = -this.dx;
            }
    
            if (this.y + this.radius > innerHeight || this.y - this.radius < 0) {
                this.dy = -this.dy;
            }
    
            this.x += this.dx;
            this.y += this.dy;
    
            this.draw();
        }
    }
    
    var circleArray = [];
    
    for (var i = 0; i < 20; i++) {
        var radius = 20;
        var x = Math.random() * (innerWidth - radius * 2) + radius;
        var y = Math.random() * (innerHeight - radius * 2) + radius;
        var dx = (Math.random() - 0.5) * 3 ;
        var dy = (Math.random() - 0.5) * 3;
        circleArray.push(new Circle(x, y, dx, dy, radius));
    }
    
    function animate() {
        requestAnimationFrame(animate);
        ctx.clearRect(0, 0, innerWidth, innerHeight);
    
        for (var i = 0; i < circleArray.length; i++) {
            circleArray[i].update();
        }
    }
    
    // animate();
}