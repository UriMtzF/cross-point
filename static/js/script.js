// Función para mostrar las sublistas en la tabla
function displaySublistInTable(generations, bestMax, bestMin) {
  const tableBody = document.querySelector("#process-table tbody");
  tableBody.innerHTML = "";  // Limpiar contenido previo de la tabla

  const bestFitText = document.getElementById("population-text");

  // Mostrar mejor individuo para maximización
  let binariosMax = "";
  bestMax["binario"].forEach(subitem => {
    binariosMax += subitem + " ";
  });

  // Mostrar mejor individuo para minimización
  let binariosMin = "";
  bestMin["binario"].forEach(subitem => {
    binariosMin += subitem + " ";
  });

  bestFitText.textContent = `Mejor individuo (Maximización): ${binariosMax}\nFitness Max: ${bestMax["fitness"]}\n\n` +
                            `Mejor individuo (Minimización): ${binariosMin}\nFitness Min: ${bestMin["fitness"]}\n\n` +
                            "Competencias:\n";

  for (let i = 0; i < generations.length; i++) {
    const genData = generations[i];
    let competenciasText = "";
    genData["competencias"].forEach((comp) => {
      competenciasText += `Padre1: ${comp.padre1.join(", ")} compite con Padre2: ${comp.padre2.join(", ")} -> Gana: ${comp.ganador.join(", ")}\n`;
    });
    bestFitText.textContent += `Generación ${genData.generacion}:\n${competenciasText}\n`;

    const row = document.createElement("tr");
    const genCell = document.createElement("td");
    const maxCell = document.createElement("td");
    const minCell = document.createElement("td");
    const maxFitnessCell = document.createElement("td");
    const minFitnessCell = document.createElement("td");

    const maxPre = document.createElement("pre");
    const minPre = document.createElement("pre");
    const maxFitPre = document.createElement("pre");
    const minFitPre = document.createElement("pre");

    let maxGen = "";
    let minGen = "";
    let maxFit = "";
    let minFit = "";

    genData["poblacion"].forEach(sublist => {
      maxGen += "[" + sublist.join(", ") + "]\n";
      minGen += "[" + sublist.join(", ") + "]\n";
    });

    genData["fitness_max"].forEach(fit => {
      maxFit += fit + "\n";
    });
    genData["fitness_min"].forEach(fit => {
      minFit += fit + "\n";
    });

    maxPre.textContent = maxGen;
    minPre.textContent = minGen;
    maxFitPre.textContent = maxFit;
    minFitPre.textContent = minFit;

    genCell.textContent = i + 1;
    maxCell.appendChild(maxPre);
    minCell.appendChild(minPre);
    maxFitnessCell.appendChild(maxFitPre);
    minFitnessCell.appendChild(minFitPre);

    row.appendChild(genCell);
    row.appendChild(maxCell);
    row.appendChild(minCell);
    row.appendChild(maxFitnessCell);
    row.appendChild(minFitnessCell);

    tableBody.appendChild(row);
  }
}

// Función para generar la población y mostrarla
function generatePopulationAndDisplay() {
  fetch('http://localhost:8000/api/get-population')
    .then(response => response.json())
    .then(data => {
      const generations = data['data']['generaciones'];
      const bestMax = data['data']['mejor_individuo_max'];
      const bestMin = data['data']['mejor_individuo_min'];
      displaySublistInTable(generations, bestMax, bestMin);
    })
    .catch(error => { console.error('Error: ', error); });
}

// Asignar el evento al botón "INICIAR"
document.getElementById("start").addEventListener("click", function () {
  generatePopulationAndDisplay();
});
