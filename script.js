// Dados das estrelas (serão carregados de stars.js)
// const stars = [...]; // Os dados já estão em stars.js e serão acessados globalmente

function getClassification(star) {
    let classification = { type: "Desconhecido", img: "assets/star.png" };
    let radius = 0;

    // Processa o raio para obter um valor numérico
    if (star.st_rad && typeof star.st_rad === 'string') {
        // Remove caracteres não numéricos e a unidade "R" e Unicode do sol (☉)
        const numericRadius = star.st_rad.replace(/[^0-9.]/g, '');
        radius = parseFloat(numericRadius);
    } else if (star.st_rad && typeof star.st_rad === 'number') {
        radius = star.st_rad;
    }

    if (isNaN(radius)) {
        // Se o raio não puder ser parseado, usa o tipo 'Desconhecido'
        classification.type = "Desconhecido";
    } else if (radius < 0.8) {
        classification.type = "Anã";
        classification.img = "assets/dwarf-star.png";
    } else if (radius < 10) {
        classification.type = "Gigante";
        classification.img = "assets/giant-star.png";
    } else {
        classification.type = "Supergigante";
        classification.img = "assets/supergiant-star.png";
    }
    return classification;
}

// Função para obter a imagem com base no tipo classificado
function getImageForClassification(classificationType) {
    switch (classificationType) {
        case "Anã": return "assets/dwarf-star.png";
        case "Gigante": return "assets/giant-star.png";
        case "Supergigante": return "assets/supergiant-star.png";
        default: return "assets/star.png";
    }
}


const sections = document.querySelectorAll('.section');
const navLinks = document.querySelectorAll('.nav-link');
const modal = document.getElementById('starModal');
const closeModal = document.getElementById('closeModal');
const detailsDiv = document.getElementById('starDetails');

function showSection(sectionId) {
    sections.forEach(sec => sec.style.display = 'none');
    document.getElementById(sectionId + 'Section').style.display = 'block';

    navLinks.forEach(link => link.classList.remove('active-link'));
    const currentLink = document.querySelector(`[onclick="showSection('${sectionId}')"]`);
    if (currentLink) {
        currentLink.classList.add('active-link');
    }
}

function renderCards(data, gridId) {
    const grid = document.getElementById(gridId);
    grid.innerHTML = ''; // Limpa o grid antes de adicionar novos cards

    if (!data || data.length === 0) {
        grid.innerHTML = '<p>Nenhuma estrela encontrada para esta categoria.</p>';
        return;
    }

    data.forEach(star => {
        const classification = getClassification(star); // Obtém a classificação baseada no raio
        const card = document.createElement('div');
        card.className = 'card';
        card.innerHTML = `
            <img src="${classification.img}" alt="${star.name}">
            <h3>${star.name}</h3>
            <p>${classification.type}</p>
        `;
        card.onclick = () => {
            detailsDiv.innerHTML = `
                <div class="star-name">${star.name}</div>
                <img src="${classification.img}" alt="${star.name}" style="width:200px;display:block;margin:auto;padding:10px;">
                <div class="star-data"><b>Nome:</b> ${star.name}</div>
                <div class="star-data"><b>Tipo (Raio):</b> ${classification.type}</div>
                <div class="star-data"><b>Raio:</b> ${star.st_rad || 'N/A'}</div>
                <div class="star-data"><b>Magnitude Absoluta:</b> ${star.sy_kmag !== null ? star.sy_kmag : 'N/A'}</div>
                <div class="star-data"><b>Temperatura:</b> ${star.st_teff !== null ? star.st_teff + ' K' : 'N/A'}</div>
                <div class="star-data"><b>Massa:</b> ${star.st_mass || 'N/A'}</div>
            `;
            modal.style.display = 'flex';
        }
        grid.appendChild(card);
    });
}

// --- Filtros e Renderização ---

// 1. Estrelas por Tamanho (classificadas pelo raio)
const sizeStars = stars.map(star => {
    const classification = getClassification(star);
    return { ...star, calculated_type: classification.type, img_type: classification.img };
});
renderCards(sizeStars, 'sizeGrid');

// 2. Estrelas com Alta Magnitude (considerando valores mais negativos como alta magnitude)
// Definindo um limiar para "alta magnitude". Valores menores (mais negativos) indicam maior brilho aparente.
const magnitudeThreshold = 2; // Você pode ajustar este valor
const magnitudeStars = stars.filter(star => star.sy_kmag !== null && star.sy_kmag < magnitudeThreshold)
    .map(star => {
        const classification = getClassification(star);
        return { ...star, calculated_type: classification.type, img_type: classification.img };
    });
renderCards(magnitudeStars, 'magnitudeGrid');


// 3. Estrelas Mais Quentes
// Filtra as estrelas com base na temperatura superficial (st_teff)
// Define um limiar para "mais quentes". Estrelas com st_teff > 7000 K são consideradas mais quentes.
// Ajuste o valor de 7000 K se desejar um critério diferente.
// 3. Estrelas Mais Quentes (Usando a temperatura)
const temperatureThreshold = 7000; // Em Kelvin
const hotStarsData = stars.filter(star => star.st_teff !== undefined && star.st_teff !== null && star.st_teff > temperatureThreshold);
hotStarsData.forEach(star => {
    const classification = getClassification(star); // Garante que tenham imagem e classificação
    star.type = classification.type;
    star.img_type = classification.img;
});
renderCards(hotStarsData, 'hotGrid'); // Assumindo que você tem um <div id="hotGrid"> no seu HTML



// --- Event Listeners ---
closeModal.onclick = () => modal.style.display = 'none';
window.onclick = e => {
    if (e.target == modal) {
        modal.style.display = 'none';
    }
}

// Exibe a seção inicial ao carregar a página
showSection('size');