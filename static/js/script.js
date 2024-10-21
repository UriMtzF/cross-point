// Función para mostrar las sublistas en la tabla
function displaySublistInTable(generations, best) {
  const tableBody = document.querySelector("#process-table tbody");
  tableBody.innerHTML = "";  // Limpiar contenido previo de la tabla

  const bestFit = document.getElementById("population-text");
  let binarios = "";
  best["binario"].forEach(subitem => {
    binarios += subitem + " ";
  });
  bestFit.textContent = "Mejor individuo binario: " + binarios + "\n" + "Fitness: " + best["fitness"];

  for (let i = 0; i < generations.length; i++) {
    const row = document.createElement("tr");

    const genCell = document.createElement("td");
    const maxCell = document.createElement("td");
    const maxFitnessCell = document.createElement("td");

    const maxPre = document.createElement("pre");
    const maxFitPre = document.createElement("pre");

    let maxGen = "";
    let maxFit = "";

    generations[i]["poblacion"].forEach(sublist => {
      maxGen += "[" + sublist.join(", ") + "]\n";
    });

    generations[i]["fitness"].forEach(sublist => {
      maxFit += sublist + "\n";
    });

    maxPre.textContent = maxGen;
    maxFitPre.textContent = maxFit;

    genCell.textContent = i;
    maxCell.appendChild(maxPre);
    maxFitnessCell.appendChild(maxFitPre);

    row.appendChild(genCell);
    row.appendChild(maxCell);
    row.appendChild(maxFitnessCell);

    tableBody.appendChild(row);
  }
}

// Función para generar la población y mostrarla
function generatePopulationAndDisplay() {

  // Usar el número seleccionado en la URL de fetch
  fetch('http://localhost:8000/api/get-population')
    .then(response => response.json())
    .then(data => {
      const generations = data['data']['generaciones'];
      const best = data['data']['mejor_individuo'];
      displaySublistInTable(generations, best);
    })
    .catch(error => { console.error('Error: ', error); });
}

// Asignar el evento al botón "INICIAR"
document.getElementById("start").addEventListener("click", function () {
  // Llamar a la función que genera la población y la muestra
  generatePopulationAndDisplay();
});