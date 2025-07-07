// Configuração base da API

const API_BASE = `${window.location.origin}/api`;

// Função para fazer requisições HTTP
async function fazerRequisicao(url, opcoes = {}) {
    try {
        const resposta = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...opcoes.headers
            },
            ...opcoes
        });
        
        const dados = await resposta.json();
        
        if (!dados.success) {
            throw new Error(dados.error || 'Erro na requisição');
        }
        
        return dados;
    } catch (erro) {
        console.error('Erro na requisição:', erro);
        alert('Erro: ' + erro.message);
        throw erro;
    }
}





// Carregar cursos da API
async function carregarCursos(filtros = {}) {
    try {
        // Construir URL com parâmetros de filtro
        const params = new URLSearchParams();
        
        if (filtros.area) params.append('area', filtros.area);
        if (filtros.metodologia) params.append('metodologia', filtros.metodologia);
        if (filtros.faixa) params.append('faixa', filtros.faixa);
        if (filtros.busca) params.append('busca', filtros.busca);
        if (filtros.tipo_busca) params.append('tipo_busca', filtros.tipo_busca);
        
        const url = `${API_BASE}/cursos?${params.toString()}`;
        const dados = await fazerRequisicao(url);
        
        // Atualizar a tabela com os cursos
        atualizarTabelaCursos(dados.cursos);
        atualizarContadores(dados.total);
        
    } catch (erro) {
        console.error('Erro ao carregar cursos:', erro);
    }
}





// Atualizar tabela de cursos
function atualizarTabelaCursos(cursos) {
    const tbody = document.querySelector('#tabelaCursos tbody');
    tbody.innerHTML = '';
    
    cursos.forEach(curso => {
        const linha = document.createElement('tr');
        linha.innerHTML = `
            <td>
                <input type="checkbox" class="checkbox-curso" value="${curso.id}">
            </td>
            <td>${curso.nome}</td>
            <td>
                <span class="badge badge-area" onclick="editarArea(${curso.id}, this)">
                    ${curso.area || 'Clique para editar'}
                </span>
            </td>
            <td><span class="badge badge-metodologia">${curso.metodologia}</span></td>
            <td><span class="badge badge-faixa">${curso.faixa}</span></td>
            <td>
                <button class="btn btn-edit btn-sm" onclick="editarCurso(${curso.id})">
                    Editar
                </button>
                <button class="btn btn-delete btn-sm" onclick="excluirCurso(${curso.id})">
                    Excluir
                </button>
            </td>
        `;
        tbody.appendChild(linha);
    });
}





// Adicionar novo curso
async function adicionarCurso(dadosCurso) {
    try {
        const dados = await fazerRequisicao(`${API_BASE}/cursos`, {
            method: 'POST',
            body: JSON.stringify(dadosCurso)
        });
        
        alert('Curso adicionado com sucesso!');
        carregarCursos(); // Recarregar lista
        
    } catch (erro) {
        console.error('Erro ao adicionar curso:', erro);
    }
}





// Editar curso
async function editarCurso(cursoId) {
    const novoNome = prompt('Digite o novo nome do curso:');
    if (!novoNome) return;
    
    try {
        await fazerRequisicao(`${API_BASE}/cursos/${cursoId}`, {
            method: 'PUT',
            body: JSON.stringify({ nome: novoNome })
        });
        
        alert('Curso atualizado com sucesso!');
        carregarCursos();
        
    } catch (erro) {
        console.error('Erro ao editar curso:', erro);
    }
}





// Editar área
async function editarArea(cursoId, elemento) {
    const novaArea = prompt('Digite a nova área:', elemento.textContent);
    if (novaArea === null) return;
    
    try {
        await fazerRequisicao(`${API_BASE}/cursos/${cursoId}`, {
            method: 'PUT',
            body: JSON.stringify({ area: novaArea })
        });
        
        elemento.textContent = novaArea || 'Clique para editar';
        
    } catch (erro) {
        console.error('Erro ao editar área:', erro);
    }
}





// Excluir curso
async function excluirCurso(cursoId) {
    if (!confirm('Tem certeza que deseja excluir este curso?')) return;
    
    try {
        await fazerRequisicao(`${API_BASE}/cursos/${cursoId}`, {
            method: 'DELETE'
        });
        
        alert('Curso excluído com sucesso!');
        carregarCursos();
        
    } catch (erro) {
        console.error('Erro ao excluir curso:', erro);
    }
}





// Carregar opções para filtros
async function carregarOpcoes() {
    try {
        const dados = await fazerRequisicao(`${API_BASE}/cursos/opcoes`);
        
        // Atualizar selects de filtro
        atualizarSelect('filtroArea', dados.opcoes.areas);
        atualizarSelect('filtroMetodologia', dados.opcoes.metodologias);
        atualizarSelect('filtroFaixa', dados.opcoes.faixas);
        
    } catch (erro) {
        console.error('Erro ao carregar opções:', erro);
    }
}





// Atualizar select com opções
function atualizarSelect(selectId, opcoes) {
    const select = document.getElementById(selectId);
    if (!select) return;
    
    // Manter primeira opção (ex: "Todas as áreas")
    const primeiraOpcao = select.children[0];
    select.innerHTML = '';
    select.appendChild(primeiraOpcao);
    
    // Adicionar novas opções
    opcoes.forEach(opcao => {
        const option = document.createElement('option');
        option.value = opcao;
        option.textContent = opcao;
        select.appendChild(option);
    });
}





// Inicializar quando a página carregar
document.addEventListener('DOMContentLoaded', function() {
    carregarCursos();
    carregarOpcoes();
    
    // Configurar eventos de filtro
    document.getElementById('campoBusca')?.addEventListener('input', aplicarFiltros);
    document.getElementById('filtroArea')?.addEventListener('change', aplicarFiltros);
    document.getElementById('filtroMetodologia')?.addEventListener('change', aplicarFiltros);
    document.getElementById('filtroFaixa')?.addEventListener('change', aplicarFiltros);
});





// Aplicar filtros
function aplicarFiltros() {
    const filtros = {
        busca: document.getElementById('campoBusca')?.value,
        area: document.getElementById('filtroArea')?.value,
        metodologia: document.getElementById('filtroMetodologia')?.value,
        faixa: document.getElementById('filtroFaixa')?.value,
        tipo_busca: document.querySelector('.search-type.active')?.dataset.type || 'curso'
    };
    
    carregarCursos(filtros);
}






// Conectar formulário de adicionar curso
document.getElementById('formAdicionarCurso')?.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const dadosCurso = {
        nome: document.getElementById('campoNome').value,
        area: document.getElementById('campoArea').value,
        metodologia: document.getElementById('campoMetodologia').value,
        faixa: document.getElementById('campoFaixa').value
    };
    
    adicionarCurso(dadosCurso);
    
    // Fechar modal e limpar formulário
    document.getElementById('modalAdicionar').style.display = 'none';
    this.reset();
});


        let currentSearchType = 'curso';
        let allCursos = [];
        let filteredCursos = [];
        let selectedCursos = new Set();
        let currentView = 'table';

        // Inicialização
        document.addEventListener('DOMContentLoaded', function() {
            loadCursos();
            loadFilterOptions();
            setupEventListeners();
        });

        function setupEventListeners() {
            document.getElementById('searchInput').addEventListener('input', filterCursos);
            document.getElementById('areaFilter').addEventListener('change', filterCursos);
            document.getElementById('metodologiaFilter').addEventListener('change', filterCursos);
            document.getElementById('faixaFilter').addEventListener('change', filterCursos);
            
            document.getElementById('addCursoForm').addEventListener('submit', handleAddCurso);
            document.getElementById('uploadForm').addEventListener('submit', handleUploadPlanilha);
        }

        async function loadCursos() {
            try {
                const response = await fetch(`${API_BASE}/cursos`);
                const data = await response.json();
                allCursos = data.cursos;
                filteredCursos = [...allCursos];

                renderCursos();
                updateStats();
            } catch (error) {
                console.error('Erro ao carregar cursos:', error);
                alert('Erro ao carregar cursos. Verifique se o backend está rodando.');
            }
        }


// Verifique a resposta da sua API. Se ela retorna `opcoes`, o código abaixo está correto.
async function loadFilterOptions() {
    try {
        const response = await fetch(`${API_BASE}/cursos/opcoes`);
        const data = await response.json();

        if (data.success && data.opcoes) { // Verifique se `opcoes` existe
            populateSelect("areaFilter", data.opcoes.areas || []); // Use `|| []` como fallback
            populateSelect("metodologiaFilter", data.opcoes.metodologias || []);
            populateSelect("faixaFilter", data.opcoes.faixas || []);
        } else {
            console.error("Resposta da API de opções inválida:", data);
        }
    } catch (error) {
        console.error("Erro ao carregar opções de filtro:", error);
    }
}

// A função populateSelect deve ser robusta para arrays vazios
function populateSelect(selectId, options) {
    const select = document.getElementById(selectId);
    if (!select) return;

    const firstOption = select.children[0];
    select.innerHTML = "";
    select.appendChild(firstOption);

    if (Array.isArray(options)) { // Verifique se `options` é um array
        options.forEach(option => {
            const optionElement = document.createElement("option");
            optionElement.value = option;
            optionElement.textContent = option;
            select.appendChild(optionElement);
        });
    }
}

        function setSearchType(type) {
            currentSearchType = type;
            
            // Atualizar visual das tabs
            document.querySelectorAll('.filter-tab').forEach(tab => {
                tab.classList.remove('active');
            });
            event.target.classList.add('active');
            
            filterCursos();
        }

        function toggleView(view) {
            currentView = view;
            
            // Atualizar botões
            document.querySelectorAll('.view-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            document.getElementById(view + 'ViewBtn').classList.add('active');
            
            // Mostrar/esconder views
            if (view === 'table') {
                document.getElementById('tableView').style.display = 'block';
                document.getElementById('cardsView').style.display = 'none';
            } else {
                document.getElementById('tableView').style.display = 'none';
                document.getElementById('cardsView').style.display = 'grid';
            }
            
            renderCursos();
        }

        function filterCursos() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            const selectedAreas = Array.from(document.getElementById('areaFilter').selectedOptions).map(o => o.value).filter(v => v);
            const selectedMetodologias = Array.from(document.getElementById('metodologiaFilter').selectedOptions).map(o => o.value).filter(v => v);
            const selectedFaixas = Array.from(document.getElementById('faixaFilter').selectedOptions).map(o => o.value).filter(v => v);
            
            filteredCursos = allCursos.filter(curso => {
                // Filtro de texto baseado no tipo de pesquisa
                let textMatch = true;
                if (searchTerm) {
                    switch(currentSearchType) {
                        case 'curso':
                            textMatch = curso.nome.toLowerCase().includes(searchTerm);
                            break;
                        case 'area':
                            textMatch = (curso.area || '').toLowerCase().includes(searchTerm);
                            break;
                        case 'metodologia':
                            textMatch = curso.metodologia.toLowerCase().includes(searchTerm);
                            break;
                        case 'faixa':
                            textMatch = curso.faixa.toLowerCase().includes(searchTerm);
                            break;
                    }
                }
                
                // Filtros de seleção múltipla
                const areaMatch = selectedAreas.length === 0 || selectedAreas.includes(curso.area);
                const metodologiaMatch = selectedMetodologias.length === 0 || selectedMetodologias.includes(curso.metodologia);
                const faixaMatch = selectedFaixas.length === 0 || selectedFaixas.includes(curso.faixa);
                
                return textMatch && areaMatch && metodologiaMatch && faixaMatch;
            });
            
            renderCursos();
            updateStats();
        }

        function renderCursos() {
            if (currentView === 'table') {
                renderTable();
            } else {
                renderCards();
            }
        }

        function renderTable() {
            const tbody = document.getElementById('cursosBody');
            tbody.innerHTML = '';
            
            filteredCursos.forEach(curso => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>
                        <input type="checkbox" class="curso-checkbox" value="${curso.id}" 
                               onchange="toggleCursoSelection(${curso.id})" 
                               ${selectedCursos.has(curso.id) ? 'checked' : ''}>
                    </td>
                    <td>${curso.nome}</td>
                    <td>
                        ${curso.area ? 
                            `<span class="area-display">${curso.area}</span>` : 
                            '<em style="color: #999;">Não definida</em>'
                        }
                    </td>
                    <td><span class="metodologia-badge">${curso.metodologia}</span></td>
                    <td><span class="faixa-badge">${curso.faixa}</span></td>
                    <td>
                        <button class="btn btn-secondary" style="padding: 10px 20px; font-size: 12px;" 
                                onclick="editCurso(${curso.id})">Editar</button>
                        <button class="btn" style="background: #dc3545; color: white; padding: 10px 20px; font-size: 12px;" 
                                onclick="deleteCurso(${curso.id})">Excluir</button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        function renderCards() {
            const cardsContainer = document.getElementById('cardsView');
            cardsContainer.innerHTML = '';
            
            filteredCursos.forEach(curso => {
                const card = document.createElement('div');
                card.className = 'course-card';
                card.innerHTML = `
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 20px;">
                        <input type="checkbox" class="curso-checkbox" value="${curso.id}" 
                               onchange="toggleCursoSelection(${curso.id})" 
                               ${selectedCursos.has(curso.id) ? 'checked' : ''}>
                        <div style="display: flex; gap: 10px;">
                            <span class="metodologia-badge">${curso.metodologia}</span>
                            <span class="faixa-badge">${curso.faixa}</span>
                        </div>
                    </div>
                    <h3 style="color: #2d3748; margin-bottom: 15px; font-size: 18px; font-weight: 600;">${curso.nome}</h3>
                    <div style="margin-bottom: 20px;">
                        <label style="font-size: 12px; color: #8B0000; font-weight: 700; text-transform: uppercase;">Área de Conhecimento</label>
                        <div style="margin-top: 8px;">
                            ${curso.area ? 
                                `<span class="area-display">${curso.area}</span>` : 
                                '<em style="color: #999;">Não definida</em>'
                            }
                        </div>
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: flex-end;">
                        <button class="btn btn-secondary" style="padding: 8px 16px; font-size: 12px;" 
                                onclick="editCurso(${curso.id})">Editar</button>
                        <button class="btn" style="background: #dc3545; color: white; padding: 8px 16px; font-size: 12px;" 
                                onclick="deleteCurso(${curso.id})">Excluir</button>
                    </div>
                `;
                cardsContainer.appendChild(card);
            });
        }

        function toggleCursoSelection(cursoId) {
            if (selectedCursos.has(cursoId)) {
                selectedCursos.delete(cursoId);
            } else {
                selectedCursos.add(cursoId);
            }
            updateStats();
            updateSelectAllCheckbox();
        }

        function toggleSelectAll() {
            const selectAllCheckbox = document.getElementById('selectAllCheckbox');
            const checkboxes = document.querySelectorAll('.curso-checkbox');
            
            if (selectAllCheckbox.checked) {
                checkboxes.forEach(checkbox => {
                    checkbox.checked = true;
                    selectedCursos.add(parseInt(checkbox.value));
                });
            } else {
                checkboxes.forEach(checkbox => {
                    checkbox.checked = false;
                    selectedCursos.delete(parseInt(checkbox.value));
                });
            }
            updateStats();
        }

        function selectAll() {
            filteredCursos.forEach(curso => selectedCursos.add(curso.id));
            renderCursos();
            updateStats();
            updateSelectAllCheckbox();
        }

        function clearSelection() {
            selectedCursos.clear();
            renderCursos();
            updateStats();
            updateSelectAllCheckbox();
        }

        function updateSelectAllCheckbox() {
            const selectAllCheckbox = document.getElementById('selectAllCheckbox');
            if (!selectAllCheckbox) return;
            
            const visibleCursoIds = filteredCursos.map(c => c.id);
            const selectedVisibleCursos = visibleCursoIds.filter(id => selectedCursos.has(id));
            
            if (selectedVisibleCursos.length === 0) {
                selectAllCheckbox.checked = false;
                selectAllCheckbox.indeterminate = false;
            } else if (selectedVisibleCursos.length === visibleCursoIds.length) {
                selectAllCheckbox.checked = true;
                selectAllCheckbox.indeterminate = false;
            } else {
                selectAllCheckbox.checked = false;
                selectAllCheckbox.indeterminate = true;
            }
        }

        function updateStats() {
            document.getElementById('totalCursos').textContent = allCursos.length;
            document.getElementById('cursosExibidos').textContent = filteredCursos.length;
            document.getElementById('cursosSelecionados').textContent = selectedCursos.size;
            
            // Habilitar/desabilitar botões de exportação
            const hasSelection = selectedCursos.size > 0;
            document.getElementById('exportBtn1').disabled = !hasSelection;
            document.getElementById('exportBtn2').disabled = !hasSelection;
        }

        // Modais
        function openAddModal() {
            document.getElementById('addModal').style.display = 'block';
        }

        function openUploadModal() {
            document.getElementById('uploadModal').style.display = 'block';
        }

        function closeModal(modalId) {
            document.getElementById(modalId).style.display = 'none';
            if (modalId === 'addModal') {
                document.getElementById('addCursoForm').reset();
            }
            if (modalId === 'uploadModal') {
                document.getElementById('uploadForm').reset();
                document.getElementById('fileInfo').style.display = 'none';
                document.getElementById('uploadBtn').disabled = true;
            }
        }

        // Adicionar curso
        async function handleAddCurso(event) {
            event.preventDefault();
            
            const formData = {
                nome: document.getElementById('cursoNome').value,
                area: document.getElementById('cursoArea').value,
                metodologia: document.getElementById('cursoMetodologia').value,
                faixa: document.getElementById('cursoFaixa').value
            };
            
            try {
                const response = await fetch(`${API_BASE}/cursos`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });
                
                if (response.ok) {
                    closeModal('addModal');
                    loadCursos();
                    loadFilterOptions();
                    alert('Curso adicionado com sucesso!');
                } else {
                    const error = await response.json();
                    alert('Erro ao adicionar curso: ' + error.error);
                }
            } catch (error) {
                console.error('Erro ao adicionar curso:', error);
                alert('Erro ao adicionar curso. Verifique sua conexão.');
            }
        }

                // Upload de planilha
        document.getElementById('arquivoPlanilha')?.addEventListener('change', function(e) {
            const arquivo = e.target.files[0];
            if (!arquivo) return;
            
            // Verificar tipo de arquivo
            const extensoesPermitidas = ['.xlsx', '.xls'];
            const extensao = arquivo.name.toLowerCase().substring(arquivo.name.lastIndexOf('.'));
            
            if (!extensoesPermitidas.includes(extensao)) {
                alert('Por favor, selecione um arquivo Excel (.xlsx ou .xls)');
                return;
            }
            
            // Confirmar upload
            if (!confirm(`Fazer upload do arquivo "${arquivo.name}"?`)) {
                return;
            }
            
            fazerUploadPlanilha(arquivo);
        });

        async function fazerUploadPlanilha(arquivo) {
            try {
                // Mostrar loading
                const btnUpload = document.querySelector('button[onclick*="arquivoPlanilha"]');
                const textoOriginal = btnUpload.textContent;
                btnUpload.textContent = '⏳ Processando...';
                btnUpload.disabled = true;
                
                // Criar FormData para envio do arquivo
                const formData = new FormData();
                formData.append('arquivo', arquivo);
                
                // Fazer requisição
                const resposta = await fetch(`${API_BASE}/cursos/upload`, {
                    method: 'POST',
                    body: formData
                });
                
                const dados = await resposta.json();
                
                if (dados.success) {
                    let mensagem = `Upload concluído!\n\n`;
                    mensagem += `✅ Cursos adicionados: ${dados.cursos_adicionados}\n`;
                    
                    if (dados.erros.length > 0) {
                        mensagem += `\n⚠️ Erros encontrados:\n`;
                        dados.erros.forEach(erro => mensagem += `• ${erro}\n`);
                    }
                    
                    alert(mensagem);
                    carregarCursos(); // Recarregar lista
                } else {
                    throw new Error(dados.error);
                }
                
            } catch (erro) {
                console.error('Erro no upload:', erro);
                alert('Erro no upload: ' + erro.message);
            } finally {
                // Restaurar botão
                const btnUpload = document.querySelector('button[onclick*="arquivoPlanilha"]');
                btnUpload.textContent = textoOriginal;
                btnUpload.disabled = false;
                
                // Limpar input
                document.getElementById('arquivoPlanilha').value = '';
            }
        }





// Exportar PDF
// Certifique-se de que esta função exista e seja chamada pelos checkboxes
function getSelectedCursoIds() {
    const selectedIds = [];
    document.querySelectorAll(".curso-checkbox:checked").forEach(checkbox => {
        selectedIds.push(parseInt(checkbox.value));
    });
    return selectedIds;
}

// Função para exportar para PDF
async function exportToPDF(design) {
    const cursoIds = getSelectedCursoIds();

    if (cursoIds.length === 0) {
        alert("Por favor, selecione pelo menos um curso para exportar.");
        return;
    }

    try {
        // Faz a requisição POST para o backend
        const response = await fetch(`${API_BASE}/cursos/export/pdf`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                curso_ids: cursoIds,
                design: design,
                titulo: "Relatório de Cursos Unyleya" // Título opcional para o PDF
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || "Erro ao gerar PDF");
        }

        // Recebe o blob (arquivo PDF) da resposta
        const blob = await response.blob();

        // Cria um URL para o blob
        const url = window.URL.createObjectURL(blob);

        // Cria um link temporário e simula o clique para download
        const a = document.createElement("a");
        a.href = url;
        a.download = `relatorio_cursos_${design}_${new Date().toISOString().slice(0,10)}.pdf`;
        document.body.appendChild(a);
        a.click();

        // Limpa o URL e o link temporário
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        alert("PDF gerado e download iniciado!");

    } catch (error) {
        console.error("Erro ao exportar PDF:", error);
        alert("Erro ao gerar PDF: " + error.message);
    }
}




        // Editar e deletar curso (implementação básica)
        async function editCurso(cursoId) {
            const curso = allCursos.find(c => c.id === cursoId);
            if (!curso) return;
            
            const novoNome = prompt('Novo nome do curso:', curso.nome);
            if (novoNome && novoNome !== curso.nome) {
                try {
                    const response = await fetch(`${API_BASE}/cursos/${cursoId}`, {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ nome: novoNome })
                    });
                    
                    if (response.ok) {
                        loadCursos();
                        alert('Curso atualizado com sucesso!');
                    } else {
                        const error = await response.json();
                        alert('Erro ao atualizar curso: ' + error.error);
                    }
                } catch (error) {
                    console.error('Erro ao atualizar curso:', error);
                    alert('Erro ao atualizar curso.');
                }
            }
        }

        async function deleteCurso(cursoId) {
            if (confirm('Tem certeza que deseja excluir este curso?')) {
                try {
                    const response = await fetch(`${API_BASE}/cursos/${cursoId}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        selectedCursos.delete(cursoId);
                        loadCursos();
                        alert('Curso excluído com sucesso!');
                    } else {
                        const error = await response.json();
                        alert('Erro ao excluir curso: ' + error.error);
                    }
                } catch (error) {
                    console.error('Erro ao excluir curso:', error);
                    alert('Erro ao excluir curso.');
                }
            }
        }

        // Fechar modal ao clicar fora
        window.onclick = function(event) {
            const modals = document.querySelectorAll('.modal');
            modals.forEach(modal => {
                if (event.target === modal) {
                    modal.style.display = 'none';
                }
            });
        }




// MOSTRAR NO CONSOLE NAVEGADOR       
let cursos = [];

fetch(`${API_BASE}/cursos`)
  .then(res => res.json())
  .then(data => {
    cursos = data; // agora cursos fica acessível no console
    console.log('Cursos carregados:', cursos);
  });





  
function renderPagination(totalPages, currentPage) {
    const container = document.getElementById('pagination');
    if (!container) return;

    container.innerHTML = ''; // limpar

    for (let i = 1; i <= totalPages; i++) {
        const btn = document.createElement('button');
        btn.className = 'btn btn-page';
        btn.textContent = i;
        if (i === currentPage) {
            btn.style.backgroundColor = '#007bff';
            btn.style.color = '#fff';
        }
        btn.onclick = () => loadCursos(i);
        container.appendChild(btn);
    }
}





