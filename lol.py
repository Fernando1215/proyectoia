from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
import json

app = FastAPI()

class Pregunta(BaseModel):
    q: str
    o: list[str]
    c: int

preguntas = [
    Pregunta(q="¿Qué es el MAS?", o=["Rectilíneo","Circular","Oscilatorio","Constante"], c=2),
    Pregunta(q="¿Qué representa k?", o=["Masa","Constante del resorte","Tiempo","Velocidad"], c=1),
    Pregunta(q="Tipo de movimiento?", o=["Lineal","Oscilatorio","Uniforme","Aleatorio"], c=1),
    Pregunta(q="Ley de Hooke?", o=["F=-kx","F=mv","F=ma","F=k"], c=0),
    Pregunta(q="Signo negativo?", o=["Error","Fuerza cero","Se opone","No importa"], c=2),
    Pregunta(q="Amplitud?", o=["Tiempo","Velocidad","Desplazamiento máximo","Masa"], c=2),
    Pregunta(q="Si k aumenta?", o=["Más lento","Más rápido","Se detiene","No cambia"], c=1),
    Pregunta(q="Ecuación MAS?", o=["x=t","x+1=0","m x''+kx=0","v=at"], c=2),
    Pregunta(q="Forma del movimiento?", o=["Lineal","Exponencial","Periódica","Aleatoria"], c=2),
]

@app.get("/", response_class=HTMLResponse)
def quiz():

    html = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Quiz MAS</title>

<style>

body{
font-family:Segoe UI;
background:linear-gradient(135deg,#1e1e2f,#3a3a6a);
color:white;
margin:0;
}

.container{
max-width:800px;
margin:30px auto;
background:#2c2c54;
padding:20px;
border-radius:15px;
box-shadow:0 10px 30px black;
}

h1{
text-align:center;
color:#00d4ff;
}

.options label{
display:block;
background:#40407a;
padding:10px;
margin:5px 0;
border-radius:8px;
cursor:pointer;
}

.options label:hover{
background:#706fd3;
}

button{
background:#00d4ff;
border:none;
padding:10px 20px;
border-radius:8px;
cursor:pointer;
}

.progress{
width:100%;
height:10px;
background:#555;
border-radius:5px;
margin-bottom:20px;
}

.progress-bar{
height:10px;
background:#00d4ff;
width:0%;
}

</style>
</head>

<body>

<div class="container">

<h1>Quiz Movimiento Armónico Simple</h1>

<div class="progress">
<div class="progress-bar" id="barra"></div>
</div>

<div id="quiz"></div>

<button onclick="siguiente()">Siguiente</button>

<div id="resultado"></div>

<br><br>

<a href="/amortiguamiento" style="color:white">Ver información sobre amortiguamiento</a>

</div>

<script>

const preguntas = """ + str([p.dict() for p in preguntas]) + """;

let actual=0;
let puntos=0;

function mostrar(){

let p=preguntas[actual];

let html="<h3>"+p.q+"</h3>";

p.o.forEach((op,i)=>{

html+=`
<label>
<input type="radio" name="r" value="${i}">
${op}
</label>
`;

});

document.getElementById("quiz").innerHTML=html;

let progreso=(actual/preguntas.length)*100;
document.getElementById("barra").style.width=progreso+"%";

}

function siguiente(){

let r=document.querySelector('input[name="r"]:checked');

if(!r){
alert("Selecciona una respuesta");
return;
}

if(parseInt(r.value)==preguntas[actual].c){
puntos++;
}

actual++;

if(actual<preguntas.length){
mostrar();
}else{

document.getElementById("quiz").innerHTML="";
document.getElementById("resultado").innerHTML=
"Tu puntaje es "+puntos+" de "+preguntas.length;

document.getElementById("barra").style.width="100%";

}

}

mostrar();

</script>

</body>
</html>
"""

    return html


@app.get("/amortiguamiento", response_class=HTMLResponse)
def info():

    return """
<h1>Fuerza de Amortiguamiento</h1>

<h2>¿Qué es?</h2>
<p>Es una fuerza que se opone al movimiento y reduce la velocidad.</p>

<h2>Fórmula</h2>
<p>F = -b·v</p>

<h2>Ecuación diferencial</h2>
<p>m·x'' + b·x' + k·x = 0</p>

<h2>Ejemplo</h2>
<p>Los amortiguadores de un carro evitan que rebote.</p>

<br>
<a href="/">Volver al quiz</a>
"""