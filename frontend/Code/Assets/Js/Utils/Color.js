export class Color{
    static componentToHex(c) {
        var hex = c.toString(16);
        return hex.length == 1 ? "0" + hex : hex;
    }

    static RGBToHex(r, g, b){
        return "#" + this.componentToHex(r) + this.componentToHex(g) + this.componentToHex(b);
    }

    static HexToRGB(hex){
        var r = parseInt(hex.substring(1, 3), 16);
        var g = parseInt(hex.substring(3, 5), 16);
        var b = parseInt(hex.substring(5, 7), 16);
        return [r, g, b];
    }

    static HexToRGBA(hex, alpha){
        var rgb = this.HexToRGB(hex);
        return `rgba(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${alpha})`;
    }

    static RGBToRGBA(r, g, b, alpha){
        return `rgba(${r}, ${g}, ${b}, ${alpha})`;
    }

    static LinearGradient(angle, ...colors) {
        let gradient = `linear-gradient(${angle}deg`;
        for (const color of colors) {
            gradient += `, ${color}`;
        }
        gradient += `)`;
        return gradient;
    }

    static RadialGradient(shape, ...colors) {
        let gradient = `radial-gradient(${shape}`;
        for (const color of colors) {
            gradient += `, ${color}`;
        }
        gradient += `)`;
        return gradient;
    }
}