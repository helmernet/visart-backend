const express = require("express");
const cors = require("cors");
const app = express();

app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("✅ Backend de SolarCalc funcionando correctamente.");
});

app.post("/api/calculo", (req, res) => {
  const {
    consumoMensual,
    costoEnergia,
    ciudad,
    sistemaConBateria
  } = req.body;

  const radiacionSolarPorCiudad = {
    Bogotá: 4.5,
    Medellín: 5.0,
    Cali: 5.5,
    Barranquilla: 6.0,
    Bucaramanga: 5.3,
  };

  const radiacion = radiacionSolarPorCiudad[ciudad] || 5.0;
  const eficienciaSistema = sistemaConBateria ? 0.70 : 0.85;

  const consumoDiario = consumoMensual / 30;
  const energiaRequeridaDiaria = consumoDiario / eficienciaSistema;

  const potenciaSistemaKWp = energiaRequeridaDiaria / radiacion;
  const cantidadPaneles = Math.ceil((potenciaSistemaKWp * 1000) / 410);

  const costoPanel = 800000;
  const costoInversor = 4000000;
  const costoBateria = sistemaConBateria ? 6000000 : 0;
  const costoInstalacion = 1500000;

  const costoTotal =
    cantidadPaneles * costoPanel +
    costoInversor +
    costoBateria +
    costoInstalacion;

  const ahorroMensual = consumoMensual * costoEnergia;
  const tiempoRetorno = Math.ceil(costoTotal / ahorroMensual);

  const resultado = {
    ciudad,
    consumoMensual,
    sistemaConBateria,
    radiacion,
    eficienciaSistema,
    consumoDiario,
    energiaRequeridaDiaria,
    potenciaSistemaKWp: potenciaSistemaKWp.toFixed(2),
    cantidadPaneles,
    costoTotal,
    ahorroMensual,
    tiempoRetorno
  };

  res.json(resultado);
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Servidor backend de SolarCalc corriendo en el puerto ${PORT}`);
});
